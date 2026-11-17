"""错误分类与修复策略 — 跨阶段共享。

从 Agnes API raw error 中提取原因并分类，应用对应修复策略后重试。
所有 image/video 生成阶段共用同一套逻辑。
"""
import re
from typing import Optional


def classify(raw: dict, default_status: str = "") -> tuple[str, str]:
    """从 API 返回的 raw 整包中提取真实错误原因并分类。

    返回 (category, reason)。category ∈
      rate_limit      限流(429/quota/too many) → 退避，本轮不重提
      invalid_image   图片无效/内容审核(400 Invalid image / unsafe / moderation) → 换提示词后重提
      transient       瞬时故障(连接断开/超时/5xx) → 原样重提
      bad_request     其他 4xx(参数/提示词问题) → 换提示词后重提
      unknown         其他 → 原样重提(安全默认)
    """
    if not isinstance(raw, dict):
        raw = {}
    err = raw.get("error")
    code, message = "", ""
    if isinstance(err, dict):
        code = str(err.get("code", ""))
        message = str(err.get("message", ""))
    elif isinstance(err, str):
        message = err
    text = f"{code} {message}".lower()

    if "429" in text or "rate" in text or "ratelimit" in text or "too many" in text or "quota" in text:
        return ("rate_limit", f"{code} {message}".strip() or "rate limit")
    if ("invalid image" in text or "invalid_image" in text or "unsafe" in text
            or "moderation" in text or "content policy" in text or "被拦截" in text
            or "审核" in text or "400" in text):
        return ("invalid_image", f"{code} {message}".strip() or "invalid image")
    if any(k in text for k in ("remoteclosed", "remotedisconnected", "connection",
                                "reset", "timeout", "timed out", "502", "503",
                                "504", "500", "gateway", "temporarily")):
        return ("transient", f"{code} {message}".strip() or "transient")
    if code and code.startswith("4"):
        return ("bad_request", f"{code} {message}".strip() or "bad request")
    return ("unknown", f"{code} {message}".strip() or default_status)


# ── 提示词软化策略（用于 invalid_image / bad_request） ──────────

# 常见触发审核的词汇（暴力/血腥/武器/敏感内容），替换为中性表述
_SOFTEN_MAP = [
    # 暴力动作 → 中性动作
    (re.compile(r'砍杀|斩杀|砍死|杀戮|屠杀|砍[向倒]'), '战斗'),
    (re.compile(r'刺穿|贯穿|捅[穿入]'), '击中'),
    (re.compile(r'撕碎|撕裂|扯碎'), '破坏'),
    (re.compile(r'鲜血|血迹|血腥|血[泊染渍]|流血'), '污迹'),
    (re.compile(r'伤口|创伤|伤痕|伤疤|损伤'), '痕迹'),
    (re.compile(r'尸体|尸骸|死者|阵亡|战死|死亡'), '倒下'),
    # 武器描述 → 模糊化
    (re.compile(r'刀刃|刀锋|利刃|锋利[的]?刀'), '武器'),
    (re.compile(r'枪[口管]|枪械'), '武器'),
    # 极端环境 → 弱化
    (re.compile(r'废墟|断壁残垣|瓦砾'), '破损建筑'),
    (re.compile(r'硝烟弥漫|浓烟滚滚'), '烟雾'),
    (re.compile(r'弹孔|弹痕'), '痕迹'),
    (re.compile(r'骷髅|骸骨|白骨'), '遗迹'),
    # 恐怖/阴暗描述 → 中化
    (re.compile(r'恐怖|可怕|狰狞|阴森|诡异'), '沉重'),
    (re.compile(r'绝望|无助|悲惨|凄凉'), '肃穆'),
]

# 需要额外删除的整段关键词（暴力/血腥类，保留武器类）
_DELETE_KEYWORDS = [
    '沾着灰尘', '泥土', '血污', '污渍',  # 脏污描述容易撞审核
]


def soften_prompt(prompt: str) -> str:
    """对因 invalid_image 被拒的 image prompt 做安全化处理。

    替换暴力/血腥/敏感词汇为中性表述，降低被内容审核拦截的概率。
    返回修改后的 prompt。若无需修改返回原字符串。
    """
    result = prompt
    for pattern, replacement in _SOFTEN_MAP:
        result = pattern.sub(replacement, result)
    for kw in _DELETE_KEYWORDS:
        result = result.replace(kw, '')
    # 清理多余空格和逗号
    result = re.sub(r'[，,]\s*[，,]', '，', result)
    result = re.sub(r'\s{2,}', ' ', result).strip()
    return result


def apply_image_strategy(category: str, prompt: str,
                         model: str = None) -> tuple[str, Optional[str], str]:
    """根据错误分类，返回 (修正后的prompt, 换用的model, 策略描述)。

    返回 (prompt, model, strategy_desc)。model=None 表示不换模型。
    调用方循环直到生成成功或所有策略耗尽。
    """
    if category in ("invalid_image", "bad_request"):
        softened = soften_prompt(prompt)
        if softened != prompt:
            return (softened, model, f"软化提示词（{category}）")
        # 如果软化后无变化（prompt 本身无敏感词），尝试换模型
        fallback = "agnes-image-2.0-flash" if (model or "").endswith("2.1-flash") else "agnes-image-2.1-flash"
        return (prompt, fallback, f"换模型({fallback})（{category}）")
    if category == "rate_limit":
        return (prompt, model, "限流退避（由上层 capped retry 处理）")
    # transient / unknown → 原样重试
    return (prompt, model, f"原样重试（{category}）")
