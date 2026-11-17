"""跳翻规则集：识别不该翻译 / 应剔除的噪声行。

来源：阅读台 6,469 条脏语料失败模式 10 类（plan.md 附录 B）+ 实锤样本
（京ICP备、扫一扫下载、© 2023 Elsevier、/G13 /F22 伪影、纯 URL/DOI/页码行…）。

三个用途：
  1) triage 噪声统计 —— 报告里明示「这份文件有哪些噪声」；
  2) OCR 重建文本层时清洗（C 级通路的文本完全由我们写入，规则在此生效）；
  3) 批量报告的噪声画像。
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ACTION_SKIP = "skip_translate"   # 保留原文，不做翻译（页眉/版权/URL…）
ACTION_DROP = "drop"             # 直接剔除（水印/伪影/控制字符载体行）


@dataclass
class RuleHit:
    rule: str
    action: str
    text: str


# (规则名, 正则, 动作)。新增规则必须带 tests/test_skip_rules.py 实锤用例。
artifact_re = re.compile(r"(?<![\w/])/[A-Z]\d{1,3}(?![\w/])")

RULES = [
    ("icp_filing",
     re.compile(r"(?:京)?ICP\s*[备證]\s*\d+|ICP\s*License", re.I),
     ACTION_DROP),
    ("watermark_download",
     re.compile(r"扫一扫|扫码(?:下载|关注)|下载.{0,8}APP|关注(?:微信)?公众号|仅供试读|内部资料"),
     ACTION_DROP),
    ("copyright",
     re.compile(r"©\s*\d{4}(?:\s*[-–]\s*\d{4})?|Copyright\s*©?\s*\d{4}|All [Rr]ights [Rr]eserved"),
     ACTION_SKIP),
    ("journal_header",
     re.compile(r"Chinese Journal of|中华.{2,14}杂志|Vol\.\s*\d+.{0,6}No\.\s*\d+", re.I),
     ACTION_SKIP),
    ("url_only",
     re.compile(r"^\s*(?:https?://|www\.)\S+\s*$", re.I),
     ACTION_SKIP),
    ("doi_only",
     re.compile(r"^\s*(?:https?://(?:dx\.)?doi\.org/|doi\s*[:：]\s*10\.)\S+", re.I),
     ACTION_SKIP),
    ("page_number",
     re.compile(r"^\s*[—–-]?\s*\d{1,4}\s*[—–-]?\s*$"),
     ACTION_SKIP),
    ("artifact_token", artifact_re, ACTION_DROP),
]

# 零宽字符与控制字符（字距异常/复制痕迹的常见载体）
CONTROL_RE = re.compile(r"[\u200b\u200c\u200d\u2060\ufeff\x00-\x08\x0b\x0c\x0e-\x1f]")


def classify_line(line: str) -> list:
    """返回一行命中的全部规则（可能多条）。"""
    hits = []
    for name, pattern, action in RULES:
        if pattern.search(line):
            hits.append(RuleHit(rule=name, action=action, text=line.strip()))
    return hits


def scan_lines(lines) -> dict:
    """对多行文本做噪声画像。返回 per-rule 计数 + 总命中。"""
    per_rule = {}
    total = 0
    for line in lines:
        for hit in classify_line(line):
            per_rule[hit.rule] = per_rule.get(hit.rule, 0) + 1
            total += 1
    return {"per_rule": per_rule, "total_hits": total, "line_count": len(lines)}


def strip_control_chars(text: str) -> str:
    return CONTROL_RE.sub("", text)


def clean_text(text: str):
    """清洗一段提取文本（供 OCR 重建层 / 统计使用）。

    返回 (cleaned_text, hits)。策略：
      - 伪影 token（/G13）：只剥 token，保留整行（防误删临床正文）；
      - 其余 drop 级命中（水印/ICP）：整行剔除；
      - 控制字符一律剥除。
    """
    hits = []
    out_lines = []
    for line in text.splitlines():
        line_hits = classify_line(line)
        hits.extend(line_hits)
        drop_rules = {h.rule for h in line_hits if h.action == ACTION_DROP}
        if drop_rules and drop_rules != {"artifact_token"}:
            continue
        if "artifact_token" in drop_rules:
            for name, pattern, _action in RULES:
                if name == "artifact_token":
                    line = pattern.sub("", line)
        out_lines.append(strip_control_chars(line))
    cleaned = "\n".join(out_lines)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned, hits
