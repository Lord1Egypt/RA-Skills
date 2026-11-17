#!/usr/bin/env python3
"""cite-check phase 2: does the cited source actually SUPPORT the claim?

Phase 1 (cite_check.py) confirms a source is real. This confirms the source
backs the claim sitting next to it, catching misattribution: a real paper
cited for something it never says.

Pipeline per (claim, source) pair:
    1. extract  - decompose the draft into atomic (claim, citation) pairs
    2. retrieve - fetch readable text for the cited URL / arXiv id
    3. verify   - score claim-vs-source with a local fact-checking model
    4. route    - SUPPORTED (auto-pass) / UNSUPPORTED / UNVERIFIABLE

Everything runs locally: claim extraction via a local Ollama instruct model,
verification via Bespoke-MiniCheck (a small grounded fact-checker, GPT-4-level
at this one job) on Ollama. No external API, no per-call cost.

Usage:
    cite-check-claims <file>           # check a draft
    cite-check-claims <file> --json
Exit code 0 when every claim is SUPPORTED (or there are none), 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict, field
from typing import Optional

import httpx

import cite_check as cc  # reuse citation extraction + resolve helpers

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EXTRACT_MODEL = os.environ.get("CITE_CHECK_EXTRACT_MODEL", "qwen2.5:7b-instruct-q4_K_M")
# Verifier: an NLI cross-encoder, fast on CPU (~100-200ms/pair). A 7B grounded
# fact-checker (bespoke-minicheck) is more accurate but impractically slow on a
# CPU-only box, so NLI is the default; set CITE_CHECK_NLI_MODEL to swap it.
NLI_MODEL = os.environ.get("CITE_CHECK_NLI_MODEL", "cross-encoder/nli-deberta-v3-base")
ENTAIL_THRESHOLD = float(os.environ.get("CITE_CHECK_ENTAIL_THRESHOLD", "0.5"))
CHUNK = 1200  # chars per source window fed to the verifier

SUPPORTED = "SUPPORTED"        # source entails the claim; auto-pass
PARTLY = "PARTLY"              # weak/borderline entailment; human review
UNSUPPORTED = "UNSUPPORTED"    # source does not back the claim
UNVERIFIABLE = "UNVERIFIABLE"  # source could not be read (dead, paywalled, empty)
PARTLY_FLOOR = 0.30           # below SUPPORTED threshold but worth a human look


@dataclass
class Claim:
    claim: str
    ref: str                 # the citation as it appeared (url or arXiv id)
    is_arxiv: bool = False
    verdict: str = ""
    detail: str = ""
    source_chars: int = 0


# --- 1. claim extraction -------------------------------------------------

EXTRACT_PROMPT = """You split drafts into atomic claim/citation pairs for fact-checking.

Rules:
- A claim is ONE verifiable assertion. Split compound sentences into separate claims.
- Each claim must be self-contained: resolve pronouns ("it", "they") to the real noun.
- Attach the citation (URL or arXiv id) that sits next to the claim.
- Only include sentences that actually carry a citation. Ignore the rest.
- Output ONLY a JSON array, no prose. Each item: {{"claim": "...", "ref": "..."}}.

