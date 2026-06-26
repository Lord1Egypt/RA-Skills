#!/usr/bin/env python3
"""
cn_typo_scan.py — scan a text-extracted PPTX / MD for the character-level typo
patterns observed in MiniMax-M2.7 `\\uXXXX` escape mis-encoding.

Usage:
    python -m markitdown deck.pptx > /tmp/deck.txt
    python3 cn_typo_scan.py /tmp/deck.txt
    # Exit 0 = clean; exit 1 = hits found (see stderr for details).

Exit code is what CI / compile.js can gate on.
"""
from __future__ import annotations
import sys
import re
import pathlib

# Red-flag dyads and phrases observed in 2026-04-18 runs.
# These are character combinations that should never appear in banker prose and
# strongly suggest a `\\uXXXX` escape went wrong. Extend this list as new typo
# patterns are encountered.
RED_FLAG_DYADS = [
    # --- initial batch (observed 2026-04-18 Cambricon v9 deck) ---
    # Cambricon case (寒武纪 → 宽厭谛79 observed)
    ("宽厭", "likely meant 寒武 (Cambricon)"),
    ("谛79", "likely meant 纪 (third char of 寒武纪)"),
    ("谛\\d", "Chinese char 谛 followed by digit — suspected escape drift"),
    # Finance line-item case (净利 / 财务 / 亏损 → 洁利 / 贜务 / 贜损 observed)
    ("洁利", "likely meant 净利 (net profit)"),
    ("贜务", "likely meant 财务 (financial)"),
    ("贜损", "likely meant 亏损 (loss)"),
    ("贜", "rare character 贜; in banker prose almost always a typo"),
    # Market case (核心 / 加速 → 校虚 observed)
    ("校虚", "likely meant 核心 or 加速 (market adj)"),
    # Catalyst case (催化剂 → 催化济 observed — last char shifted)
    ("催化济", "probably intended 催化剂 — last char shifted"),
    # --- 2nd batch: also observed in the same 2026-04-18 Cambricon deck ---
    # 转化 → 转映 observed ("转换成本转映软件")
    ("转映", "likely meant 转化 (conversion)"),
    # 艾瑞 / 艾媒 → 艺瑞 observed ("艺瑞咨询 2024")
    ("艺瑞", "likely meant 艾瑞 or 艾媒 (market research firm)"),
    # 产品 → 棒品 observed ("AI校虚国产化棒品")
    ("棒品", "likely meant 产品"),
    # 调试 → 调诚 observed ("需6-12个月调诚Loop")
    ("调诚", "likely meant 调试 (debug/tuning)"),
]

# Generic patterns that signal broken escape sequences
# 1. Chinese ideograph directly followed by a digit is extremely rare in
#    banker prose (numbers are typically surrounded by digits/units), and is
#    the classic symptom of a `\\uXXXX` truncation where the closing digits
#    of the escape got parsed as literal text.
RE_HANZI_THEN_DIGIT = re.compile(r"[\u4e00-\u9fff][0-9]")
# Year-like digit runs (19xx/20xx) right after a hanzi are almost never an
# escape drift — escape drift produces random digit tails, not coherent
# 4-digit years. Gate below: if the hit's trailing digit sequence starts
# with 19XX or 20XX, treat as benign.
RE_YEAR_TAIL = re.compile(r"(19|20)\d{2}")

# 2. CJK Compatibility / rare CJK-Extension chars that should not appear in
#    banker deliverables. A simple hit on U+3400-U+4DBF (CJK Extension A) or
#    U+20000+ (Extension B/C/D) is almost always a corruption indicator.
RE_RARE_CJK = re.compile(r"[\u3400-\u4dbf]|[\U00020000-\U0002ffff]")


