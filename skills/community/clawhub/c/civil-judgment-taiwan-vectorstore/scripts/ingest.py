#!/usr/bin/env python3
"""Ingest Taiwan civil judgments (HTML or PDF) into Qdrant using Ollama embeddings.

v1 scope:
- Read a `judicialyuan-search` run folder
- Discover archived detail files under `<run_folder>/archive/*.html` and `*.pdf`
- Canonicalize HTML/PDF -> plain text (deterministic whitespace)
- Section split (rule-based headings)
- Section-aware chunking
- Embed via Ollama (`/api/embeddings`)
- Upsert into Qdrant collections:
    - civil_case_doc
    - civil_case_chunk
- Write local manifest + report

Notes:
- Raw HTML/PDF is treated as immutable source-of-truth.
- IDs are deterministic using sha256 of canonical plain text.

"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.http import models as qm


class PreflightError(RuntimeError):
    pass


DOC_COLLECTION = "civil_case_doc"
CHUNK_COLLECTION = "civil_case_chunk"

DEFAULT_VECTOR_SIZE = 1024
DEFAULT_DISTANCE = qm.Distance.COSINE


HEADING_SYNONYMS: List[Tuple[str, List[str]]] = [
    ("holding", ["主文"]),
    ("facts", ["事實", "事實及理由", "理由"]),  # some judgments merge headings
    ("claims", ["理由", "兩造", "當事人"]),
    ("reasoning", ["理由", "理由要旨"]),
    ("conclusion", ["結論", "綜上", "據上", "依據", "如主文"]),
]


@dataclass
class Chunk:
    section: str
    index: int
    text: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def normalize_whitespace(text: str) -> str:
    # Normalize newlines and spaces deterministically.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Remove trailing spaces per line
    text = "\n".join([ln.strip() for ln in text.split("\n")])
    # Collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse long runs of spaces/tabs
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def normalize_heading_token(text: str) -> str:
    """Normalize noisy PDF/OCR heading lines for section detection only."""
    if not text:
        return ""
    s = text.strip()
    compat_map = str.maketrans({
        "⽂": "文",
        "⺠": "民",
        "⽇": "日",
        "⽉": "月",
        "⽅": "方",
        "⾼": "高",
        "理": "理",
    })
    s = s.translate(compat_map)
    s = re.sub(r"[\s\u00A0\u1680\u180E\u2000-\u200F\u2028-\u202F\u205F\u3000]+", "", s)
    s = s.replace("：", ":")
    return s


def parse_roc_date_to_iso(s: str) -> Optional[str]:
    """Parse '民國 114 年 02 月 14 日' -> '2025-02-14'."""
    m = re.search(r"民國\s*(\d{2,3})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", s)
    if not m:
        return None
    y = int(m.group(1)) + 1911
    mo = int(m.group(2))
    d = int(m.group(3))
    return f"{y:04d}-{mo:02d}-{d:02d}"


def classify_court_tier_from_court(court: str) -> str:
    if not court:
        return "unknown"
    if "最高" in court:
        return "supreme"
    if "高等" in court or "智財" in court or "智慧財產" in court:
        return "high"
    if "地方法院" in court or "地院" in court or "地方" in court:
        return "district"
    return "other"


def extract_fields_from_int_table(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract metadata from the FJUD '.int-table' block.

    Observed pattern:
      裁判字號：<value>
      裁判日期：<value>
      裁判案由：<value>
    Followed by party lines (上訴人/被上訴人/原告/被告...).
    """
    out: Dict[str, Any] = {}
    tbl = soup.select_one('.int-table')
    if not tbl:
        return out

    txt = tbl.get_text("\n", strip=True)

    def grab(label: str) -> Optional[str]:
        # Capture text after 'label：' until next known label or end
        # Keep it simple and robust.
        pat = rf"{re.escape(label)}\s*：\s*(.*?)\n(?:裁判字號|裁判日期|裁判案由)\s*：|{re.escape(label)}\s*：\s*(.*)$"
        m = re.search(pat, txt, flags=re.S)
        if not m:
            return None
        v = m.group(1) or m.group(2)
        if not v:
            return None
        # If it includes trailing next label due to regex fallback, trim aggressively
        v = v.strip()
        v = v.split("\n裁判")[0].strip()
        return normalize_whitespace(v)

    case_no = grab("裁判字號")
    date_raw = grab("裁判日期")
    cause = grab("裁判案由")

    if case_no:
        out["case_no"] = case_no
    if date_raw:
        out["date_raw"] = date_raw
        iso = parse_roc_date_to_iso(date_raw)
        if iso:
            out["date"] = iso
    if cause:
        out["cause"] = cause

    # Parties (very heuristic): collect lines after the three header fields.
    # We'll store raw party block for now; later iterations can normalize roles.
    # Find the first occurrence of '上訴人'/'原告' etc.
    m = re.search(r"(上\s*訴\s*人|被\s*上\s*訴\s*人|原\s*告|被\s*告|聲\s*請\s*人|相\s*對\s*人).+", txt, flags=re.S)
    if m:
        parties_block = normalize_whitespace(m.group(0))
        out["parties_raw"] = parties_block

    return out


