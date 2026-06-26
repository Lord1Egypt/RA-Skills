#!/usr/bin/env python3
from typing import Union, Optional
"""Query SEC EDGAR for company filings and financial data.

Uses the free EDGAR FULL-TEXT SEARCH API and company data endpoints.
Requires a User-Agent header identifying the requester per SEC policy:
    SEC_EDGAR_USER_AGENT="Name email@example.com"

Usage:
    python sec_edgar.py <command> [options]

Commands:
    search          Full-text search across EDGAR filings
    filings         Recent filings for a company (by CIK or ticker)
    filing-index    List all documents in a filing package
    read-filing     Download and read the text content of a filing
    company         Company facts (structured XBRL data)
    concept         Single XBRL concept time series for a company
    submissions     Filing history and company metadata
    insider         Insider transactions (Forms 3, 4, 5)
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

DEFAULT_UA = "OpenClaw/1.0 agent@openclaw.ai"


class _HTMLTextExtractor(HTMLParser):
    """Strip HTML tags, keep text content."""
    def __init__(self):
        super().__init__()
        self._parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "head"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "head"):
            self._skip = False
        if tag in ("p", "div", "tr", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th"):
            self._parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self._parts.append(data)

    def get_text(self) -> str:
        raw = "".join(self._parts)
        lines = [re.sub(r"[ \t]+", " ", ln).strip() for ln in raw.splitlines()]
        text = "\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def _html_to_text(html_content: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(html_content)
    return parser.get_text()


def _get(url: str, ua: str, accept: str = "application/json") -> Union[dict, list]:
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": accept,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"EDGAR API error ({e.code}): {body}") from e


def _get_raw(url: str, ua: str) -> str:
    """Fetch raw text/HTML content from a URL."""
    req = urllib.request.Request(url, headers={
        "User-Agent": ua,
        "Accept": "text/html, application/xhtml+xml, text/plain, */*",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"EDGAR fetch error ({e.code}): {body}") from e


def _resolve_cik(identifier: str, ua: str) -> str:
    """Resolve a ticker symbol to a zero-padded 10-digit CIK."""
    if identifier.isdigit():
        return identifier.zfill(10)
    url = "https://www.sec.gov/files/company_tickers.json"
    data = _get(url, ua)
    ticker_upper = identifier.upper()
    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker_upper:
            return str(entry["cik_str"]).zfill(10)
    raise ValueError(f"Ticker '{identifier}' not found in SEC ticker list")


def cmd_search(query: str, form_type: str, date_from: str, date_to: str, limit: int, ua: str) -> dict:
    """Full-text search via EDGAR FULL-TEXT SEARCH API (efts)."""
    base = "https://efts.sec.gov/LATEST/search-index"
    params = [f"q={urllib.request.quote(query)}", f"from=0", f"size={limit}"]
    if form_type:
        params.append(f"forms={urllib.request.quote(form_type)}")
    if date_from:
        params.append(f"dateRange=custom&startdt={date_from}")
    if date_to:
        params.append(f"enddt={date_to}")
    url = f"{base}?{'&'.join(params)}"
    return _get(url, ua)


def cmd_filings(identifier: str, form_type: str, limit: int, ua: str) -> dict:
    """Get recent filings for a company via the submissions endpoint."""
    cik = _resolve_cik(identifier, ua)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = _get(url, ua)
    recent = data.get("filings", {}).get("recent", {})
    if not recent:
        return {"error": "No recent filings found", "cik": cik}
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])
    results = []
    for i in range(len(forms)):
        if form_type and forms[i] != form_type:
            continue
        acc_no_dashes = accessions[i].replace("-", "")
        results.append({
            "form": forms[i],
            "filingDate": dates[i],
            "accessionNumber": accessions[i],
            "primaryDocument": primary_docs[i] if i < len(primary_docs) else None,
            "description": descriptions[i] if i < len(descriptions) else None,
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_dashes}/{primary_docs[i]}" if i < len(primary_docs) else None,
        })
        if len(results) >= limit:
            break
    company_name = data.get("name", "")
    return {"cik": cik, "company": company_name, "filings": results}


def cmd_filing_index(identifier: str, accession: str, ua: str) -> dict:
    """List all documents in a filing package."""
    cik = _resolve_cik(identifier, ua)
    acc_no_dashes = accession.replace("-", "")
    url = f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_dashes}/index.json"
    data = _get(url, ua)
    directory = data.get("directory", {})
    items = directory.get("item", [])
    docs = []
    for item in items:
        name = item.get("name", "")
        docs.append({
            "name": name,
            "type": item.get("type", ""),
            "size": item.get("size", ""),
            "lastModified": item.get("last-modified", ""),
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_dashes}/{name}",
        })
    return {"cik": cik, "accession": accession, "documents": docs}


# 10-K / 10-Q standard section headings for extraction
_10K_SECTIONS = {
    "1":   r"item\s+1[.\s:—–-]+business",
    "1a":  r"item\s+1a[.\s:—–-]+risk\s+factors",
    "1b":  r"item\s+1b[.\s:—–-]+unresolved\s+staff\s+comments",
    "2":   r"item\s+2[.\s:—–-]+properties",
    "3":   r"item\s+3[.\s:—–-]+legal\s+proceedings",
    "5":   r"item\s+5[.\s:—–-]+market",
    "6":   r"item\s+6[.\s:—–-]+(selected|reserved)",
    "7":   r"item\s+7[.\s:—–-]+management",
    "7a":  r"item\s+7a[.\s:—–-]+quantitative",
    "8":   r"item\s+8[.\s:—–-]+financial\s+statements",
    "9":   r"item\s+9[.\s:—–-]+changes",
    "9a":  r"item\s+9a[.\s:—–-]+controls",
    "10":  r"item\s+10[.\s:—–-]+directors",
    "11":  r"item\s+11[.\s:—–-]+executive\s+compensation",
    "12":  r"item\s+12[.\s:—–-]+security\s+ownership",
    "13":  r"item\s+13[.\s:—–-]+certain\s+relationships",
    "14":  r"item\s+14[.\s:—–-]+principal\s+account",
}


def _extract_section(text: str, section: str) -> Optional[str]:
    """Try to extract a specific 10-K/10-Q section from filing text."""
    section = section.lower().strip()
    pattern = _10K_SECTIONS.get(section)
    if not pattern:
        return None
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    if not matches:
        return None
    # Use the last match (skip table of contents entries which appear first)
    start = matches[-1].start()
    rest = text[start + len(matches[-1].group()):]
    next_item = re.search(r"\n\s*item\s+\d+[a-z]?[\s.:—–-]", rest, re.IGNORECASE)
    if next_item:
        end = start + len(matches[-1].group()) + next_item.start()
    else:
        end = min(start + 80000, len(text))
    return text[start:end].strip()


def cmd_read_filing(url: str, section: str, max_chars: int, ua: str) -> dict:
    """Download a filing and return its text content."""
    raw = _get_raw(url, ua)
    is_html = "<html" in raw[:500].lower() or "<body" in raw[:500].lower()
    text = _html_to_text(raw) if is_html else raw

    result: dict = {"url": url, "totalChars": len(text)}

    if section:
        extracted = _extract_section(text, section)
        if extracted:
            if len(extracted) > max_chars:
                extracted = extracted[:max_chars] + f"\n\n... [truncated at {max_chars} chars, full section is {len(extracted)} chars]"
            result["section"] = section
            result["content"] = extracted
            return result
        result["warning"] = f"Section 'Item {section}' not found, returning first {max_chars} chars"

    if len(text) > max_chars:
        result["content"] = text[:max_chars] + f"\n\n... [truncated at {max_chars} chars, full document is {len(text)} chars]"
        result["truncated"] = True
    else:
        result["content"] = text
    return result


def cmd_company_facts(identifier: str, ua: str) -> dict:
    """Get structured XBRL company facts (all reported concepts)."""
    cik = _resolve_cik(identifier, ua)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    data = _get(url, ua)
    entity = data.get("entityName", "")
    facts_raw = data.get("facts", {})
    summary = {}
    for taxonomy, concepts in facts_raw.items():
        summary[taxonomy] = list(concepts.keys())[:50]
    return {
        "cik": cik,
        "entity": entity,
        "taxonomies": summary,
        "hint": "Use the 'concept' command to drill into a specific concept, e.g. us-gaap/Revenue",
    }


def cmd_concept(identifier: str, taxonomy: str, concept: str, ua: str) -> dict:
    """Get time-series data for a single XBRL concept."""
    cik = _resolve_cik(identifier, ua)
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/{taxonomy}/{concept}.json"
    data = _get(url, ua)
    entity = data.get("entityName", "")
    units = data.get("units", {})
    result = {"cik": cik, "entity": entity, "concept": f"{taxonomy}/{concept}", "units": {}}
    for unit_name, values in units.items():
        result["units"][unit_name] = values[-20:]
    return result


def cmd_submissions(identifier: str, ua: str) -> dict:
    """Get company metadata and filing history summary."""
    cik = _resolve_cik(identifier, ua)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = _get(url, ua)
    return {
        "cik": cik,
        "name": data.get("name"),
        "tickers": data.get("tickers", []),
        "exchanges": data.get("exchanges", []),
        "sic": data.get("sic"),
        "sicDescription": data.get("sicDescription"),
        "stateOfIncorporation": data.get("stateOfIncorporation"),
        "fiscalYearEnd": data.get("fiscalYearEnd"),
        "website": data.get("website"),
        "phone": data.get("phone"),
        "addresses": data.get("addresses"),
        "formerNames": data.get("formerNames", []),
        "filingCount": len(data.get("filings", {}).get("recent", {}).get("form", [])),
    }


def cmd_insider(identifier: str, limit: int, ua: str) -> dict:
    """Get insider transactions by fetching Forms 3, 4, 5."""
    cik = _resolve_cik(identifier, ua)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    data = _get(url, ua)
    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    insider_forms = {"3", "4", "5", "3/A", "4/A", "5/A"}
    results = []
    for i in range(len(forms)):
        if forms[i] not in insider_forms:
            continue
        acc_no_dashes = accessions[i].replace("-", "")
        results.append({
            "form": forms[i],
            "filingDate": dates[i],
            "accessionNumber": accessions[i],
            "url": f"https://www.sec.gov/Archives/edgar/data/{cik.lstrip('0')}/{acc_no_dashes}/{primary_docs[i]}" if i < len(primary_docs) else None,
        })
        if len(results) >= limit:
            break
    return {"cik": cik, "company": data.get("name", ""), "insider_filings": results}


def main() -> int:
    ap = argparse.ArgumentParser(description="Query SEC EDGAR.")
    ap.add_argument("command", choices=[
        "search", "filings", "filing-index", "read-filing",
        "company", "concept", "submissions", "insider",
    ])
    ap.add_argument("identifier", nargs="?", default="",
                     help="Ticker symbol or CIK number (required for most commands)")
    ap.add_argument("--query", "-q", default="", help="Search query text (for 'search' command)")
    ap.add_argument("--form-type", default="", help="Filter by form type (e.g. 10-K, 10-Q, 8-K)")
    ap.add_argument("--date-from", default="", help="Start date YYYY-MM-DD (search only)")
    ap.add_argument("--date-to", default="", help="End date YYYY-MM-DD (search only)")
    ap.add_argument("--limit", type=int, default=10, help="Max results to return")
    ap.add_argument("--taxonomy", default="us-gaap", help="XBRL taxonomy (default: us-gaap)")
    ap.add_argument("--concept", default="", help="XBRL concept name (e.g. Revenue, NetIncomeLoss)")
    ap.add_argument("--accession", default="", help="Filing accession number (for filing-index)")
    ap.add_argument("--url", default="", help="Direct filing document URL (for read-filing)")
    ap.add_argument("--section", default="", help="10-K/10-Q section to extract (e.g. 1, 1a, 7, 8)")
    ap.add_argument("--max-chars", type=int, default=50000,
                     help="Max characters to return from read-filing (default 50000)")
    ap.add_argument("--user-agent", default="",
                     help="SEC-required User-Agent (or set SEC_EDGAR_USER_AGENT env var)")
    args = ap.parse_args()

    import os
    ua = args.user_agent or os.environ.get("SEC_EDGAR_USER_AGENT", DEFAULT_UA)

    handlers = {
        "search": lambda: cmd_search(args.query or args.identifier, args.form_type, args.date_from, args.date_to, args.limit, ua),
        "filings": lambda: cmd_filings(args.identifier, args.form_type, args.limit, ua),
        "filing-index": lambda: cmd_filing_index(args.identifier, args.accession, ua),
        "read-filing": lambda: cmd_read_filing(args.url, args.section, args.max_chars, ua),
        "company": lambda: cmd_company_facts(args.identifier, ua),
        "concept": lambda: cmd_concept(args.identifier, args.taxonomy, args.concept, ua),
        "submissions": lambda: cmd_submissions(args.identifier, ua),
        "insider": lambda: cmd_insider(args.identifier, args.limit, ua),
    }

    no_id_commands = {"search", "read-filing"}
    if args.command not in no_id_commands and not args.identifier:
        print("Error: identifier (ticker or CIK) is required", file=sys.stderr)
        return 1
    if args.command == "concept" and not args.concept:
        print("Error: --concept is required for 'concept' command", file=sys.stderr)
        return 1
    if args.command == "filing-index" and not args.accession:
        print("Error: --accession is required for 'filing-index' command", file=sys.stderr)
        return 1
    if args.command == "read-filing" and not args.url:
        print("Error: --url is required for 'read-filing' command", file=sys.stderr)
        return 1

    try:
        result = handlers[args.command]()
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
