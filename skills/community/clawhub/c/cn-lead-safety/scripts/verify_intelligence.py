#!/usr/bin/env python3
"""
verify_intelligence.py — lead-discovery intelligence markdown gate.

Scans a generated banker intelligence .md and enforces Rule 4 of
`cn-lead-safety`: every hard number (digit + banker unit) must have an
inline source citation within the same line or the immediately-following
line.

Usage:
    python3 verify_intelligence.py <intelligence.md>
    python3 verify_intelligence.py --strict-mcp <intelligence.md>

    # exit 0 → every hard number has citation (and, under --strict-mcp, the
    #          citation matches an MCP tool or an official-filing anchor)
    # exit 1 → one or more hard numbers lack citation (default mode)
    # exit 1 → or, under --strict-mcp, one or more citations fall back to
    #          forbidden fabricated sources (Wind / 同花顺 / 万得) or to
    #          non-authoritative media

"Hard number" uses the same pattern as the downstream financial-services
provenance_verify.py:  digits (optional thousands commas + decimal) + one
of the banker units 亿 / 万 / % / 元 / 亿元 / RMB / USD / CNY / HKD / M / B.

Strict-MCP mode (0.8.0+): added after MiniMax-host deliverables were
found citing "Wind (2026-04-17)" and "同花顺 F10" as sources even though
neither is an installed MCP or accessible tool on macmini. Under
--strict-mcp the gate demands every hard number cite ONE of:
    - an aigroup-market-mcp / PrimeMatrixData / Tianyancha tool anchor, OR
    - an official-filing URL (cninfo / sse / szse / hkex / gsxt / sec), OR
    - an exchange/issuer announcement anchor (巨潮 / 上交所 / 深交所 / 港交所 / 招股书 / 年报 / 季报)
Media-only citations (财新 / 新浪财经 / 21世纪 / …) still pass default mode
but FAIL --strict-mcp for hard numbers (they are acceptable for prose).
"""
from __future__ import annotations
import argparse
import re
import sys
import pathlib

UNITS = r"(?:亿元|亿|万|%|元|RMB|USD|CNY|HKD|M|B)"
NUM_CORE = r"\d+(?:,\d{3})*(?:\.\d+)?"
HARD_NUMBER = re.compile(rf"({NUM_CORE})\s*({UNITS})")

# MCP-tool anchors — any of these prefixes in the citation window means
# the hard number is sourced from an installed, auditable MCP tool call.
# These are REQUIRED (in addition to official-filing or exchange anchors)
# under --strict-mcp.
MCP_TOOL_ANCHORS = (
    "aigroup-market-mcp",
    "PrimeMatrixData",
    "Tianyancha",
)

# Official filing / exchange anchors — authoritative primary sources.
# Pass both default and --strict-mcp.
OFFICIAL_ANCHORS = (
    "招股书", "年报", "季报", "半年报", "中报",  # 中报 = interim report (semi-annual)
    "公司公告", "公司公告/", "公告",
    "巨潮", "cninfo", "CNINFO",
    "上交所", "深交所", "港交所", "SSE", "SZSE", "HKEX",
    "国家企业信用", "gsxt.gov.cn", "gsxt",
    "sec.gov", "EDGAR",  # retained for HK/US overlay even in CN-primary gate
    "招股说明书", "募集说明书",
    "http://", "https://",
)

# Media / portal anchors — acceptable in default mode for contextual
# prose, but insufficient for hard numbers under --strict-mcp. 2026-04
# multi-company real-test showed MiniMax citing "Wind" and "同花顺" for
# market data, which are NOT installed tools — these are now in
# FORBIDDEN_ANCHORS and will FAIL --strict-mcp for hard numbers.
MEDIA_ANCHORS = (
    "来源：", "来源:", "源：", "Source:", "source:",
    "据", "根据", "引自",
    "天眼查",  # when cited as website/media, not Tianyancha MCP
    "企查查",
    "东方财富", "Choice",
    "财新", "21世纪", "第一财经", "中证", "上证", "财联社", "澎湃",
    "新浪财经", "新浪", "sina.com.cn",
    "证券之星", "stockstar",
    "金融界", "jrj.com",
    "华尔街见闻", "wallstreetcn",
    "中国经济网", "国证",
    "中国基金报", "chnfund",
    "界面新闻", "jiemian",
    "中鹏信评", "中诚信", "联合资信", "大公国际",
    "上海证券报", "证券日报", "证券时报",
    "雪球", "xueqiu",
    "派财经", "时代周报",
    "[^",
)