def html_to_text_and_meta(html: str, *, base_url: str = "https://judgment.judicial.gov.tw") -> Tuple[str, Dict[str, Any]]:
    soup = BeautifulSoup(html, "lxml")

    # Remove scripts/styles and hidden elements that tend to add noise.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Title
    title = ""
    if soup.title and soup.title.string:
        title = normalize_whitespace(soup.title.string)

    # Attempt to recover a canonical doc_url from <form action="...">
    doc_url = None
    form = soup.find("form")
    if form and form.get("action"):
        action = str(form.get("action"))
        if action.startswith("http"):
            doc_url = action
        else:
            # many pages use relative like ./data.aspx?... or /FJUD/data.aspx?...; normalize
            action = action.lstrip(".")
            if not action.startswith("/"):
                action = "/" + action
            doc_url = base_url.rstrip("/") + action

    # Extract readable text; use newline separator to preserve blocks
    text = soup.get_text("\n")
    text = normalize_whitespace(text)

    # Metadata extraction
    court = title.split()[0] if title else ""
    meta: Dict[str, Any] = {
        "title": title,
        "court": court,
        "court_tier": classify_court_tier_from_court(court),
        "doc_url": doc_url,
        **extract_fields_from_int_table(soup),
    }
    return text, meta


def extract_fields_from_plain_text(text: str) -> Dict[str, Any]:
    """Extract metadata from plain text (used for PDF files lacking HTML structure)."""
    out: Dict[str, Any] = {}

    m = re.search(r"裁判字號[：:]\s*([^\n\r]+)", text)
    if m:
        out["case_no"] = normalize_whitespace(m.group(1))

    m = re.search(r"裁判日期[：:]\s*([^\n\r]+)", text)
    if m:
        date_raw = normalize_whitespace(m.group(1))
        out["date_raw"] = date_raw
        iso = parse_roc_date_to_iso(date_raw)
        if iso:
            out["date"] = iso

    m = re.search(r"裁判案由[：:]\s*([^\n\r]+)", text)
    if m:
        out["cause"] = normalize_whitespace(m.group(1))

    m = re.search(r"(上\s*訴\s*人|被\s*上\s*訴\s*人|原\s*告|被\s*告|聲\s*請\s*人|相\s*對\s*人).+", text, flags=re.S)
    if m:
        out["parties_raw"] = normalize_whitespace(m.group(0))

    return out


def pdf_to_text_and_meta(path: Path) -> Tuple[str, Dict[str, Any]]:
    """Extract text and metadata from a PDF judgment file using pypdf."""
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        t = page.extract_text()
        if t:
            pages.append(t)
    text = normalize_whitespace("\n\n".join(pages))

    # Title: try PDF metadata first, fall back to first non-empty line
    title = ""
    pdf_meta = reader.metadata
    if pdf_meta and pdf_meta.title:
        title = normalize_whitespace(str(pdf_meta.title))
    if not title:
        first_lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
        title = first_lines[0] if first_lines else ""

    court = title.split()[0] if title else ""
    fields = extract_fields_from_plain_text(text)

    meta: Dict[str, Any] = {
        "title": title,
        "court": court,
        "court_tier": classify_court_tier_from_court(court),
        "doc_url": None,
        **fields,
    }
    return text, meta


def split_sections(plain_text: str) -> Dict[str, str]:
    """Heuristic section split.

    Conservative by default, but tolerant of PDF/OCR heading noise.
    """
    lines = [ln.strip() for ln in plain_text.split("\n")]
    lines = [ln for ln in lines if ln]

    normalized_synonyms = {
        section: {normalize_heading_token(s) for s in synonyms}
        for section, synonyms in HEADING_SYNONYMS
    }

    # Build indices of heading lines
    heading_positions: List[Tuple[int, str]] = []
    for i, ln in enumerate(lines):
        norm_ln = normalize_heading_token(ln)
        for section, _synonyms in HEADING_SYNONYMS:
            if norm_ln in normalized_synonyms[section]:
                heading_positions.append((i, section))
                break

    if not heading_positions:
        return {"full": "\n".join(lines)}

    # Keep first occurrence per section in order
    heading_positions.sort(key=lambda x: x[0])

    sections: Dict[str, List[str]] = {}
    for idx, (pos, section) in enumerate(heading_positions):
        start = pos + 1
        end = heading_positions[idx + 1][0] if idx + 1 < len(heading_positions) else len(lines)
        body = lines[start:end]
        if not body:
            continue
        sections.setdefault(section, []).extend(body)

    # Always keep full text too
    out = {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}
    out["full"] = "\n".join(lines)
    return out


def chunk_text(text: str, *, max_chars: int = 900, overlap_chars: int = 150) -> List[str]:
    """Simple CJK-friendly character chunker with overlap."""
    text = text.strip()
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(n, start + max_chars)
        chunk = text[start:end]
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = max(0, end - overlap_chars)
    return chunks


