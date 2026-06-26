#!/usr/bin/env python3
"""
Pass 1: Claim Extraction for docx-chapter Phase 5.
Extracts all verifiable factual claims from chapter.md, outputs structured JSON.

Aligns with citation-check v2 Claim Extraction Rules.
Usage:
    python3 extract_claims.py chapter.md claims_pass1.json
"""

import re
import json
import sys
from pathlib import Path
from typing import Optional

# ── Claim type patterns (regex-based pre-extraction) ──────────────────────────

# Attribution: "According to X...", "X et al. found...", "per X report..."
ATTRIBUTION_RE = re.compile(
    r'(?:'
    r'根据|据|按照|引用|参见|参考|援引|'
    r'[Aa]ccording\s+to|'
    r'[Pp]er\s+|'
    r'[Rr]eported\s+by|'
    r'[Ss]tated\s+by|'
    r'[Nn]oted\s+by|'
    r'[Ff]ound\s+by|'
    r'[Pp]ublished\s+by'
    r')\s*.{3,120}?(?:[。.!?;；]|$)'
)

# Statistics: number + unit/context pattern
STATISTIC_RE = re.compile(
    r'(?:'
    r'\d+(?:\.\d+)?\s*%|'                          # 百分比
    r'\$\d+(?:\.\d+)?\s*(?:[万亿]|[BMKTQbmktq]|billion|million|thousand)?|'  # 金额
    r'\d+(?:\.\d+)?\s*(?:亿|万|千|百|[BMKTQbmktq]|billion|million|thousand)?\s*(?:美元|元|人民币|美金)?|'  # 中文金额
    r'\d+(?:\.\d+)?%\s*(?:的|of)?\s*\S+|'           # xx% of ...
    r'(?:超过|达到|增长|下降|减少|上升|提高|降低|占比|覆盖|拥有|约|大约|近|超过)\s*\d+(?:\.\d+)?|'  # 中文数字前缀
    r'\d+(?:\.\d+)?\s*(?:倍|次|个|项|家|条|人|用户|客户|企业)'  # 中文量词
    r')'
)

# Comparative: X is [comparative] than Y
COMPARATIVE_RE = re.compile(
    r'(?:'
    r'比\S{1,20}(?:更|还|还要|要|快|高|大|多|少|低|小|强|弱|好|差)|'
    r'(?:更|还|还要|最|较为?|特别|尤其|显著|明显|大幅|急剧)\S{0,10}(?:快|高|大|多|少|低|小|强|弱|好|差|于|过|的)|'
    r'(?:higher|lower|faster|slower|better|worse|larger|smaller|more|less)\s+than|'
    r'\d+(?:\.\d+)?\s*(?:倍|x|X|times)\s*(?:faster|slower|better|more|higher|lower|cheaper|expensive|as\s+\S+)|'
    r'(?:优于|劣于|好于|差于|高于|低于|大于|小于|超过|不及|领先|落后)'
    r')'
)

# Temporal: time-bound assertion
TEMPORAL_RE = re.compile(
    r'(?:'
    r'(?:19|20)\d{2}\s*年(?:\s*(?:第[一二三四]季度|[上下]半年|初|末|底))?|'
    r'(?:in|since|by|before|after|during)\s+(?:19|20)\d{2}|'
    r'(?:19|20)\d{2}\s*(?:年|\.|年)?\s*(?:以来|以后|以前|以来|开始|起|之际|至今)?|'
    r'自\s*(?:19|20)\d{2}\s*年|'
    r'(?:19|20)\d{2}[-–—](?:19|20)\d{2}|'
    r'(?:Q[1-4]\s*(?:19|20)\d{2})|'
    r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+(?:19|20)\d{2}'
    r')'
)

# Ranking: position claims
RANKING_RE = re.compile(
    r'(?:'
    r'(?:最大|最小|最高|最低|最长|最短|最快|最慢|最热|最冷|最强|最弱|最好|最差|最优|最劣|顶级|一流|领先|首个|第一|首次|最先|最早|'
    r'首款|首例|首创|率先|第一个|第一位|第一名|第一代|第一名|'
    r'第[一二三四五六七八九十百千0-9]+(?:名|位|个|项|家|条|款)|'
    r'前\s*[0-9一二三四五]+(?:名|位|个|项|家)|'
    r'[Tt]op\s*\d+|'
    r'largest|smallest|highest|lowest|fastest|slowest|first|leading|pioneering|'
    r'foremost|premier|unprecedented|groundbreaking)'
    r')'
)

# Causal: X causes/leads to/results in Y
CAUSAL_RE = re.compile(
    r'(?:'
    r'(?:导致|引起|造成|引发|触发|促使|推动|带动|驱动|使得|有助于|有利于|促进|改善|改善|提升|降低|减少|增加|提高|加强|增强|'
    r'削弱|阻碍|抑制|防止|避免|预防|消除|解决|缓解|减轻|'
    r'因为|由于|因此|所以|从而|进而|因而|以此|由此|'
    r'这\S{0,5}(?:使|让|令|致|导致|引起|造成)|'
    r'其\S{0,5}(?:使|让|令|致|导致|引起|造成)|'
    r''
    r'so\s+that|such\s+that|therefore|thus|hence|consequently|as\s+a\s+result|'
    r'leads?\s+to|results?\s+in|causes?|triggers?|enables?|facilitates?|'
    r'promotes?|improves?|reduces?|increases?|enhances?|prevents?|avoids?'
    r'))'
)