# Forbidden-source anchors — these appeared in MiniMax-hallucinated
# 2026-04-19 BYD / 2026-04-20 Midea & Ping An deliverables as source
# labels even though the underlying tools are NOT installed on macmini
# (Wind is a paid institutional terminal; 同花顺 F10 is not an MCP).
# Default mode warns; --strict-mcp fails.
FORBIDDEN_ANCHORS = (
    # Substring matches — "同花顺" covers "同花顺 F10" / "同花顺F10";
    # "Wind" covers "Wind (2026-04-17)".
    "Wind", "万得", "同花顺",
)

# Back-compat: legacy callers (provenance_verify / external tooling)
# may import CITATION_ANCHORS directly. Union of every non-forbidden
# anchor set, plus bare "Tushare" for decks that cite it without the
# full aigroup-market-mcp prefix.
CITATION_ANCHORS = (
    *MCP_TOOL_ANCHORS,
    *OFFICIAL_ANCHORS,
    *MEDIA_ANCHORS,
    "Tushare", "tushare",
)


def citation_window(line: str, next_line: str | None) -> str:
    return line + "\n" + (next_line or "")


def has_any(window: str, anchors: tuple[str, ...]) -> bool:
    return any(a in window for a in anchors)


def classify(window: str) -> str:
    """Return 'mcp' | 'official' | 'media' | 'forbidden' | 'none'."""
    if has_any(window, FORBIDDEN_ANCHORS):
        return "forbidden"
    if has_any(window, MCP_TOOL_ANCHORS):
        return "mcp"
    # Tushare cited without the aigroup-market-mcp prefix still traces to
    # the same installed tool — classify as mcp, not media.
    if "Tushare" in window or "tushare" in window:
        return "mcp"
    if has_any(window, OFFICIAL_ANCHORS):
        return "official"
    if has_any(window, MEDIA_ANCHORS):
        return "media"
    return "none"


def scan(text: str, strict_mcp: bool = False) -> list[tuple[int, str, str, str, str]]:
    """Return list of (line_no, number, unit, snippet, reason) failing the gate."""
    lines = text.splitlines()
    failures: list[tuple[int, str, str, str, str]] = []
    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else None
        window = citation_window(line, next_line)
        for m in HARD_NUMBER.finditer(line):
            verdict = classify(window)
            if verdict == "none":
                failures.append(
                    (i + 1, m.group(1), m.group(2),
                     line.strip()[:120], "no citation")
                )
            elif verdict == "forbidden":
                failures.append(
                    (i + 1, m.group(1), m.group(2),
                     line.strip()[:120],
                     "forbidden source (Wind/同花顺 not installed)")
                )
            elif strict_mcp and verdict == "media":
                failures.append(
                    (i + 1, m.group(1), m.group(2),
                     line.strip()[:120],
                     "media-only citation insufficient under --strict-mcp; "
                     "expected MCP tool or official filing")
                )
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument("intelligence_md", type=pathlib.Path)
    parser.add_argument(
        "--strict-mcp",
        action="store_true",
        help="require MCP-tool or official-filing citation for every hard number",
    )
    args = parser.parse_args(argv[1:])

    if not args.intelligence_md.exists():
        print(f"file not found: {args.intelligence_md}", file=sys.stderr)
        return 2

    text = args.intelligence_md.read_text(encoding="utf-8", errors="replace")
    failures = scan(text, strict_mcp=args.strict_mcp)

    total = sum(len(HARD_NUMBER.findall(line)) for line in text.splitlines())
    mode_label = "strict-mcp" if args.strict_mcp else "default"

    if not failures:
        print(
            f"OK: verify_intelligence [{mode_label}] clean on {args.intelligence_md} "
            f"({total} hard numbers, all with acceptable citation)"
        )
        return 0

    covered = total - len(failures)
    print(
        f"FAIL [{mode_label}]: {len(failures)} of {total} hard numbers failed "
        f"citation check in {args.intelligence_md}",
        file=sys.stderr,
    )
    for lineno, num, unit, snippet, reason in failures[:60]:
        print(
            f"  L{lineno:>4}: '{num}{unit}' — {reason}",
            file=sys.stderr,
        )
        print(f"         context: {snippet!r}", file=sys.stderr)
    if len(failures) > 60:
        print(f"  ...and {len(failures) - 60} more truncated.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