ISSUE_HEADING_PAT = re.compile(
    r"^(?:\s*)(爭點|爭點如下|爭點整理|爭點歸納|爭執事項|兩造爭執事項|本院認為爭點|本案爭點)(?:\s*)(：|:)?(?:\s*)$"
)

NOT_ISSUE_HEADING_PAT = re.compile(
    r"^(?:\s*)(不爭執事項|不爭執事項：|不爭執)(?:\s*)$"
)


def is_issue_heading_line(line: str) -> bool:
    """More tolerant heading detector.

    Many judgments write headings like '本件爭點如下：' or '爭點：' with extra words.
    We treat short lines containing '爭點'/'爭執事項' as headings.
    BUT: '兩造爭執事項' itself is NOT an issue - it's a heading that PRECEDES the actual issues.
    And '不爭執事項' is NEVER an issue (both parties agree on facts).
    """
    ln = normalize_whitespace(line)
    if not ln:
        return False

    # "不爭執事項" is NOT an issue block (skip it)
    if NOT_ISSUE_HEADING_PAT.match(ln):
        return False

    # "兩造爭執事項" itself is the heading, NOT an issue
    if ln.startswith("兩造爭執事項") and (ln == "兩造爭執事項" or len(ln) <= 16):
        return True  # treat as heading, but we will skip this line itself when extracting issues

    if ISSUE_HEADING_PAT.match(ln):
        return True
    if ("爭點" in ln or "爭執事項" in ln) and len(ln) <= 12:
        return True
    if ln.endswith("如下") and ("爭點" in ln) and len(ln) <= 14:
        return True
    return False
ISSUE_ITEM_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r"^([一二三四五六七八九十]+、)\s*(.+)$"),
    re.compile(r"^([(（]?[一二三四五六七八九十]+[)）])\s*(.+)$"),
    re.compile(r"^(\d+\.)\s*(.+)$"),
    re.compile(r"^([(（]?\d+[)）])\s*(.+)$"),
    re.compile(r"^(壹、|貳、|參、|肆、|伍、|陸、|柒、|捌、|玖、|拾、)\s*(.+)$"),
]

# Norms / citations (very lightweight v1): capture cited statutes / interpretations / circulars.
NORM_PATTERNS: List[re.Pattern[str]] = [
    re.compile(r"(?:民法|民事訴訟法|土地法|建築法|都市計畫法|國土計畫法|行政程序法|刑法|公司法|消費者保護法)[^。\n]{0,60}?第\s*\d+\s*條(?:之\s*\d+)?"),
    re.compile(r"(?:司法院)?釋字第\s*\d+\s*號"),
    re.compile(r"憲判字第\s*\d+\s*號"),
    re.compile(r"最高法院\s*\d+\s*年度[^\n。]{0,20}?字第\s*\d+\s*號"),
    re.compile(r"(?:內政部|財政部|法務部|司法院|行政院)[^\n。]{0,20}函"),
]


def extract_norms(text: str, *, max_items: int = 50) -> List[str]:
    if not text:
        return []
    hits: List[str] = []
    for pat in NORM_PATTERNS:
        for m in pat.finditer(text):
            s = normalize_whitespace(m.group(0))
            if s:
                hits.append(s)
    # de-dup
    seen=set(); out=[]
    for h in hits:
        if h in seen:
            continue
        seen.add(h)
        out.append(h)
        if len(out) >= max_items:
            break
    return out


def extract_fact_reason_snippets(text: str, *, window: int = 2, max_snippets: int = 60) -> List[str]:
    """Extract court-important fact/reason paragraphs.

    Per Sean feedback, paragraphs starting with '查/經查/惟查' often contain
    key facts and reasoning steps.

    This function uses sentence-based splitting (by "。" - Chinese period) to ensure
    snippets include full sentences.

    Returns list of snippet strings.
    """
    if not text:
        return []

    # Split by sentence delimiter (。) - this is crucial for the new rule
    sentences: List[str] = []
    current = ""
    for ch in text:
        current += ch
        if ch == "。":
            s = current.strip()
            if s:
                sentences.append(s)
            current = ""
    if current.strip():
        sentences.append(current.strip())

    if not sentences:
        return []

    def is_party_assertion(s: str) -> bool:
        s = s.strip()
        return s.endswith("等語") or s.endswith("等語。") or s.endswith("等語，")

    def is_prior_court_citation(s: str) -> bool:
        """Sentences starting with '原審以' are prior court opinions, skip."""
        s = s.strip()
        return s.startswith("原審以") or s.startswith("原審認") or s.startswith("原審為")

    out: List[str] = []
    seen = set()
    for i, sent in enumerate(sentences):
        if is_party_assertion(sent):
            continue
        if is_prior_court_citation(sent):
            continue

        if not (sent.startswith("查") or sent.startswith("經查") or sent.startswith("惟查")):
            continue

        # Expand to include surrounding sentences (full sentences up to periods)
        lo = max(0, i - window)
        hi = min(len(sentences), i + window + 1)
        context_parts = []
        for j in range(lo, hi):
            s = sentences[j]
            if not is_party_assertion(s) and not is_prior_court_citation(s):
                context_parts.append(s)
        snippet = normalize_whitespace("。".join(context_parts))
        if not snippet:
            continue
        if snippet in seen:
            continue
        seen.add(snippet)
        out.append(snippet)
        if len(out) >= max_snippets:
            break
    return out


