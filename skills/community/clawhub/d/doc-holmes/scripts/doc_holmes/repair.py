"""文本体检与降噪（作用于我们控制的文本：OCR 重建层、triage 统计、审计报告）。

v1.0.0 范围：检测 + 清洗。对引擎内部的排版不做手术（AGPL 隔离）。
v1.1 计划（plan Phase 2）：camelCase 粘连拆分（wordninja）、标题图层合并回写。
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field

from . import skip_rules

DUP_EXACT_MIN_LEN = 6      # 完全相同行的最小长度（过滤页码等短 token）
DUP_NEAR_RATIO = 0.95      # 保留常数：近似判定已被证明误报编号系列，v1.0 仅用精确相等
DUP_NEAR_MIN_LEN = 15


@dataclass
class TextIssues:
    """一段文本的噪声画像。"""
    line_count: int = 0
    control_chars: int = 0
    duplicate_pairs: int = 0
    duplicate_examples: list = field(default_factory=list)
    rule_hits: dict = field(default_factory=dict)   # rule -> count
    total_rule_hits: int = 0

    def watermark_lines(self) -> int:
        """水印级噪声行数（drop 级规则命中行）。"""
        return sum(
            cnt for rule, cnt in self.rule_hits.items()
            if any(r[0] == rule and r[2] == skip_rules.ACTION_DROP
                   for r in skip_rules.RULES)
        )


def _has_text(line):
    return any(ch.isalpha() or "一" <= ch <= "鿿" for ch in line)


def find_duplicate_pairs(lines):
    """相邻重复行（图层重复打印的典型形态）。

    判据（v1.0 收紧，防编号系列误报）：完全相同（strip 后）且长度 ≥6 且含文字。
    编号系列（Line 1/Line 10、水印 …0/…1/…2、行号、页码）相似但不同 → 不误报。
    返回 [(i, line_a, line_b)]。
    """
    dups = []
    prev = None
    for i, line in enumerate(lines):
        cur = " ".join(line.split())
        if not cur:
            prev = None
            continue
        if prev is not None:
            # v1.0 只认精确相等：近似(比率)判定实测会误报编号系列
            # （Line 1 vs Line 10 比率 0.98；水印 …0/…1/…2）。漏报代价=多翻一行，
            # 误报代价=A 级被降级误导用户 —— 取保守侧。
            same = (cur == prev and len(cur) >= DUP_EXACT_MIN_LEN and _has_text(cur))
            if same:
                dups.append((i, prev, cur))
        prev = cur
    return dups


def detect_issues(text: str) -> TextIssues:
    issues = TextIssues()
    lines = text.splitlines()
    issues.line_count = len(lines)
    issues.control_chars = len(skip_rules.CONTROL_RE.findall(text))
    dups = find_duplicate_pairs(lines)
    issues.duplicate_pairs = len(dups)
    issues.duplicate_examples = ["%r ~ %r" % (a, b) for _, a, b in dups[:3]]
    stats = skip_rules.scan_lines(lines)
    issues.rule_hits = stats["per_rule"]
    issues.total_rule_hits = stats["total_hits"]
    return issues


def clean_text(text: str):
    """剥控制字符 + 剔除 drop 级噪声行。返回 (cleaned, hits)。"""
    return skip_rules.clean_text(text)
