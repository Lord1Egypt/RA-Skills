"""阶段1：原始输入预处理（规则引擎，不调用 LLM）。

职责：
1. 基础清洗：首尾空格、控制字符、零宽字符、不可见 Unicode、注入类 payload
2. 长度校验：过短直接拦截；过长提示精简
3. 黑名单匹配：违规话术分级标记（block 级 / warning 级）

输出：PreprocessResult(rule_block, risk_type, raw_text_cleaned, ...)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 清洗用正则
# ---------------------------------------------------------------------------

# 零宽字符 & 不可见 Unicode（U+200B-U+200F、U+202A-U+202E、U+2060-U+206F、U+FEFF）
_INVISIBLE_RE = re.compile(
    r"[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff\u00ad]"
)
# C0/C1 控制字符（保留 \n 用于后续句子边界，但在清洗结果中压为空格）
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]")

# 注入类特殊 payload（命中即清除，不进入 LLM）
_PAYLOAD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("script_tag", re.compile(r"<\s*script.*?>.*?<\s*/\s*script\s*>", re.I | re.S)),
    ("html_tag", re.compile(r"</?\s*(script|iframe|img|svg|object|embed|link|style)\b[^>]*>", re.I)),
    ("sql_fragment", re.compile(
        r"(?i)(union\s+select|drop\s+table|or\s+1\s*=\s*1|;--|--\s|/\*.*?\*/)")),
    ("markdown_injection", re.compile(r"!\[[^\]]*\]\((https?://|javascript:)", re.I)),
    ("prompt_marker", re.compile(r"(<\|im_start\|>|<\|im_end\|>|<\|endoftext\|>|###\s*system)", re.I)),
]

# ---------------------------------------------------------------------------
# 黑名单词库（两级）
# ---------------------------------------------------------------------------

# block 级：命中即判定索要投资建议/违规，正常情况下 LLM 层也会 block（双保险）
RISK_WORDS_BLOCK: tuple[str, ...] = (
    "稳赚", "必涨", "必跌", "保本", "保收益", "稳赚不赔", "翻倍", "涨停",
    "内幕", "内幕消息", "老鼠仓", "坐庄", "操盘", "带单", "喊单", "拉群",
    "老师带你", "百分百", "百分之百", "零风险", "无风险套利", "抄底密码",
    "预测涨跌", "保证收益", "收益率保证",
)

# warning 级：命中不拦截，但强制要求 LLM 意图层关注（如口语化“能买吗”之外的敏感表达）
RISK_WORDS_WARNING: tuple[str, ...] = (
    "借钱", "贷款炒", "加杠杆", "配资", "梭哈", "全仓", "抵押房",
)

# ---------------------------------------------------------------------------
# 结果结构
# ---------------------------------------------------------------------------


@dataclass
class PreprocessResult:
    raw_text: str
    raw_text_cleaned: str
    rule_block: bool = False
    risk_type: str = ""            # too_short / too_long / sensitive_word / payload
    rule_labels: list[str] = field(default_factory=list)   # hit_rule_block_word 等
    blocked_reason: str = ""       # rule_block=true 时给前端的提示


def clean_text(text: str) -> str:
    """去除控制字符、零宽字符、注入 payload，压缩空白。"""
    if not text:
        return ""
    text = _INVISIBLE_RE.sub("", text)
    text = _CONTROL_RE.sub(" ", text)
    removed_payload_labels: list[str] = []
    for label, pattern in _PAYLOAD_PATTERNS:
        if pattern.search(text):
            removed_payload_labels.append(label)
            text = pattern.sub(" ", text)
    # 压缩空白（含全角空格）
    text = re.sub(r"[ \t\r\n\f\v\u3000]+", " ", text).strip()
    return text


def _match_words(text: str, words: tuple[str, ...]) -> list[str]:
    return [w for w in words if w in text]


def preprocess(raw_text: str, max_length: int = 2000) -> PreprocessResult:
    """阶段1主入口。rule_block=true 时调用方应直接终止，不进入 LLM 意图识别。"""
    cleaned = clean_text(raw_text or "")
    result = PreprocessResult(raw_text=raw_text or "", raw_text_cleaned=cleaned)

    # ---- 长度校验（清洗后判断，避免纯零宽字符骗过长度）----
    if len(cleaned) < 2:
        result.rule_block = True
        result.risk_type = "too_short"
        result.rule_labels.append("too_short")
        result.blocked_reason = "您的输入过短，请输入 ETF、行业或指数相关的投研问题。"
        return result

    if len(cleaned) > max_length:
        result.rule_block = True
        result.risk_type = "too_long"
        result.rule_labels.append("too_long")
        result.blocked_reason = f"您的提问超过平台最大输入限制（{max_length} 字符），请精简后重试。"
        return result

    # ---- 黑名单匹配（block 级词库）----
    hit_block = _match_words(cleaned, RISK_WORDS_BLOCK)
    if hit_block:
        result.rule_block = True
        result.risk_type = "sensitive_word"
        result.rule_labels.append("hit_rule_block_word:" + ",".join(hit_block))
        result.blocked_reason = (
            "本平台仅提供客观 ETF 投研数据分析，不提供荐股、收益承诺、买卖点位等投资决策建议，"
            "请调整您的提问。"
        )
        return result

    # ---- 黑名单匹配（warning 犯规倾向，不拦截，仅打标供 LLM 层参考）----
    hit_warning = _match_words(cleaned, RISK_WORDS_WARNING)
    if hit_warning:
        result.rule_labels.append("hit_rule_warning_word:" + ",".join(hit_warning))

    return result