def extract_norm_snippets(text: str, *, window: int = 1, max_snippets: int = 40, include_norm_only_paras: bool = True) -> List[Dict[str, str]]:
    """Extract reasoning snippets around cited norms.

    Output schema (list of dicts):
      {"norm": <matched norm string>, "snippet": <context lines>}

    Heuristics (per Sean feedback):
    - If sentence ends with '定有明文' or '判決意旨參照' or '判決參照',
      EXPAND BACKWARDS to include full norm statement (until previous period).
    - If sentence ends with '定有明文' AND next sentence starts with '又',
      EXPAND FORWARDS to include next sentence too.
    - Paragraphs ending with '等語' are usually parties' assertions, skip.
    """
    if not text:
        return []

    # Split by sentence delimiter (。) - this is crucial for the new rules
    sentences: List[str] = []
    current = ""
    for ch in text:
        current += ch
        if ch == "。":
            s = current.strip()
            if s:
                sentences.append(s)
            current = ""
    if current.strip():
        sentences.append(current.strip())

    if not sentences:
        return []

    def is_party_assertion(s: str) -> bool:
        s = s.strip()
        return s.endswith("等語") or s.endswith("等語。") or s.endswith("等語，")

    def is_prior_court_citation(s: str) -> bool:
        """Check if sentence is citing a prior court's opinion (should be excluded from norms/reasons).

        Per Sean feedback: sentences starting with '原審以' are just repeating the lower court's view,
        not the current court's own reasoning.
        """
        s = s.strip()
        return s.startswith("原審以") or s.startswith("原審認") or s.startswith("原審為")

    def sentence_ends_with_norm_keyword(s: str) -> bool:
        s = s.strip()
        return s.endswith("定有明文") or s.endswith("定有明文。") or "判決意旨參照" in s or "判決參照" in s

    snippets: List[Dict[str, str]] = []
    seen = set()

    for i, sent in enumerate(sentences):
        if is_party_assertion(sent):
            continue
        # Per Sean: sentences starting with '原審以' are prior court opinions, not current court's reasoning
        if is_prior_court_citation(sent):
            continue

        norms_in_sent: List[str] = []
        for pat in NORM_PATTERNS:
            for m in pat.finditer(sent):
                n = normalize_whitespace(m.group(0))
                if n:
                    norms_in_sent.append(n)

        # If no explicit norm found but ends with 定有明文, treat as norm
        if not norms_in_sent and include_norm_only_paras:
            if sent.endswith("定有明文") or sent.endswith("定有明文。"):
                norms_in_sent = ["(定有明文)"]

        if not norms_in_sent:
            continue

        # Per Sean's rules: expand to full norm statement
        # Rule 1: If ends with 定有明文/判決意旨參照, expand BACKWARDS
        lo_idx = i
        if sentence_ends_with_norm_keyword(sent):
            # go backwards to include full norm statement
            while lo_idx > 0:
                prev_sent = sentences[lo_idx - 1]
                if any(prev_sent.startswith(kw) for kw in ["按", "次按", "又", "本院", "依"]):
                    lo_idx -= 1
                elif "。" not in prev_sent:
                    lo_idx -= 1
                else:
                    break

        # Rule 2: If ends with 定有明文 AND next starts with 又, expand FORWARDS
        hi_idx = i + 1
        if sent.endswith("定有明文") or sent.endswith("定有明文。"):
            if hi_idx < len(sentences):
                next_sent = sentences[hi_idx]
                if next_sent.strip().startswith("又"):
                    hi_idx += 1

        # Build the expanded snippet
        snippet_parts = sentences[lo_idx:hi_idx]
        filtered_parts = [p for p in snippet_parts if not is_party_assertion(p)]
        snippet = normalize_whitespace("。".join(filtered_parts))
        if not snippet:
            continue

        for n in norms_in_sent:
            key = (n, snippet[:200])
            if key in seen:
                continue
            seen.add(key)
            snippets.append({"norm": n, "snippet": snippet})
            if len(snippets) >= max_snippets:
                return snippets

    return snippets


REASONING_CUE_PATTERNS = [
    "是故",
    "因此",
    "準此",
    "可見",
    "由此可見",
    "即應",
    "爰依",
    "自應",
    "從而",
    "甚是",
    "茲因",
    "是則",
    "應認",
    "所以",
    "顯見",
    "顯然",
    "必然",
]


COURT_REASONING_HEADERS = [
    "本院之判斷",
    "本院判斷",
    "本院理由",
    "本院認為",
    "得心證之理由",
    "得心證理由",
    "法院之判斷",
    "兩造爭執事項",
    "經查：",
    "茲分述如下",
    "茲分述如下：",
]


