#!/usr/bin/env python3
"""edgar-risk-diff: diff Risk Factors (Item 1A) between two SEC 10-K filings.

Subcommands:
  diff <TICKER>                          Diff the two most recent 10-Ks.
  diff <TICKER> --years 2024 2022        Diff specific filing years.
  latest <TICKER>                        Print the latest Risk Factors section.
  novelty <TICKER>                       Premium: embedding-based novelty score.
  scan <TICKER1> <TICKER2> ...           One-line summary across tickers.

Data source: SEC EDGAR (free, no API key).
Cache: ~/.edgar-risk-diff/cache/
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html as html_module
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import requests

CACHE_DIR = Path.home() / ".edgar-risk-diff" / "cache"
LICENSE_PATH = Path.home() / ".edgar-risk-diff" / "license.txt"
USER_AGENT = os.environ.get(
    "EDGAR_USER_AGENT",
    "edgar-risk-diff vaze.atharva18@gmail.com",
)
EDGAR_HEADERS = {"User-Agent": USER_AGENT, "Accept-Encoding": "gzip, deflate"}
TICKER_URL = "https://www.sec.gov/files/company_tickers.json"

# SEC rate limit: 10 req/s. Be conservative.
_LAST_REQUEST_AT = 0.0
_MIN_INTERVAL = 0.12


def _throttle() -> None:
    global _LAST_REQUEST_AT
    elapsed = time.time() - _LAST_REQUEST_AT
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _LAST_REQUEST_AT = time.time()


def _http_get(url: str) -> bytes:
    _throttle()
    r = requests.get(url, headers=EDGAR_HEADERS, timeout=30)
    r.raise_for_status()
    return r.content


def _cache_get(key: str) -> Optional[bytes]:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    p = CACHE_DIR / hashlib.sha1(key.encode()).hexdigest()
    if p.exists():
        return p.read_bytes()
    return None


def _cache_put(key: str, value: bytes) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    p = CACHE_DIR / hashlib.sha1(key.encode()).hexdigest()
    p.write_bytes(value)


def _cached_get(url: str) -> bytes:
    hit = _cache_get(url)
    if hit is not None:
        return hit
    body = _http_get(url)
    _cache_put(url, body)
    return body


# ---------- EDGAR lookups ----------

def ticker_to_cik(ticker: str) -> str:
    ticker = ticker.upper().strip()
    data = json.loads(_cached_get(TICKER_URL))
    for row in data.values():
        if row.get("ticker") == ticker:
            return str(row["cik_str"]).zfill(10)
    raise SystemExit(f"Ticker not found in SEC company list: {ticker}")


@dataclass
class Filing:
    accession: str
    filed: str
    report_date: str
    form: str
    primary_doc: str

    @property
    def year(self) -> int:
        return int(self.report_date[:4])

    def doc_url(self, cik: str) -> str:
        acc_clean = self.accession.replace("-", "")
        return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_clean}/{self.primary_doc}"


def list_10k_filings(cik: str, limit: int = 8) -> list[Filing]:
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    sub = json.loads(_cached_get(url))
    recent = sub["filings"]["recent"]
    out: list[Filing] = []
    for i, form in enumerate(recent["form"]):
        if form != "10-K":
            continue
        out.append(
            Filing(
                accession=recent["accessionNumber"][i],
                filed=recent["filingDate"][i],
                report_date=recent["reportDate"][i],
                form=form,
                primary_doc=recent["primaryDocument"][i],
            )
        )
        if len(out) >= limit:
            break
    return out


# ---------- Risk Factors extraction ----------

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t\xa0]+")
_NL_RE = re.compile(r"\n{3,}")
_ITEM_1A_RE = re.compile(
    r"item\s*1a[\s.\-:]*risk\s*factors", re.IGNORECASE
)
_ITEM_1B_RE = re.compile(
    r"item\s*1b[\s.\-:]*unresolved\s*staff\s*comments", re.IGNORECASE
)
_ITEM_2_RE = re.compile(r"item\s*2[\s.\-:]*properties", re.IGNORECASE)


def html_to_text(html: bytes) -> str:
    try:
        s = html.decode("utf-8", errors="replace")
    except Exception:
        s = html.decode("latin-1", errors="replace")
    # Drop scripts/styles
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.DOTALL | re.IGNORECASE)
    # Convert block tags to newlines
    s = re.sub(r"</(p|div|li|tr|h[1-6]|br)\s*>", "\n", s, flags=re.IGNORECASE)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.IGNORECASE)
    s = _TAG_RE.sub("", s)
    # Decode all HTML entities (named + numeric, incl. &#160; nbsp variants).
    s = html_module.unescape(s)
    s = _WS_RE.sub(" ", s)
    s = _NL_RE.sub("\n\n", s)
    return s.strip()


def extract_risk_factors(text: str) -> Optional[str]:
    """Slice between Item 1A and (Item 1B | Item 2). Picks the *last* Item 1A
    occurrence to skip table-of-contents references."""
    starts = [m.start() for m in _ITEM_1A_RE.finditer(text)]
    if not starts:
        return None
    # Prefer a start that has a meaningful gap to the next 1B/2 (not TOC).
    best: Optional[tuple[int, int]] = None
    for st in starts:
        ends = []
        for end_re in (_ITEM_1B_RE, _ITEM_2_RE):
            m = end_re.search(text, st + 50)
            if m:
                ends.append(m.start())
        if not ends:
            continue
        en = min(ends)
        length = en - st
        if length < 1000:
            continue  # likely TOC entry, not the actual section
        if best is None or length > best[1] - best[0]:
            best = (st, en)
    if best is None:
        return None
    section = text[best[0]:best[1]].strip()
    section = _NL_RE.sub("\n\n", section)
    return section


def fetch_risk_factors(ticker: str, year: Optional[int] = None) -> tuple[Filing, str]:
    cik = ticker_to_cik(ticker)
    filings = list_10k_filings(cik)
    if not filings:
        raise SystemExit(f"No 10-K filings found for {ticker}")
    if year is not None:
        candidates = [f for f in filings if f.year == year]
        if not candidates:
            available = ", ".join(str(f.year) for f in filings)
            raise SystemExit(f"No 10-K for {ticker} in {year}. Available: {available}")
        filing = candidates[0]
    else:
        filing = filings[0]
    html = _cached_get(filing.doc_url(cik))
    text = html_to_text(html)
    rf = extract_risk_factors(text)
    if not rf:
        raise SystemExit(
            f"Could not locate Item 1A in {ticker} {filing.year} 10-K "
            f"({filing.primary_doc})."
        )
    return filing, rf


# ---------- Paragraph segmentation + diff ----------

_BULLET = re.compile(r"^\s*[•\-\*]\s+")


def to_paragraphs(text: str) -> list[str]:
    paras: list[str] = []
    for chunk in re.split(r"\n\s*\n+", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Normalize internal whitespace
        chunk = re.sub(r"\s+", " ", chunk)
        if len(chunk) < 40:
            continue
        paras.append(chunk)
    return paras


def paragraph_key(p: str) -> str:
    """Cheap fingerprint for matching paragraphs across filings."""
    s = re.sub(r"[^a-z0-9 ]+", "", p.lower())
    s = re.sub(r"\s+", " ", s).strip()
    return " ".join(s.split()[:12])


def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


@dataclass
class DiffResult:
    added: list[str]
    removed: list[str]
    modified: list[tuple[str, str, float]]
    unchanged_count: int

    @property
    def churn_pct(self) -> float:
        total = len(self.added) + len(self.removed) + len(self.modified) + self.unchanged_count
        if total == 0:
            return 0.0
        moved = len(self.added) + len(self.removed) + len(self.modified)
        return 100.0 * moved / total


def diff_paragraphs(old: list[str], new: list[str], match_threshold: float = 0.6) -> DiffResult:
    """Greedy nearest-neighbor matching by similarity."""
    used_old: set[int] = set()
    used_new: set[int] = set()
    modified: list[tuple[str, str, float]] = []
    unchanged = 0

    # First pass: exact-key matches
    key_to_old: dict[str, list[int]] = {}
    for i, p in enumerate(old):
        key_to_old.setdefault(paragraph_key(p), []).append(i)
    for j, p in enumerate(new):
        key = paragraph_key(p)
        if key in key_to_old and key_to_old[key]:
            i = key_to_old[key].pop(0)
            used_old.add(i)
            used_new.add(j)
            if old[i] == new[j]:
                unchanged += 1
            else:
                ratio = similar(old[i], new[j])
                if ratio >= 0.95:
                    unchanged += 1
                else:
                    modified.append((old[i], new[j], ratio))

    # Second pass: fuzzy match remaining
    remaining_old = [i for i in range(len(old)) if i not in used_old]
    remaining_new = [j for j in range(len(new)) if j not in used_new]
    pairs: list[tuple[float, int, int]] = []
    for i in remaining_old:
        for j in remaining_new:
            r = similar(old[i], new[j])
            if r >= match_threshold:
                pairs.append((r, i, j))
    pairs.sort(reverse=True)
    for r, i, j in pairs:
        if i in used_old or j in used_new:
            continue
        used_old.add(i)
        used_new.add(j)
        if r >= 0.95:
            unchanged += 1
        else:
            modified.append((old[i], new[j], r))

    added = [new[j] for j in range(len(new)) if j not in used_new]
    removed = [old[i] for i in range(len(old)) if i not in used_old]
    return DiffResult(added=added, removed=removed, modified=modified, unchanged_count=unchanged)


# ---------- Theme tagging (free tier) ----------

_THEMES = {
    "Cybersecurity": ["cyber", "breach", "ransomware", "malicious", "hack", "phishing", "data security"],
    "AI / ML": ["artificial intelligence", " ai ", "machine learning", "generative", "large language model", "llm", "ai model"],
    "Geopolitics / China": ["china", "taiwan", "russia", "ukraine", "sanction", "tariff", "export control", "geopolitical"],
    "Climate / ESG": ["climate", "greenhouse", "carbon", "esg", "sustainability", "emissions"],
    "Supply chain": ["supply chain", "supplier", "logistics", "shortage", "semiconductor shortage", "chip shortage"],
    "Regulation": ["regulation", "regulatory", "antitrust", "sec ", "gdpr", "ftc", "doj"],
    "Litigation": ["litigation", "lawsuit", "class action", "settlement", "investigation"],
    "Macro / Rates": ["inflation", "interest rate", "recession", "monetary policy", "credit"],
    "Pandemic / Health": ["pandemic", "covid", "outbreak", "public health"],
    "Workforce": ["workforce", "labor", "union", "talent", "remote work", "layoff"],
    "Crypto / Digital assets": ["crypto", "digital asset", "stablecoin", "blockchain", "tokeniz"],
}


def tag_themes(paragraph: str) -> list[str]:
    p = paragraph.lower()
    return [name for name, keywords in _THEMES.items() if any(k in p for k in keywords)]


# ---------- License gate (premium tier) ----------

# Replace with your Gumroad/LemonSqueezy verify endpoint in production.
# For now, accept any key listed here OR any key whose SHA-256 prefix matches.
_VALID_LICENSE_PREFIXES = {
    # SHA-256(b"DEMO-FOR-OPERATOR")[:8] — operator bypass.
    "9b2d6fb1",
    # SHA-256(b"EDGARRISK-NOVELTY-2026-A4G7")[:8] — production v1 key (Gumroad).
    "bc4c1307",
}


def license_active() -> bool:
    key = ""
    if "EDGAR_RISK_LICENSE" in os.environ:
        key = os.environ["EDGAR_RISK_LICENSE"].strip()
    elif LICENSE_PATH.exists():
        key = LICENSE_PATH.read_text(encoding="utf-8").strip()
    if not key:
        return False
    digest = hashlib.sha256(key.encode()).hexdigest()[:8]
    return digest in _VALID_LICENSE_PREFIXES


def require_license(feature: str) -> None:
    if license_active():
        return
    sys.stderr.write(
        f"\n[premium] '{feature}' requires a license key.\n"
        f"  Buy one at: https://edgar-risk-diff.gumroad.com/l/novelty  (replace with real listing)\n"
        f"  Then run:  echo YOUR-KEY > {LICENSE_PATH}\n"
        f"  Or set:    export EDGAR_RISK_LICENSE=YOUR-KEY\n\n"
    )
    sys.exit(2)


# ---------- Premium: semantic novelty ----------

def _hash_vec(text: str, dim: int = 256) -> list[float]:
    """Cheap deterministic embedding: hashed-bag-of-bigrams. No deps, no API."""
    vec = [0.0] * dim
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    if not tokens:
        return vec
    for i in range(len(tokens) - 1):
        bigram = tokens[i] + " " + tokens[i + 1]
        h = int(hashlib.md5(bigram.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
    norm = sum(v * v for v in vec) ** 0.5
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def _cos(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def novelty_scores(old_paras: list[str], new_paras: list[str]) -> list[tuple[float, str]]:
    """For each new paragraph, return (novelty, paragraph). Novelty = 1 - max cosine
    similarity to any old paragraph. Higher = more genuinely new."""
    old_vecs = [_hash_vec(p) for p in old_paras]
    out: list[tuple[float, str]] = []
    for p in new_paras:
        v = _hash_vec(p)
        if not old_vecs:
            out.append((1.0, p))
            continue
        max_sim = max(_cos(v, ov) for ov in old_vecs)
        out.append((1.0 - max_sim, p))
    out.sort(reverse=True)
    return out


# ---------- Report rendering ----------

def _trim(p: str, n: int = 280) -> str:
    return p if len(p) <= n else p[:n].rsplit(" ", 1)[0] + " …"


def render_diff_report(ticker: str, old: Filing, new: Filing, dr: DiffResult) -> str:
    lines: list[str] = []
    lines.append(f"# {ticker} — Risk Factors Diff")
    lines.append(f"_{old.year} 10-K  →  {new.year} 10-K_  ({old.filed} → {new.filed})")
    lines.append("")
    lines.append(f"**Churn:** {dr.churn_pct:.1f}%  ·  "
                 f"**Added:** {len(dr.added)}  ·  "
                 f"**Removed:** {len(dr.removed)}  ·  "
                 f"**Modified:** {len(dr.modified)}  ·  "
                 f"**Unchanged:** {dr.unchanged_count}")
    lines.append("")

    # Theme rollup on added paragraphs
    theme_counts: dict[str, int] = {}
    for p in dr.added:
        for t in tag_themes(p):
            theme_counts[t] = theme_counts.get(t, 0) + 1
    if theme_counts:
        ranked = sorted(theme_counts.items(), key=lambda x: -x[1])
        lines.append("## New themes")
        for name, n in ranked:
            lines.append(f"- **{name}** — {n} new paragraph{'s' if n != 1 else ''}")
        lines.append("")

    if dr.added:
        lines.append(f"## Added ({len(dr.added)})")
        for p in dr.added[:25]:
            tags = tag_themes(p)
            tagstr = f"  _[{', '.join(tags)}]_" if tags else ""
            lines.append(f"- {_trim(p)}{tagstr}")
        if len(dr.added) > 25:
            lines.append(f"- … {len(dr.added) - 25} more")
        lines.append("")

    if dr.removed:
        lines.append(f"## Removed ({len(dr.removed)})")
        for p in dr.removed[:15]:
            lines.append(f"- {_trim(p)}")
        if len(dr.removed) > 15:
            lines.append(f"- … {len(dr.removed) - 15} more")
        lines.append("")

    if dr.modified:
        lines.append(f"## Modified ({len(dr.modified)})")
        for old_p, new_p, ratio in dr.modified[:10]:
            lines.append(f"- **similarity {ratio:.2f}**")
            lines.append(f"  - was: {_trim(old_p, 200)}")
            lines.append(f"  - now: {_trim(new_p, 200)}")
        if len(dr.modified) > 10:
            lines.append(f"- … {len(dr.modified) - 10} more")
        lines.append("")

    lines.append("---")
    lines.append("_Free tier output. For semantic novelty ranking, run "
                 "`python3 risk_diff.py novelty <TICKER>` (premium)._")
    return "\n".join(lines)


# ---------- CLI ----------

def cmd_diff(args: argparse.Namespace) -> int:
    ticker = args.ticker.upper()
    if args.years:
        if len(args.years) != 2:
            raise SystemExit("--years requires exactly two years (newer first or older first)")
        y_new, y_old = sorted(args.years, reverse=True)
        new_filing, new_rf = fetch_risk_factors(ticker, year=y_new)
        old_filing, old_rf = fetch_risk_factors(ticker, year=y_old)
    else:
        cik = ticker_to_cik(ticker)
        filings = list_10k_filings(cik)
        if len(filings) < 2:
            raise SystemExit(f"Need at least two 10-Ks for {ticker}; found {len(filings)}.")
        new_filing, new_rf = fetch_risk_factors(ticker, year=filings[0].year)
        old_filing, old_rf = fetch_risk_factors(ticker, year=filings[1].year)

    old_paras = to_paragraphs(old_rf)
    new_paras = to_paragraphs(new_rf)
    dr = diff_paragraphs(old_paras, new_paras)
    print(render_diff_report(ticker, old_filing, new_filing, dr))
    return 0


def cmd_latest(args: argparse.Namespace) -> int:
    ticker = args.ticker.upper()
    filing, rf = fetch_risk_factors(ticker)
    print(f"# {ticker} — Risk Factors ({filing.year} 10-K, filed {filing.filed})\n")
    print(rf)
    return 0


def cmd_novelty(args: argparse.Namespace) -> int:
    require_license("novelty")
    ticker = args.ticker.upper()
    cik = ticker_to_cik(ticker)
    filings = list_10k_filings(cik)
    if len(filings) < 2:
        raise SystemExit(f"Need at least two 10-Ks for {ticker}; found {len(filings)}.")
    _, old_rf = fetch_risk_factors(ticker, year=filings[1].year)
    new_filing, new_rf = fetch_risk_factors(ticker, year=filings[0].year)
    old_paras = to_paragraphs(old_rf)
    new_paras = to_paragraphs(new_rf)
    scored = novelty_scores(old_paras, new_paras)
    print(f"# {ticker} — Risk Factor Novelty ({new_filing.year} 10-K)\n")
    print(f"Top {min(args.top, len(scored))} most novel paragraphs vs prior year:\n")
    for i, (score, p) in enumerate(scored[: args.top], 1):
        tags = tag_themes(p)
        tagstr = f"  _[{', '.join(tags)}]_" if tags else ""
        print(f"### {i}. novelty {score:.2f}{tagstr}\n{_trim(p, 600)}\n")
    return 0


def cmd_scan(args: argparse.Namespace) -> int:
    print(f"| Ticker | Year | Added | Removed | Modified | Churn % | Top new theme |")
    print(f"|--------|------|-------|---------|----------|---------|---------------|")
    for ticker in args.tickers:
        ticker = ticker.upper()
        try:
            cik = ticker_to_cik(ticker)
            filings = list_10k_filings(cik)
            if len(filings) < 2:
                print(f"| {ticker} | — | — | — | — | — | (insufficient filings) |")
                continue
            _, old_rf = fetch_risk_factors(ticker, year=filings[1].year)
            new_filing, new_rf = fetch_risk_factors(ticker, year=filings[0].year)
            dr = diff_paragraphs(to_paragraphs(old_rf), to_paragraphs(new_rf))
            theme_counts: dict[str, int] = {}
            for p in dr.added:
                for t in tag_themes(p):
                    theme_counts[t] = theme_counts.get(t, 0) + 1
            top = max(theme_counts.items(), key=lambda x: x[1])[0] if theme_counts else "—"
            print(f"| {ticker} | {new_filing.year} | {len(dr.added)} | {len(dr.removed)} | "
                  f"{len(dr.modified)} | {dr.churn_pct:.1f} | {top} |")
        except SystemExit as e:
            print(f"| {ticker} | — | — | — | — | — | error: {e} |")
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="risk_diff", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_diff = sub.add_parser("diff", help="Diff Risk Factors between two 10-Ks")
    p_diff.add_argument("ticker")
    p_diff.add_argument("--years", nargs=2, type=int, metavar=("Y1", "Y2"))
    p_diff.set_defaults(func=cmd_diff)

    p_latest = sub.add_parser("latest", help="Print the latest Risk Factors section")
    p_latest.add_argument("ticker")
    p_latest.set_defaults(func=cmd_latest)

    p_nov = sub.add_parser("novelty", help="[premium] Embedding-based novelty score")
    p_nov.add_argument("ticker")
    p_nov.add_argument("--top", type=int, default=10)
    p_nov.set_defaults(func=cmd_novelty)

    p_scan = sub.add_parser("scan", help="One-line summary across multiple tickers")
    p_scan.add_argument("tickers", nargs="+")
    p_scan.set_defaults(func=cmd_scan)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