Draft:
---
{draft}
---
JSON array:"""


def _ollama_generate(model: str, prompt: str, timeout: int = 120) -> str:
    r = httpx.post(f"{OLLAMA}/api/generate",
                   json={"model": model, "prompt": prompt, "stream": False,
                         "options": {"temperature": 0}},
                   timeout=timeout)
    r.raise_for_status()
    return r.json().get("response", "")


def extract_claims(text: str) -> list[Claim]:
    """LLM decomposition with a deterministic regex fallback."""
    try:
        raw = _ollama_generate(EXTRACT_MODEL, EXTRACT_PROMPT.format(draft=text[:8000]))
        m = re.search(r"\[.*\]", raw, re.DOTALL)
        if m:
            items = json.loads(m.group(0))
            claims = []
            for it in items:
                ref = str(it.get("ref", "")).strip()
                claim = str(it.get("claim", "")).strip()
                if claim and ref:
                    claims.append(Claim(claim=claim, ref=ref,
                                        is_arxiv=_looks_arxiv(ref)))
            if claims:
                return claims
    except (httpx.HTTPError, json.JSONDecodeError, KeyError, TypeError):
        pass
    return _fallback_extract(text)


def _looks_arxiv(ref: str) -> bool:
    return bool(re.search(r"\d{4}\.\d{4,5}", ref)) and "http" not in ref.lower()


def _fallback_extract(text: str) -> list[Claim]:
    """No-LLM fallback: pair each citation-bearing sentence with its citation."""
    claims: list[Claim] = []
    for sent in re.split(r"(?<=[.!?])\s+", text):
        urls, ids = cc.find_citations(sent)
        for u in urls:
            claims.append(Claim(claim=sent.strip(), ref=u))
        for aid in ids:
            claims.append(Claim(claim=sent.strip(), ref=aid, is_arxiv=True))
    return claims


# --- 2. source retrieval -------------------------------------------------

def _clean_html(html: str) -> str:
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        return re.sub(r"\n{3,}", "\n\n", soup.get_text("\n")).strip()
    except Exception:
        return re.sub(r"<[^>]+>", " ", html)


def fetch_source_text(claim: Claim, client: httpx.Client) -> tuple[Optional[str], str]:
    """Return (text, note). text is None when the source can't be read."""
    if claim.is_arxiv:
        aid = re.search(r"\d{4}\.\d{4,5}", claim.ref).group(0)
        # ar5iv gives clean HTML full text; fall back to the API abstract.
        try:
            r = client.get(f"https://ar5iv.org/abs/{aid}", follow_redirects=True,
                           timeout=25)
            if r.status_code < 400 and len(r.text) > 2000:
                return _clean_html(r.text), "ar5iv full text"
        except httpx.HTTPError:
            pass
        try:
            r = client.get(cc.ARXIV_API, params={"id_list": aid},
                           follow_redirects=True, timeout=20)
            m = re.search(r"<summary>(.*?)</summary>", r.text, re.DOTALL)
            if m:
                return m.group(1).strip(), "arXiv abstract only"
        except httpx.HTTPError:
            pass
        return None, "arXiv source unreadable"

    url = claim.ref
    try:
        r = client.get(url, follow_redirects=True, timeout=25,
                       headers={"User-Agent": cc.UA})
    except httpx.HTTPError as e:
        return None, f"fetch failed: {type(e).__name__}"
    if r.status_code >= 400:
        return None, f"HTTP {r.status_code}"

    ctype = r.headers.get("content-type", "")
    if "pdf" in ctype or url.lower().endswith(".pdf"):
        try:
            import fitz  # pymupdf, optional
            doc = fitz.open(stream=r.content, filetype="pdf")
            return "\n".join(p.get_text() for p in doc), "pdf text"
        except Exception:
            return None, "pdf unreadable (pymupdf missing)"
    text = _clean_html(r.text)
    if len(text) < 50:
        return None, "page empty or login-walled"
    return text, "html text"


# --- 3. verification (Bespoke-MiniCheck on Ollama) -----------------------

_NLI = None  # lazily loaded CrossEncoder; label order: contradiction/entailment/neutral


def _nli():
    global _NLI
    if _NLI is None:
        from sentence_transformers import CrossEncoder
        _NLI = CrossEncoder(NLI_MODEL)
    return _NLI


def _entail_prob(premise: str, hypothesis: str) -> float:
    """Probability that `premise` entails `hypothesis` (0..1)."""
    import numpy as np
    logits = _nli().predict([(premise, hypothesis)])[0]
    e = np.exp(logits - np.max(logits))
    probs = e / e.sum()
    return float(probs[1])  # index 1 == entailment for nli-deberta-v3


def supports(doc: str, claim: str) -> tuple[bool, float]:
    """True if the source supports the claim. Lenient over chunks: supported if
    ANY chunk entails the claim above threshold. Returns (supported, best_prob)."""
    best = 0.0
    for i in range(0, min(len(doc), CHUNK * 12), CHUNK):
        chunk = doc[i:i + CHUNK].strip()
        if not chunk:
            continue
        p = _entail_prob(chunk, claim)
        best = max(best, p)
        if best >= ENTAIL_THRESHOLD:
            return True, best
    return False, best


# --- 4. orchestrate + route ----------------------------------------------

def assess(claims: list[Claim]) -> list[Claim]:
    with httpx.Client() as client:
        for c in claims:
            text, note = fetch_source_text(c, client)
            if text is None:
                c.verdict, c.detail = UNVERIFIABLE, note
                continue
            c.source_chars = len(text)
            ok, score = supports(text, c.claim)
            if ok:
                c.verdict = SUPPORTED
            elif score >= PARTLY_FLOOR:
                c.verdict = PARTLY
            else:
                c.verdict = UNSUPPORTED
            c.detail = f"{note}; entailment {score:.2f}"
    return claims


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="cite-check-claims",
        description="Check that each cited source actually supports its claim.")
    ap.add_argument("file", nargs="?", help="draft file (default: stdin)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    text = open(args.file, encoding="utf-8", errors="replace").read() \
        if args.file else sys.stdin.read()

    claims = assess(extract_claims(text))
    bad = [c for c in claims if c.verdict != SUPPORTED]

    if args.json:
        print(json.dumps({"checked": len(claims), "not_supported": len(bad),
                          "claims": [asdict(c) for c in claims]}, indent=2))
    else:
        if not claims:
            print("cite-check-claims: no cited claims found.")
        for c in claims:
            mark = "PASS" if c.verdict == SUPPORTED else "FLAG"
            print(f"[{mark}] {c.verdict:<12} {c.ref}")
            print(f"        claim: {c.claim[:100]}")
            if c.verdict != SUPPORTED:
                print(f"        -> {c.detail}")
        print(f"\ncite-check-claims: {len(claims)-len(bad)}/{len(claims)} supported"
              + (f", {len(bad)} need a human eye" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