def find_court_reasoning_start(text: str) -> int:
    """Find the start position of court reasoning section in text.

    Headers to look for:
    - 本院（之）判斷 / 本院理由 / 本院認為
    - 得心證（之）理由
    - 兩造爭執事項
    - 經查：
    - 茲分述如下 / 茲分述如下：

    Returns the character index where reasoning starts, or 0 if not found.
    """
    if not text:
        return 0

    lines = text.split("\n")
    for i, ln in enumerate(lines):
        stripped = ln.strip()
        if not stripped:
            continue
        for header in COURT_REASONING_HEADERS:
            # Allow ordinal prefixes like "三、本院之判斷："
            if (
                stripped == header
                or stripped.startswith(header + "：")
                or stripped.startswith(header + ":")
                or stripped.startswith(header + " ")
                or (header in stripped and len(stripped) <= 30)
            ):
                pos = text.find(ln)
                if pos != -1:
                    return pos
                pos = text.find("\n" + ln)
                if pos != -1:
                    return pos + 1
    return 0


def extract_reasoning_snippets(text: str, *, max_snippets: int = 30) -> List[Dict[str, str]]:
    """Extract court's subsumption reasoning (涵攝推理) sentences.

    Per Sean: the core of court's reasoning is the logical process of:
    1) identifying the norm (大前提)
    2) confirming facts (小前提)
    3) applying facts to norm to derive legal effect (涵攝)

    This function extracts sentences that contain reasoning cue patterns like
    '是故', '因此', '準此', '爰依', '自應', '從而', etc.

    Returns list of dicts: {"cue": <keyword found>, "snippet": <sentence with context>}
    """
    if not text:
        return []

    # Split by sentence delimiter (。)
    sentences: List[str] = []
    current = ""
    for ch in text:
        current += ch
        if ch == "。":
            s = current.strip()
            if s:
                sentences.append(s)
            current = ""
    if current.strip():
        sentences.append(current.strip())

    if not sentences:
        return []

    def is_party_assertion(s: str) -> bool:
        s = s.strip()
        return s.endswith("等語") or s.endswith("等語。") or s.endswith("等語，")

    def is_prior_court_citation(s: str) -> bool:
        s = s.strip()
        return s.startswith("原審以") or s.startswith("原審認") or s.startswith("原審為")

    def has_reasoning_cue(s: str) -> str:
        s = s.strip()
        for cue in REASONING_CUE_PATTERNS:
            if cue in s:
                return cue
        return ""

    snippets: List[Dict[str, str]] = []
    seen = set()

    for i, sent in enumerate(sentences):
        if is_party_assertion(sent):
            continue
        if is_prior_court_citation(sent):
            continue

        cue = has_reasoning_cue(sent)
        if not cue:
            continue

        # Include some context: reasoning sentence + surrounding sentences
        lo = max(0, i - 1)
        hi = min(len(sentences), i + 2)
        context_parts = []
        for j in range(lo, hi):
            s = sentences[j]
            if not is_party_assertion(s) and not is_prior_court_citation(s):
                context_parts.append(s)
        snippet = normalize_whitespace("。".join(context_parts))

        key = (cue, snippet[:150])
        if key in seen:
            continue
        seen.add(key)
        snippets.append({"cue": cue, "snippet": snippet})
        if len(snippets) >= max_snippets:
            break

    return snippets


def extract_candidate_issues(reasoning_text: str, *, max_issues: int = 30, min_len: int = 6) -> List[str]:
    """Extract candidate issues from reasoning text (M2).

    Heuristic approach (v1.3):
    - Prefer an explicit issue heading block (e.g., '爭點') and capture numbered items following it.
    - Fallback: scan reasoning for numbered-item lines, but apply aggressive anti-主文/聲明 filters.

    Returns a de-duplicated list (order-preserving).
    """
    if not reasoning_text:
        return []

    lines = [ln.strip() for ln in reasoning_text.split("\n") if ln.strip()]
    if not lines:
        return []

    bad_pat = re.compile(
        r"(訴訟費用|假執行|供擔保|如主文|主文|撤銷|駁回|准許|不受理|移送|本訴部分|反訴部分|上訴費用|第一審|第二審|原判決|執行|清償|給付|確認原告|確認被告|被告應|原告應|上訴人|被上訴人)"
    )
    cue_pat = re.compile(r"(是否|應否|得否|可否|有無|能否|要件|成立|不成立|應負|應負擔|得請求|得主張|得否請求)")
    impossible_prefixes = [
        "經查",
        "按",
        "次按",
        "至關於",
        "查",
        "考量",
        "綜上",
        "據上",
        "又",
        "末按",
    ]

    def ok_issue(s: str, *, require_cue: bool) -> bool:
        s = normalize_whitespace(s)
        if not s:
            return False
        if len(s) < min_len:
            return False
        # user-provided: these paragraph openers are almost never 'issues'
        for pfx in impossible_prefixes:
            if s.startswith(pfx):
                return False
        # exclude obvious 主文/聲明 fragments
        if bad_pat.search(s):
            return False
        # Without an explicit '爭點' heading, numbered lines are usually facts/arguments;
        # require issue cue-words to improve precision.
        if require_cue and not cue_pat.search(s):
            return False
        return True

    # Prefer content right after an '爭點' heading if present.
    start_idx = 0
    for i, ln in enumerate(lines):
        if is_issue_heading_line(ln):
            start_idx = i + 1
            break

    cands: List[str] = []
    found_heading = start_idx != 0

    # Strategy 2 (coverage-first):
    # - If explicit issue heading exists, do NOT require cue words.
    # - If no heading, keep cue-word requirement.
    for ln in lines[start_idx:]:
        # stop early if we hit another major heading
        if ln in {"主文", "事實", "事實及理由", "理由", "結論"}:
            break
        for pat in ISSUE_ITEM_PATTERNS:
            m = pat.match(ln)
            if m:
                issue = normalize_whitespace(m.group(2))
                if ok_issue(issue, require_cue=(not found_heading)):
                    cands.append(issue)
                break
        if len(cands) >= max_issues:
            break

    # Fallback: scan all lines if nothing found.
    if not cands:
        for ln in lines:
            for pat in ISSUE_ITEM_PATTERNS:
                m = pat.match(ln)
                if m:
                    issue = normalize_whitespace(m.group(2))
                    if ok_issue(issue, require_cue=True):
                        cands.append(issue)
                    break
            if len(cands) >= max_issues:
                break

    # De-dup while preserving order
    seen = set()
    out: List[str] = []
    for x in cands:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return out