def scan(text: str) -> list[tuple[int, str, str]]:
    """Return list of (line_no, matched_snippet, reason)."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for dyad, reason in RED_FLAG_DYADS:
            if re.search(dyad, line):
                hits.append((lineno, line.strip()[:120], f"red-flag dyad '{dyad}': {reason}"))
        for m in RE_HANZI_THEN_DIGIT.finditer(line):
            # allow a few benign patterns: 年份数字, 百分比, unit-attached numbers
            # e.g. "2024年" is hanzi-after-digit, not digit-after-hanzi. the
            # pattern only fires hanzi→digit, which is the suspicious direction.
            ctx = line[max(0, m.start() - 5):m.end() + 5]
            # Whitelist chars that are legitimately followed by a digit in
            # banker prose. Every character here should be evaluated as
            # "would a 2024-era banker deck ever write this char + a digit
            # literally, without it being an escape-drift typo?" Keep this
            # list conservative and add to it only when a real deliverable
            # produces a clear false-positive. See per-group comments below
            # for semantics + real-world examples.
            WHITELIST_LEADS = (
                # measure / count qualifiers
                "第共计超约近多"
                # banker line-item leads (营收 净利 股价 市值 毛利率 …)
                "营收净利股价市值毛利率润流"
                # sector / industry leads
                "白酒消费科技金融家电食品医药奢"
                # known-brand leads (茅台 五粮 泸州 洋河 海天 伊利 美的 格力)
                "茅台五粮泸州洋河海天伊利美的格力"
                # frequent CN-text + number joiners observed in banker prose:
                #   产 (年产/产 X 万吨), 破 (突破 X 亿), 液 (五粮液 1618 product-id),
                #   能 (产能 X 万吨), 为 (为 2024-xx), 前 (前 X 名),
                #   后 (后 X 年), 年/月/日 (年营收 X 亿 / 月产 X 万),
                #   含 (含税 X 元)
                "产破液能为前后年月日含"
                # misc nouns that legitimately precede digits
                "窖红额于指居金应在间售"
                # frequency / ordinal / proportion qualifiers
                "高中低同环比首半全三四两"
                # verbs that legitimately precede digits in banker prose:
                #   续 (连续 14 年), 受 (受 2022 年疫情), 达 (毛利率达 53%),
                #   至 (下降至 38.3 亿 / 恢复至 73.6 亿), 破 (already above),
                #   增 (同比增 17%), 达到/到 (达到 X / 增长到 Y), 逾 (逾 100 亿),
                #   过 (超过 X 亿 / 不过 X%), 仅 (仅 3%), 约 (already above),
                #   计 (共计 already as 共), 期 (期内 3Q), 降 (下降 X%),
                #   减 (减 X%), 涨 (上涨 X%), 跌 (下跌 X%),
                #   有 (有 X 家 / 具有 X), 下 (下滑 3% — 下 can be noun 'down')
                "续受达至到增逾过仅期降减涨跌有下"
                # CN address terms legitimately followed by digits (2026-04:
                # PrimeMatrix returns 注册住所 like "北京市朝阳区酒仙桥路10号";
                # 路/号/区/街/层/座/室/楼/栋/院/门/馆 all naturally meet a digit)
                "路号区街层座室楼栋院门馆"
                # State-of-the-business verbs: 保持 X%/增长（持 as in 保持 X%），
                # 支持 X 亿 — 持 legitimately precedes a digit in banker prose.
                "保持"
                # Quantifiers and scope words that legitimately precede digits:
                # 全部 12 个季度, 第 3 部, 一部 1000 亿
                "部"
                # More banker-prose leads found in 0.9.5→0.9.6 runs: common
                # prepositions / nouns / business verbs that commonly sit
                # before a digit in CN sell-side text. Each is low-risk for
                # escape-drift (the known MiniMax escape corruption produces
                # rare-character sequences, not normal prose chars).
                "从本损是矿业项期内上下左右前后次旁"
                "资本金额度值率比利息本期末初"
                "元收入利润成长增长盈亏销售毛"
                # foreign brand heads
                "LVMH"
            )
            if m.group(0)[0] in WHITELIST_LEADS:
                continue
            # Year-tail guard: if the digit starts a 4-digit year sequence
            # (e.g. "增速2024E" / "受2022年"), treat as legitimate year
            # reference rather than escape drift.
            tail = line[m.start() + 1:m.start() + 5]
            if RE_YEAR_TAIL.match(tail):
                continue
            hits.append((lineno, ctx.strip()[:120], f"hanzi-then-digit '{m.group(0)}' — escape drift suspect"))
        for m in RE_RARE_CJK.finditer(line):
            hits.append((lineno, line.strip()[:120], f"rare CJK char U+{ord(m.group(0)):04X}"))
    return hits


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: cn_typo_scan.py <text-file>", file=sys.stderr)
        return 2
    p = pathlib.Path(argv[1])
    if not p.exists():
        print(f"file not found: {p}", file=sys.stderr)
        return 2
    text = p.read_text(encoding="utf-8", errors="replace")
    hits = scan(text)
    if not hits:
        print(f"OK: cn_typo_scan clean on {p} ({len(text):,} chars)")
        return 0
    print(f"FAIL: {len(hits)} typo red-flag hit(s) in {p}", file=sys.stderr)
    for lineno, snippet, reason in hits[:80]:
        print(f"  L{lineno:>4}: {reason}", file=sys.stderr)
        print(f"         {snippet!r}", file=sys.stderr)
    if len(hits) > 80:
        print(f"  ...and {len(hits) - 80} more hits truncated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