# Existence: asserts something exists/is true
EXISTENCE_RE = re.compile(
    r'(?:'
    r'(?:存在|拥有|具备|具有|有|含|包含|包括|涵盖|覆盖|涉及|'
    r'支持|兼容|适用|适合|适用于|可用于|可用于|'
    r'采用|使用|利用|运用|应用|引入|导入|集成|整合|融入|'
    r'部署|实施|执行|运行|操作|管理|控制|'
    r'(?:有|拥有|具备|具有|存在)\s*\d+(?:\.\d+)?\s*(?:亿|万|千|百|[BMKTQbmktq])?\s*(?:个|项|家|条|人|用户|客户|企业|件|台|部|辆|次)|'
    r'there\s+(?:is|are|exists?)|'
    r'(?:supports?|includes?|covers?|features?|enables?|provides?|offers?|delivers?|contains?)'
    r'))'
)

# Quote: direct quotation
QUOTE_RE = re.compile(
    r'["""\u201c\u201d](.{8,200}?)["""\u201c\u201d]|'
    r'\u300c(.{8,200}?)\u300d'
)

# ── Patterns to EXCLUDE (not claims) ─────────────────────────────────────────

EXCLUDE_PATTERNS = [
    # Definitions
    re.compile(r'(?:是指|定义为|即|所谓|指的是|的含义是|的概念是|is\s+defined\s+as|refers?\s+to|means?)'),
    # Opinions
    re.compile(r'(?:我们认为|笔者认为|本文认为|作者认为|在我看来|we\s+believe|in\s+our\s+view|we\s+think)'),
    # Hypotheticals
    re.compile(r'(?:如果|假如|假设|倘若|若|如果\S*的话|if\s+|assuming|suppose|would\s+be|could\s+be|might\s+be|potentially)'),
    # Questions
    re.compile(r'[？?]$'),
    # Methodology
    re.compile(r'(?:我们(?:采用|使用|利用|运用|应用|基于|借助|通过|按照|根据|按照|遵循|运用|实施)|'
               r'we\s+(?:used?|employed?|applied?|adopted?|utilized?|leveraged?|implemented?|conducted?|performed?))'),
    # Acknowledgments
    re.compile(r'(?:感谢|致谢|鸣谢|acknowledg|thanks?\s+to)'),
]

FOOTNOTE_MARKER_RE = re.compile(r'\[\^(\d+)\]')


def is_excluded(sentence: str) -> bool:
    """Check if a sentence should be excluded from claim extraction."""
    for pat in EXCLUDE_PATTERNS:
        if pat.search(sentence):
            return True
    return False


def classify_claim(text: str) -> Optional[str]:
    """Classify a claim text into one of the 8 types."""
    scores = {}
    if ATTRIBUTION_RE.search(text):
        scores["Attribution"] = ATTRIBUTION_RE.search(text).group(0).count(' ') + 1
    if STATISTIC_RE.search(text):
        scores["Statistic"] = STATISTIC_RE.search(text).group(0).count(' ') + 1
    if COMPARATIVE_RE.search(text):
        scores["Comparative"] = 1
    if TEMPORAL_RE.search(text):
        scores["Temporal"] = 1
    if RANKING_RE.search(text):
        scores["Ranking"] = 1
    if CAUSAL_RE.search(text):
        scores["Causal"] = 1
    if EXISTENCE_RE.search(text):
        scores["Existence"] = 1
    if QUOTE_RE.search(text):
        scores["Quote"] = 1

    if not scores:
        return None

    # Return highest-scoring type
    return max(scores, key=scores.get)


def extract_claims(text: str) -> list[dict]:
    """Extract claims from full chapter markdown text.

    Returns list of {claim_id, text, claim_type, location, footnote_ids}
    """
    # Split off footnote definitions section
    parts = re.split(r'\n##\s*脚注\s*\n', text, maxsplit=1)
    body = parts[0]

    # Split body into sentences
    sentences = re.split(r'(?<=[。.!?;；\n])\s*', body)

    claims = []
    claim_idx = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent or len(sent) < 10:
            continue
        # Skip headings (#, ##, ###, etc.)
        if re.match(r'^#{1,6}\s', sent):
            continue
        # Skip horizontal rules, code blocks
        if re.match(r'^[-*_]{3,}|^```|^>', sent):
            continue
        # Skip footnote definitions
        if sent.startswith('[^'):
            continue

        # Check exclusion patterns
        if is_excluded(sent):
            continue

        # Classify
        claim_type = classify_claim(sent)
        if claim_type is None:
            continue

        # Find footnote markers in this sentence
        footnotes = FOOTNOTE_MARKER_RE.findall(sent)

        claims.append({
            "claim_id": f"C{claim_idx:03d}",
            "text": sent,
            "claim_type": claim_type,
            "footnote_ids": footnotes,
        })
        claim_idx += 1

    return claims


def main():
    if len(sys.argv) < 3:
        print("Usage: extract_claims.py <chapter.md> <output.json>", file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    output_path = sys.argv[2]

    if not Path(md_path).exists():
        print(f"Error: {md_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(md_path, 'r') as f:
        text = f.read()

    claims = extract_claims(text)

    # Statistics
    type_counts = {}
    for c in claims:
        t = c["claim_type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    result = {
        "source": str(Path(md_path).resolve()),
        "pass": "Pass 1 — Claim Extraction",
        "total_claims": len(claims),
        "type_distribution": type_counts,
        "claims": claims,
        "note": "Claims flow directly to Pass 2 without human confirmation (per skill design).",
    }

    with open(output_path, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(claims)} claims → {output_path}")
    for t, n in sorted(type_counts.items()):
        print(f"  {t}: {n}")


if __name__ == "__main__":
    main()