def ollama_embed(texts: List[str], *, ollama: str, model: str, timeout: int = 60) -> List[List[float]]:
    """Embed texts via Ollama /api/embeddings.

    Ollama endpoint: http://host:11434
    """
    url = ollama.rstrip("/") + "/api/embeddings"
    vecs: List[List[float]] = []
    for t in texts:
        r = requests.post(url, json={"model": model, "prompt": t}, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        emb = data.get("embedding")
        if not isinstance(emb, list):
            raise RuntimeError(f"Unexpected Ollama response: {data}")
        vecs.append(emb)
    return vecs


def ensure_collection(client: QdrantClient, name: str, *, vector_size: int, distance: qm.Distance) -> None:
    exists = False
    try:
        client.get_collection(name)
        exists = True
    except Exception:
        exists = False

    if not exists:
        client.create_collection(
            collection_name=name,
            vectors_config=qm.VectorParams(size=vector_size, distance=distance),
        )


def upsert_batched(client: QdrantClient, collection: str, points: List[qm.PointStruct], *, batch_size: int = 64) -> int:
    """Upsert points in batches to avoid Qdrant request payload size limits (default 32MB)."""
    if not points:
        return 0
    total = 0
    for i in range(0, len(points), batch_size):
        batch = points[i : i + batch_size]
        client.upsert(collection_name=collection, points=batch)
        total += len(batch)
    return total


def iter_input_files(run_folder: Path) -> List[Path]:
    archive = run_folder / "archive"
    if not archive.exists():
        return []
    files = [p for p in archive.iterdir() if p.is_file() and p.suffix.lower() in (".html", ".pdf")]
    return sorted(files)


def preflight_or_raise(*, qdrant_url: str, ollama_url: str, embed_model: str, run_folder: Path) -> None:
    """Fail-fast preflight before any upsert."""
    # 1) Qdrant reachable
    try:
        r = requests.get(qdrant_url.rstrip("/") + "/collections", timeout=5)
        if r.status_code != 200:
            raise PreflightError(f"Qdrant not ready: GET /collections -> {r.status_code}")
    except Exception as e:
        raise PreflightError(f"Qdrant not reachable: {e}")

    # 2) Ollama reachable + model exists
    try:
        r = requests.get(ollama_url.rstrip("/") + "/api/tags", timeout=5)
        if r.status_code != 200:
            raise PreflightError(f"Ollama not ready: GET /api/tags -> {r.status_code}")
        data = r.json()
        models = [m.get("name") for m in (data.get("models") or []) if isinstance(m, dict)]
        if embed_model not in models:
            raise PreflightError(f"Ollama model missing: {embed_model}. Pull it first (ollama pull {embed_model}).")
    except PreflightError:
        raise
    except Exception as e:
        raise PreflightError(f"Ollama not reachable/invalid: {e}")

    # 3) run_folder exists + has archive/*.html or archive/*.pdf
    if not run_folder.exists():
        raise PreflightError(f"run_folder not found: {run_folder}")
    htmls = iter_input_files(run_folder)
    if len(htmls) < 1:
        raise PreflightError(f"No archive/*.html or archive/*.pdf found under: {run_folder}")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-folder", required=True)
    ap.add_argument("--ollama", default=os.environ.get("OLLAMA_URL", "http://localhost:11434"))
    ap.add_argument("--qdrant", default=os.environ.get("QDRANT_URL", "http://localhost:6333"))
    ap.add_argument("--embed-model", default="bge-m3:latest")
    ap.add_argument("--vector-size", type=int, default=DEFAULT_VECTOR_SIZE)
    ap.add_argument("--max-chars", type=int, default=900)
    ap.add_argument("--overlap-chars", type=int, default=150)
    ap.add_argument("--limit", type=int, default=0, help="for testing; 0 = no limit")
    args = ap.parse_args()

    run_folder = Path(args.run_folder).expanduser().resolve()

    # Pre-flight (fail-fast) BEFORE creating collections / any upsert
    try:
        preflight_or_raise(qdrant_url=args.qdrant, ollama_url=args.ollama, embed_model=args.embed_model, run_folder=run_folder)
    except PreflightError as e:
        raise SystemExit(f"PREFLIGHT_FAILED: {e}")

    # Derive source_run from folder name prefix if possible
    source_run = run_folder.name.split("_")[0]

    qdrant = QdrantClient(url=args.qdrant)
    ensure_collection(qdrant, DOC_COLLECTION, vector_size=args.vector_size, distance=DEFAULT_DISTANCE)
    ensure_collection(qdrant, CHUNK_COLLECTION, vector_size=args.vector_size, distance=DEFAULT_DISTANCE)

    input_files = iter_input_files(run_folder)
    if args.limit and args.limit > 0:
        input_files = input_files[: args.limit]

    manifest_rows: List[Dict[str, Any]] = []
    issues_rows: List[Dict[str, Any]] = []

    upsert_doc_points: List[qm.PointStruct] = []
    upsert_chunk_points: List[qm.PointStruct] = []

    processed = 0
    skipped = 0  # doc_embed_failed or partial (chunk_embed_failed)
    errored = 0

    for input_path in input_files:
        processed += 1
        try:
            if input_path.suffix.lower() == ".pdf":
                plain_text, meta = pdf_to_text_and_meta(input_path)
            else:
                html = input_path.read_text(encoding="utf-8", errors="ignore")
                plain_text, meta = html_to_text_and_meta(html)
        except Exception as e:
            errored += 1
            manifest_rows.append({
                "ts": now_iso(),
                "status": "error",
                "error": f"read_or_parse_failed: {e}",
                "local_path": str(input_path),
            })
            continue

        # Prepend title to help retrieval
        title = meta.get("title") or ""
        if title and not plain_text.startswith(title):
            canonical_text = normalize_whitespace(title + "\n\n" + plain_text)
        else:
            canonical_text = plain_text

        doc_sha = sha256_text(canonical_text)
        sections = split_sections(canonical_text)

        reasoning_for_issues = sections.get("reasoning") or sections.get("full") or ""
        candidate_issues = extract_candidate_issues(reasoning_for_issues)

        # Per Sean feedback: only extract from "本院之判斷" / "得心證之理由" / "兩造爭執事項" / "經查：" / "茲分述如下" sections onwards
        # Use full text to find the header position
        full_text_for_norm_extraction = sections.get("full") or ""
        
        # Per Sean: if no header detected, fallback to full text (already done below)
        # Also per Sean: Supreme Court (最高法院) judgments should NOT use header filtering - use full text
        court_name = meta.get("court", "")
        is_supreme_court = "最高法院" in court_name
        
        if is_supreme_court:
            # Supreme Court: use full text, no header filtering
            norms_text = full_text_for_norm_extraction
        else:
            # Other courts: try to find reasoning header
            court_reasoning_start_pos = find_court_reasoning_start(full_text_for_norm_extraction)
            if court_reasoning_start_pos > 0:
                norms_text = full_text_for_norm_extraction[court_reasoning_start_pos:]
            else:
                # Fallback to reasoning section if header not found
                norms_text = sections.get("reasoning") or sections.get("full") or ""

        cited_norms = extract_norms(norms_text)
        norms_reasoning_snippets = extract_norm_snippets(norms_text, window=1)
        fact_reason_snippets = extract_fact_reason_snippets(norms_text, window=2)
        reasoning_snippets = extract_reasoning_snippets(norms_text)

        # Build doc-level text (shorten: title + first ~1200 chars of full)
        doc_text = canonical_text[:1200]
        try:
            doc_vec = ollama_embed([doc_text], ollama=args.ollama, model=args.embed_model)[0]
        except Exception as e:
            skipped += 1
            manifest_rows.append({
                "ts": now_iso(),
                "status": "skipped",
                "error": f"doc_embed_failed: {e}",
                "local_path": str(input_path),
                "doc_sha256": doc_sha,
                "title": title,
                "doc_url": meta.get("doc_url"),
            })
            continue

        # Qdrant point IDs must be uint or UUID. Use UUID derived from stable sha256.
        doc_uuid = hashlib.md5(f"{doc_sha}:doc".encode("utf-8")).hexdigest()
        doc_id = f"{doc_uuid[0:8]}-{doc_uuid[8:12]}-{doc_uuid[12:16]}-{doc_uuid[16:20]}-{doc_uuid[20:32]}"

        used_full_text_fallback = False
        doc_payload: Dict[str, Any] = {
            "point_id": doc_id,
            "source_run": source_run,
            "system": "FJUD",  # archive html here is from FJUD in this run
            "title": title,
            "court": meta.get("court"),
            "court_tier": meta.get("court_tier"),
            "date": meta.get("date"),
            "date_raw": meta.get("date_raw"),
            "case_no": meta.get("case_no"),
            "cause": meta.get("cause"),
            "parties_raw": meta.get("parties_raw"),
            "doc_url": meta.get("doc_url"),
            "local_path": str(input_path),
            "doc_sha256": doc_sha,
            "candidate_issues": candidate_issues,
            "cited_norms": cited_norms,
            "norms_reasoning_snippets": norms_reasoning_snippets,
            "fact_reason_snippets": fact_reason_snippets,
            "reasoning_snippets": reasoning_snippets,
            "parser_version": "v3.6-heading-normalization-full-fallback",
            "level": "doc",
            "used_full_text_fallback": False,
        }

        upsert_doc_points.append(qm.PointStruct(id=doc_id, vector=doc_vec, payload=doc_payload))

        if candidate_issues:
            issues_rows.append({
                "ts": now_iso(),
                "doc_id": doc_id,
                "doc_sha256": doc_sha,
                "title": title,
                "doc_url": meta.get("doc_url"),
                "local_path": str(input_path),
                "candidate_issues": candidate_issues,
            })

        # Chunk-level points
        failed_sections: List[str] = []
        chunkable_sections = {k: v for k, v in sections.items() if k != "full"}
        if not chunkable_sections and sections.get("full"):
            chunkable_sections = {"full": sections["full"]}
            used_full_text_fallback = True
            doc_payload["used_full_text_fallback"] = True

        for section_name, section_text in chunkable_sections.items():
            chunk_strs = chunk_text(section_text, max_chars=args.max_chars, overlap_chars=args.overlap_chars)
            if not chunk_strs:
                continue
            try:
                vecs = ollama_embed(chunk_strs, ollama=args.ollama, model=args.embed_model)
            except Exception as e:
                failed_sections.append(f"{section_name}: {e}")
                continue
            for i, (chunk_s, vec) in enumerate(zip(chunk_strs, vecs)):
                chunk_sha = sha256_text(chunk_s)
                raw_id = f"{doc_sha}:{section_name}:{i}"
                h = hashlib.md5(raw_id.encode("utf-8")).hexdigest()
                chunk_id = f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
                payload = {
                    **doc_payload,
                    "level": "chunk",
                    "section": section_name,
                    "chunk_index": i,
                    "chunk_sha256": chunk_sha,
                    "text": chunk_s,
                    "point_id": chunk_id,
                }
                upsert_chunk_points.append(qm.PointStruct(id=chunk_id, vector=vec, payload=payload))

        if failed_sections:
            skipped += 1
            manifest_rows.append({
                "ts": now_iso(),
                "status": "partial",
                "error": f"chunk_embed_failed: {'; '.join(failed_sections)}",
                "doc_sha256": doc_sha,
                "title": title,
                "local_path": str(input_path),
                "doc_url": meta.get("doc_url"),
            })
        else:
            manifest_rows.append({
                "ts": now_iso(),
                "status": "ok",
                "doc_sha256": doc_sha,
                "title": title,
                "local_path": str(input_path),
                "doc_url": meta.get("doc_url"),
            })

    if upsert_doc_points:
        upsert_batched(qdrant, DOC_COLLECTION, upsert_doc_points, batch_size=64)
    if upsert_chunk_points:
        upsert_batched(qdrant, CHUNK_COLLECTION, upsert_chunk_points, batch_size=64)

    manifest_path = run_folder / "ingest_manifest.jsonl"
    write_jsonl(manifest_path, manifest_rows)

    issues_path = run_folder / "issues.jsonl"
    if issues_rows:
        write_jsonl(issues_path, issues_rows)

    report_path = run_folder / "ingest_report.md"
    report = [
        f"# Ingest report\n",
        f"- Run folder: `{run_folder}`\n",
        f"- Collections: `{DOC_COLLECTION}`, `{CHUNK_COLLECTION}`\n",
        f"- Embed model: `{args.embed_model}`\n",
        f"- Files discovered (HTML+PDF): {len(input_files)}\n",
        f"- Processed: {processed}\n",
        f"- Skipped/Partial: {skipped}\n",
        f"- Errored: {errored}\n",
        f"- Doc points upserted: {len(upsert_doc_points)}\n",
        f"- Chunk points upserted: {len(upsert_chunk_points)}\n",
        f"- Manifest: `{manifest_path}`\n",
        f"- Issues (M2): `{issues_path}` (rows={len(issues_rows)})\n",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")

    print(
        f"OK files={len(input_files)} processed={processed} skipped={skipped} errored={errored} "
        f"doc_points={len(upsert_doc_points)} chunk_points={len(upsert_chunk_points)}"
    )
    print(f"manifest={manifest_path}")
    print(f"report={report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
