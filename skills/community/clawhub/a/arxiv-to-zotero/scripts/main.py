#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main CLI for the arxiv-to-zotero skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import socket
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


APP_NAME = "arxiv-to-zotero"
APP_VERSION = "1.0.2"
DEFAULT_SKILL_TAG = APP_NAME
DEFAULT_TARGET_COLLECTION_NAME = APP_NAME


def fixed_config_path() -> Path:
    return Path(__file__).resolve().parent.parent / "config.json"


def fixed_env_path() -> Path:
    return Path("~/.openclaw/.env").expanduser()


ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
HTTP_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------------------------
# 数据结构 / Data model
# ---------------------------------------------------------------------------
@dataclass
class PaperRecord:
    """统一论文记录 / Unified paper record."""

    title: str
    authors: List[str] = field(default_factory=list)
    abstract: str | None = None
    year: int | None = None
    venue: str | None = None
    comments: str | None = None
    journal_ref: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    url: str | None = None
    pdf_url: str | None = None
    citation_count: int | None = None
    source_names: List[str] = field(default_factory=list)
    source_payloads: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HttpResponse:
    status_code: int
    headers: Dict[str, str]
    body: bytes

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text)


def http_request(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: str | bytes | None = None,
    timeout: int = 20,
) -> HttpResponse:
    if params:
        encoded_params = urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None}, doseq=True
        )
        if encoded_params:
            separator = '&' if '?' in url else '?'
            url = f"{url}{separator}{encoded_params}"
    payload: bytes | None
    if isinstance(data, str):
        payload = data.encode('utf-8')
    else:
        payload = data
    request = urllib.request.Request(url, data=payload, method=method.upper())
    for key, value in (headers or {}).items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return HttpResponse(
                status_code=getattr(response, 'status', response.getcode()),
                headers={k: v for k, v in response.headers.items()},
                body=response.read(),
            )
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return HttpResponse(
            status_code=exc.code,
            headers={k: v for k, v in exc.headers.items()},
            body=body,
        )


def ensure_success(response: HttpResponse, context: str = 'HTTP request') -> HttpResponse:
    if 200 <= response.status_code < 300:
        return response
    detail = response.text.strip()
    if len(detail) > 300:
        detail = detail[:300] + '...'
    if detail:
        raise RuntimeError(f"{context} failed with HTTP {response.status_code}: {detail}")
    raise RuntimeError(f"{context} failed with HTTP {response.status_code}")


def safe_filename_from_url(url: str | None, default: str = "paper.pdf") -> str:
    """Build a stable PDF filename from a URL."""
    raw = (url or '').strip()
    if not raw:
        return default
    parsed = urllib.parse.urlparse(raw)
    name = Path(urllib.parse.unquote(parsed.path or '')).name or default
    if not name.lower().endswith('.pdf'):
        name = f"{name}.pdf" if name else default
    name = re.sub(r'[^A-Za-z0-9._-]+', '_', name).strip('._')
    return name or default


def read_file_bytes_and_md5(path: Path) -> tuple[bytes, str]:
    data = path.read_bytes()
    return data, hashlib.md5(data).hexdigest()


def looks_like_pdf(path: Path) -> bool:
    try:
        with path.open('rb') as fh:
            return fh.read(5) == b'%PDF-'
    except OSError:
        return False


def download_pdf_with_curl(pdf_url: str, *, timeout: int = 60) -> Dict[str, Any]:
    """Download a PDF to a temporary file with curl.

    curl is used here intentionally so the behavior matches the user's desired
    workflow: try a real file download first, then decide how to attach it.
    """
    filename = safe_filename_from_url(pdf_url)
    temp_dir = tempfile.mkdtemp(prefix='arxiv_to_zotero_')
    target = Path(temp_dir) / filename
    command = [
        'curl',
        '--location',
        '--fail',
        '--silent',
        '--show-error',
        '--max-time', str(max(10, int(timeout))),
        '--output', str(target),
        pdf_url,
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'ok': False,
            'error': f'curl_not_found:{exc}',
            'path': str(target),
            'filename': filename,
            'download_method': 'curl',
        }
    if completed.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'ok': False,
            'error': f"curl_failed:{(completed.stderr or completed.stdout or '').strip()}",
            'path': str(target),
            'filename': filename,
            'download_method': 'curl',
        }
    if not target.exists() or target.stat().st_size <= 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'ok': False,
            'error': 'empty_download',
            'path': str(target),
            'filename': filename,
            'download_method': 'curl',
        }
    if not looks_like_pdf(target):
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {
            'ok': False,
            'error': 'downloaded_file_is_not_pdf',
            'path': str(target),
            'filename': filename,
            'download_method': 'curl',
        }
    return {
        'ok': True,
        'path': str(target),
        'filename': filename,
        'filesize': target.stat().st_size,
        'download_method': 'curl',
    }


# ---------------------------------------------------------------------------
# 文本与 URL 工具 / Text and URL helpers
# ---------------------------------------------------------------------------
def round_seconds(value: float) -> float:
    return round(max(0.0, float(value)), 3)


def normalize_text(text: str | None) -> str:
    """归一化文本：统一大小写、空格和常见标点。

    Normalize text for robust title matching.
    """
    value = unicodedata.normalize('NFKC', (text or '').strip()).casefold()
    value = value.replace("–", "-").replace("—", "-").replace("：", ":")
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"[-\[\](){}<>\"'`“”‘’.,;:!?/\\|]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


STOPWORDS = {
    "a", "an", "the", "of", "for", "to", "on", "in", "with", "and", "or", "by",
    "from", "via", "using", "based", "at", "into", "towards", "under",
}

ARXIV_FIELD_PREFIXES = {"ti", "au", "abs", "co", "jr", "cat", "rn", "id", "all", "submittedDate"}
ARXIV_BOOLEAN_WORDS = {"AND", "OR", "ANDNOT", "TO"}
ARXIV_AUTO_QUOTE_FIELDS = {"ti", "au", "abs", "co", "jr", "cat", "rn", "id", "all"}
ARXIV_FIELD_PATTERN = re.compile(
    r"(?i)\b(?P<field>ti|au|abs|co|jr|cat|rn|id|all|submittedDate):"
)
ARXIV_BOOLEAN_BOUNDARY_PATTERN = re.compile(r"(?i)\s+(ANDNOT|AND|OR|TO)\b")


def normalize_query_string(raw: Any) -> str:
    value = str(raw or "").strip()
    return re.sub(r"\s+", " ", value)


def auto_quote_arxiv_field_phrases(query: str) -> Dict[str, Any]:
    """Protect common multi-word field values that forgot double quotes.

    Example:
        all:graph neural network OR ti:test time adaptation
    becomes:
        all:"graph neural network" OR ti:"test time adaptation"
    """
    value = normalize_query_string(query)
    if not value:
        return {
            "input_query": "",
            "effective_query": "",
            "modified": False,
            "fixes": [],
            "fix_count": 0,
        }

    out: List[str] = []
    fixes: List[Dict[str, str]] = []
    i = 0
    while i < len(value):
        match = ARXIV_FIELD_PATTERN.match(value, i)
        if not match:
            out.append(value[i])
            i += 1
            continue

        field = match.group("field").lower()
        prefix_text = value[i:match.end()]
        out.append(prefix_text)
        i = match.end()

        while i < len(value) and value[i].isspace():
            i += 1

        if field not in ARXIV_AUTO_QUOTE_FIELDS or i >= len(value) or value[i] in {'"', '[', '('}:
            continue

        start = i
        j = i
        in_quote = False
        paren_depth = 0
        bracket_depth = 0
        while j < len(value):
            ch = value[j]
            if ch == '"':
                in_quote = not in_quote
                j += 1
                continue
            if not in_quote:
                if ch == '[':
                    bracket_depth += 1
                elif ch == ']':
                    bracket_depth = max(0, bracket_depth - 1)
                elif ch == '(':
                    if paren_depth == 0 and bracket_depth == 0 and j == start:
                        break
                    paren_depth += 1
                elif ch == ')':
                    if paren_depth == 0 and bracket_depth == 0:
                        break
                    paren_depth = max(0, paren_depth - 1)
                if paren_depth == 0 and bracket_depth == 0 and ARXIV_BOOLEAN_BOUNDARY_PATTERN.match(value, j):
                    break
            j += 1

        if j == start:
            continue

        original_segment = value[start:j]
        stripped_segment = original_segment.rstrip()
        trailing_ws = original_segment[len(stripped_segment):]
        should_quote = False
        if (
            stripped_segment
            and " " in stripped_segment
            and '"' not in stripped_segment
            and '[' not in stripped_segment
            and ']' not in stripped_segment
            and '(' not in stripped_segment
            and ')' not in stripped_segment
            and ':' not in stripped_segment
        ):
            tokens = [tok for tok in stripped_segment.split() if tok]
            if len(tokens) >= 2 and not any(tok.upper() in ARXIV_BOOLEAN_WORDS for tok in tokens):
                should_quote = True

        if should_quote:
            replacement = f'"{stripped_segment}"'
            out.append(replacement)
            out.append(trailing_ws)
            fixes.append({
                "field": field,
                "original": stripped_segment,
                "replacement": replacement,
            })
        else:
            out.append(original_segment)
        i = j

    effective_query = normalize_query_string("".join(out))
    return {
        "input_query": value,
        "effective_query": effective_query,
        "modified": effective_query != value,
        "fixes": fixes,
        "fix_count": len(fixes),
    }


def _strip_arxiv_query_syntax(query: str) -> str:
    value = normalize_query_string(query)
    if not value:
        return ""
    value = re.sub(r"submittedDate:\[[^\]]+\]", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"\b(?:" + "|".join(sorted(ARXIV_FIELD_PREFIXES, key=len, reverse=True)) + r"):", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"\b(?:" + "|".join(sorted(ARXIV_BOOLEAN_WORDS, key=len, reverse=True)) + r")\b", " ", value, flags=re.IGNORECASE)
    value = re.sub(r"[()\[\]{}:]", " ", value)
    value = re.sub(r"\b\d{8,12}\b", " ", value)
    return value


def derive_cache_terms_from_arxiv_search_query(query: str, max_terms: int = 12) -> List[str]:
    """Build deduplicated single-word Zotero cache terms from a raw arXiv query."""
    value = _strip_arxiv_query_syntax(query).replace('"', ' ')
    tokens = [tok for tok in normalize_text(value).split() if tok and tok not in STOPWORDS]
    tokens = list(dict.fromkeys(tokens))
    if max_terms > 0:
        tokens = tokens[:max_terms]
    return tokens


def derive_cache_phrases_from_arxiv_search_query(query: str, max_phrases: int = 6) -> List[str]:
    """Extract quoted multi-word phrases for broader Zotero cache warm-up."""
    value = normalize_query_string(query)
    phrases: List[str] = []
    for raw in re.findall(r'"([^"\n]+)"', value):
        cleaned = normalize_text(raw)
        if not cleaned or ' ' not in cleaned:
            continue
        if cleaned not in phrases:
            phrases.append(cleaned)
        if max_phrases > 0 and len(phrases) >= max_phrases:
            break
    return phrases


def derive_cache_query_from_arxiv_search_query(query: str, max_terms: int = 12) -> str:
    """Backward-compatible human-readable cache summary string."""
    return " ".join(derive_cache_terms_from_arxiv_search_query(query, max_terms=max_terms))


def derive_storage_tags_from_arxiv_search_query(query: str, *, max_terms: int = 12, max_phrases: int = 6) -> List[str]:
    """Build Zotero tags from the arXiv query for later recall in the library."""
    value = normalize_query_string(query)
    tags: List[str] = []
    for raw in re.findall(r'"([^"\n]+)"', value):
        cleaned = re.sub(r"\s+", " ", raw).strip()
        if cleaned and cleaned not in tags:
            tags.append(cleaned)
        if max_phrases > 0 and len(tags) >= max_phrases:
            break

    for token in derive_cache_terms_from_arxiv_search_query(query, max_terms=max_terms):
        if token not in tags:
            tags.append(token)
    return tags


def infer_venue_from_arxiv_metadata(comment: str | None, journal_ref: str | None) -> str | None:
    journal = (journal_ref or '').strip()
    if journal:
        return journal
    comment_text = re.sub(r"\s+", " ", (comment or '').strip())
    if not comment_text:
        return None

    patterns = [
        r'(?i)accepted\s+for\s+presentation\s+to\s+the\s+(.+?)(?:\.|;|$)',
        r'(?i)accepted\s+at\s+the\s+(.+?)(?:\.|;|$)',
        r'(?i)accepted\s+to\s+the\s+(.+?)(?:\.|;|$)',
        r'(?i)to\s+appear\s+in\s+the\s+(.+?)(?:\.|;|$)',
        r'(?i)presented\s+at\s+the\s+(.+?)(?:\.|;|$)',
        r'(?i)published\s+in\s+the\s+(.+?)(?:\.|;|$)',
    ]
    for pattern in patterns:
        match = re.search(pattern, comment_text)
        if match:
            venue = re.sub(r"\s+", " ", match.group(1)).strip(" .,;:-")
            if venue:
                return venue
    return None


# ---------------------------------------------------------------------------
# 配置 / Config
# ---------------------------------------------------------------------------
def load_simple_env(path: Path) -> None:
    """Load KEY=VALUE pairs from a fixed .env file without overriding existing env vars."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#") or "=" not in raw:
            continue
        key, value = raw.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_skill_config(config_arg: str | None = None) -> Dict[str, Any]:
    """Load config from an explicit path or the fixed OpenClaw location."""
    env_path = fixed_env_path()
    config_path = Path(config_arg).expanduser() if config_arg and str(config_arg).strip() else fixed_config_path()
    load_simple_env(env_path)
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}. Expected non-secret config at {config_path} and secrets in {env_path}."
        )
    return json.loads(config_path.read_text(encoding="utf-8"))

def zotero_runtime_available(config: Dict[str, Any]) -> bool:
    """Whether Zotero can be contacted at command time without blocking startup."""
    zotero = config.get("zotero") or {}
    return bool(zotero.get("library_id") and zotero.get("library_type") and resolve_zotero_api_key(config))


def resolve_zotero_api_key(config: Dict[str, Any]) -> str:
    """Resolve the Zotero API key from config compatibility fields or environment."""
    zotero = config.get("zotero") or {}
    api_key = str(zotero.get("api_key") or "").strip()
    if api_key and not api_key.startswith("YOUR_"):
        return api_key
    env_name = str(zotero.get("api_key_env") or "ZOTERO_API_KEY").strip()
    return os.getenv(env_name, "").strip()


def validate_config(config: Dict[str, Any], command: str) -> None:
    zotero = config.get("zotero") or {}
    if command in {"search"}:
        return
    missing = [
        field
        for field in ["library_id", "library_type"]
        if not zotero.get(field) or str(zotero.get(field)).startswith("YOUR_")
    ]
    library_type = str(zotero.get("library_type") or "").strip()
    if library_type and library_type not in {"user", "group"}:
        raise ValueError("zotero.library_type must be 'user' or 'group'")
    if command in {"import", "cleanup"} and not resolve_zotero_api_key(config):
        missing.append(f"api_key_env:{zotero.get('api_key_env', 'ZOTERO_API_KEY')}")
    if missing:
        raise ValueError(f"Missing Zotero config fields: {missing}")


# ---------------------------------------------------------------------------
# 数据源 / Sources
# ---------------------------------------------------------------------------
def query_arxiv(query: str, config: Dict[str, Any], timeout: int = 20) -> List[PaperRecord]:
    cfg = ((config.get("sources") or {}).get("arxiv") or {})
    if not cfg.get("enabled", True):
        return []
    prepared_query = auto_quote_arxiv_field_phrases(query)
    search_query = prepared_query["effective_query"]
    if not search_query:
        return []
    max_results = int(cfg.get("max_results", 50))
    sort_by = cfg.get("sort_by", "submittedDate")
    request_timeout = int(cfg.get("request_timeout_seconds", timeout or 30))
    retries = int(cfg.get("max_retries", 3))
    min_interval = float(cfg.get("min_interval_seconds", 3))
    retry_sleep = float(cfg.get("retry_sleep_seconds", 10))
    max_retry_sleep = float(cfg.get("max_retry_sleep_seconds", 120))
    params = {
        "search_query": search_query,
        "sortBy": sort_by,
        "sortOrder": "descending",
        "max_results": max_results,
    }
    url = "https://export.arxiv.org/api/query"

    last_exc: Exception | None = None
    response: HttpResponse | None = None
    for attempt in range(retries + 1):
        if attempt > 0:
            sleep_for = min(max_retry_sleep, retry_sleep * (2 ** (attempt - 1)))
            time.sleep(sleep_for)
        try:
            response = http_request("GET", url, params=params, timeout=request_timeout, headers={"User-Agent": HTTP_USER_AGENT})
            if response.status_code in {429, 502, 503, 504}:
                last_exc = RuntimeError(f"arXiv temporary failure: HTTP {response.status_code}")
                if attempt == retries:
                    raise last_exc
                continue
            ensure_success(response, "arXiv request")
            break
        except (urllib.error.URLError, socket.timeout, TimeoutError, RuntimeError) as exc:
            last_exc = exc
            if attempt == retries:
                raise
            continue

    if response is None:
        if last_exc:
            raise last_exc
        raise RuntimeError("arXiv request failed without a response")

    time.sleep(min_interval)

    root = ET.fromstring(response.text)
    items: List[PaperRecord] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        title = (entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        abstract = (entry.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        comments = (entry.findtext("arxiv:comment", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        journal_ref = (entry.findtext("arxiv:journal_ref", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        doi = (entry.findtext("arxiv:doi", default="", namespaces=ATOM_NS) or "").strip().replace("\n", " ")
        venue = infer_venue_from_arxiv_metadata(comments, journal_ref)
        published_raw = (entry.findtext("atom:published", default="", namespaces=ATOM_NS) or "").strip()
        published_dt = None
        if published_raw:
            try:
                published_dt = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
            except ValueError:
                published_dt = None
        authors = [
            (author.findtext("atom:name", default="", namespaces=ATOM_NS) or "").strip()
            for author in entry.findall("atom:author", ATOM_NS)
        ]
        entry_id = (entry.findtext("atom:id", default="", namespaces=ATOM_NS) or "").strip()
        arxiv_id = entry_id.rstrip("/").split("/")[-1] if entry_id else None
        pdf_url = None
        for link in entry.findall("atom:link", ATOM_NS):
            if link.get("title") == "pdf":
                pdf_url = link.get("href")
                break
        items.append(
            PaperRecord(
                title=title,
                authors=[a for a in authors if a],
                abstract=abstract or None,
                year=published_dt.year if published_dt else None,
                venue=venue or None,
                comments=comments or None,
                journal_ref=journal_ref or None,
                doi=doi or None,
                arxiv_id=arxiv_id,
                url=entry_id.replace("http://", "https://") if entry_id else None,
                pdf_url=(pdf_url or "").replace("http://", "https://") or None,
                source_names=["arxiv"],
                source_payloads={"arxiv": {"raw_id": entry_id, "query": search_query}},
            )
        )
    return items

def merge_record(base: PaperRecord, incoming: PaperRecord) -> None:
    for field_name in ["abstract", "year", "venue", "comments", "journal_ref", "doi", "arxiv_id", "url", "pdf_url"]:
        if not getattr(base, field_name) and getattr(incoming, field_name):
            setattr(base, field_name, getattr(incoming, field_name))
    if base.citation_count is None and incoming.citation_count is not None:
        base.citation_count = incoming.citation_count
    base.source_names = sorted(set(base.source_names + incoming.source_names))
    base.tags = sorted(set(base.tags + incoming.tags))
    for key, value in incoming.source_payloads.items():
        base.source_payloads.setdefault(key, value)




def title_fingerprint(title: str | None) -> str:
    """Build a normalized title fingerprint for dedupe."""
    tokens = [tok for tok in normalize_text(title).split() if tok and tok not in STOPWORDS]
    return " ".join(tokens)


def normalized_title_prefix_match(a: str | None, b: str | None, min_chars: int = 42) -> bool:
    """Return True when one normalized title is a sufficiently long prefix of the other."""
    na = normalize_text(a)
    nb = normalize_text(b)
    if not na or not nb:
        return False
    shorter, longer = (na, nb) if len(na) <= len(nb) else (nb, na)
    return len(shorter) >= min_chars and longer.startswith(shorter)


def exact_normalized_title_match(a: str | None, b: str | None) -> bool:
    na = normalize_text(a)
    nb = normalize_text(b)
    return bool(na and nb and na == nb)


def titles_look_equivalent(a: str | None, b: str | None) -> bool:
    """Compatibility helper for strict title-based dedupe."""
    return exact_normalized_title_match(a, b) or normalized_title_prefix_match(a, b, min_chars=42)


def canonical_url(url: str | None) -> str:
    """Lightweight URL canonicalization for de-duplication keys."""
    raw = (url or "").strip()
    if not raw:
        return ""
    parsed = urllib.parse.urlparse(raw)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return urllib.parse.urlunparse((scheme, netloc, path, "", "", ""))


def resolve_pdf_candidates_from_item_url(item_url: str | None) -> List[str]:
    """Build likely PDF URLs from the parent item's saved URL."""
    candidates: List[str] = []

    def add(url: str | None) -> None:
        value = (url or "").strip()
        if not value:
            return
        value = value.replace("http://", "https://")
        if value not in candidates:
            candidates.append(value)

    raw_url = (item_url or "").strip()
    if not raw_url:
        return candidates

    normalized = raw_url.replace("http://", "https://")
    if normalized.lower().endswith(".pdf"):
        add(normalized)
        return candidates

    if "arxiv.org/abs/" in normalized:
        base = normalized.replace("/abs/", "/pdf/")
        add(base + ".pdf" if not base.endswith(".pdf") else base)
        add(base[:-4] if base.endswith(".pdf") else base)
        return candidates

    if "arxiv.org/pdf/" in normalized:
        add(normalized if normalized.lower().endswith(".pdf") else normalized + ".pdf")
        add(normalized[:-4] if normalized.lower().endswith(".pdf") else normalized)
        return candidates

    add(normalized)
    return candidates


def resolve_pdf_url(record: PaperRecord) -> str | None:
    candidates = resolve_pdf_candidates_from_item_url(record.url)
    return candidates[0] if candidates else None


def extract_arxiv_id(value: str | None) -> str | None:
    """Extract a normalized arXiv id from a field or URL."""
    raw = (value or "").strip()
    if not raw:
        return None
    raw = raw.replace("arXiv:", "").replace("arxiv:", "").strip()
    if "arxiv.org/" in raw:
        match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#]+)", raw)
        if match:
            raw = match.group(1)
    raw = raw.removesuffix(".pdf").strip("/")
    return raw or None


def candidate_keys(record: PaperRecord) -> List[str]:
    keys: List[str] = []
    title_key = title_fingerprint(record.title)
    if title_key:
        keys.append(f"title:{title_key}")
    if record.doi:
        keys.append(f"doi:{normalize_text(record.doi)}")
    if record.arxiv_id:
        keys.append(f"arxiv:{normalize_text(record.arxiv_id)}")
    if record.url:
        url = canonical_url(record.url)
        if url:
            keys.append(f"url:{url}")
    return keys


def dedupe_records(records: Iterable[PaperRecord]) -> List[PaperRecord]:
    merged: Dict[str, PaperRecord] = {}
    title_index: List[tuple[str, str]] = []

    for record in records:
        keys = candidate_keys(record)
        title_key = title_fingerprint(record.title)
        chosen = None

        for key in keys:
            if key in merged:
                chosen = key
                break

        if not chosen and title_key:
            for existing_title, storage_key in title_index:
                if titles_look_equivalent(existing_title, title_key):
                    chosen = storage_key
                    break

        if not chosen:
            chosen = keys[0] if keys else f"raw:{len(merged)}"
            merged[chosen] = record
            if title_key:
                title_index.append((title_key, chosen))
            continue

        merge_record(merged[chosen], record)

    return list(merged.values())


# ---------------------------------------------------------------------------
# Zotero 客户端 / Zotero client
# ---------------------------------------------------------------------------
class ZoteroClient:
    def __init__(self, library_id: str, library_type: str, api_key: str, timeout: int = 20):
        self.library_id = str(library_id)
        self.library_type = library_type
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = f"https://api.zotero.org/{library_type}s/{library_id}"
        self.headers = {"Zotero-API-Key": api_key, "Zotero-API-Version": "3"}
        self.force_link_mode = False
        self._resolved_target_collection_key: str | None = None

    def _get(self, path: str, **params: Any) -> HttpResponse:
        response = http_request("GET", f"{self.base_url}{path}", headers=self.headers, params=params, timeout=self.timeout)
        return ensure_success(response, f"Zotero GET {path}")

    def _post_json(self, path: str, payload: Any) -> HttpResponse:
        response = http_request(
            "POST",
            f"{self.base_url}{path}",
            headers={**self.headers, "Content-Type": "application/json", "Zotero-Write-Token": secrets.token_hex(16)},
            data=json.dumps(payload),
            timeout=self.timeout,
        )
        return ensure_success(response, f"Zotero POST {path}")


    def _collection_lookup_name(self, config: Dict[str, Any]) -> str:
        zotero_cfg = config.get("zotero") or {}
        return str(zotero_cfg.get("target_collection_name") or DEFAULT_TARGET_COLLECTION_NAME).strip()

    def get_collection(self, collection_key: str) -> Dict[str, Any] | None:
        key = str(collection_key or "").strip()
        if not key:
            return None
        response = http_request("GET", f"{self.base_url}/collections/{key}", headers=self.headers, timeout=self.timeout)
        if response.status_code == 404:
            return None
        return ensure_success(response, f"Zotero GET /collections/{key}").json()

    def list_top_collections(self, *, max_rows: int = 200) -> List[Dict[str, Any]]:
        rows_all: List[Dict[str, Any]] = []
        start = 0
        remaining = max(0, int(max_rows))
        while remaining > 0:
            batch_limit = min(100, remaining)
            rows = self._get("/collections/top", limit=batch_limit, start=start, format="json").json()
            if not isinstance(rows, list) or not rows:
                break
            rows_all.extend(rows)
            if len(rows) < batch_limit:
                break
            start += batch_limit
            remaining -= batch_limit
        return rows_all

    def find_top_collection_key_by_name(self, name: str) -> str:
        wanted = normalize_text(name)
        if not wanted:
            return ""
        for row in self.list_top_collections():
            data = row.get("data") or {}
            if normalize_text(data.get("name")) == wanted:
                return str(row.get("key") or data.get("key") or "").strip()
        return ""

    def create_collection(self, name: str, parent_collection: str | None = None) -> str:
        payload_obj: Dict[str, Any] = {"name": str(name).strip()}
        parent = str(parent_collection or "").strip()
        if parent:
            payload_obj["parentCollection"] = parent
        response = self._post_json("/collections", [payload_obj])
        data = response.json()
        success = ((data.get("successful") or {}).get("0") or {})
        return str(success.get("key") or "").strip()

    def resolve_target_collection_key(self, config: Dict[str, Any], *, create_if_missing: bool) -> str:
        if self._resolved_target_collection_key:
            return self._resolved_target_collection_key
        if self._resolved_target_collection_key == "" and not create_if_missing:
            return ""

        zotero_cfg = config.get("zotero") or {}
        configured_key = str(zotero_cfg.get("target_collection_key") or "").strip()
        if configured_key:
            if self.get_collection(configured_key):
                self._resolved_target_collection_key = configured_key
                return configured_key

        collection_name = self._collection_lookup_name(config)
        found_key = self.find_top_collection_key_by_name(collection_name)
        if found_key:
            self._resolved_target_collection_key = found_key
            return found_key

        if not create_if_missing or not bool(zotero_cfg.get("auto_create_collection", True)) or not collection_name:
            if not create_if_missing:
                self._resolved_target_collection_key = ""
            return ""

        created_key = self.create_collection(collection_name)
        self._resolved_target_collection_key = created_key
        return created_key


    def create_item(self, paper: PaperRecord, config: Dict[str, Any]) -> Dict[str, Any]:
        zotero_cfg = config.get("zotero") or {}
        item_url = (paper.url or "").strip()
        item_type = self._infer_item_type(paper)
        target_collection_key = self.resolve_target_collection_key(
            config,
            create_if_missing=bool(zotero_cfg.get("auto_create_collection", True)),
        )
        payload_item = {
            "itemType": item_type,
            "title": paper.title,
            "creators": [self._author_to_creator(name) for name in paper.authors],
            "abstractNote": paper.abstract or "",
            "date": str(paper.year) if paper.year else "",
            "url": item_url,
            "DOI": paper.doi or "",
            "tags": [{"tag": tag} for tag in sorted(set((zotero_cfg.get("default_tags") or [DEFAULT_SKILL_TAG]) + (paper.tags or [])))],
            "extra": self._build_extra(paper),
            **self._item_specific_fields(paper, item_type),
            **({"collections": [target_collection_key]} if target_collection_key else {}),
        }
        payload = [payload_item]
        started = time.perf_counter()
        response = self._post_json("/items", payload)
        data = response.json()
        success = ((data.get("successful") or {}).get("0") or {})
        item_key = success.get("key")
        create_seconds = round_seconds(time.perf_counter() - started)
        if not item_key:
            return {"created": False, "response": data, "timings": {"create_item_seconds": create_seconds}}

        pdf_started = time.perf_counter()
        pdf_result = self.attach_pdf(item_key, item_url, paper, config)
        pdf_seconds = round_seconds(time.perf_counter() - pdf_started)
        return {
            "created": True,
            "item_key": item_key,
            "pdf_attached": bool(pdf_result.get("attached")),
            "pdf_attachment_mode": pdf_result.get("mode"),
            "pdf_attachment_status": pdf_result.get("status"),
            "pdf_file_uploaded": pdf_result.get("mode") == "imported_url",
            "pdf_link_attached": pdf_result.get("mode") == "linked_url",
            "pdf_attachment_key": pdf_result.get("attachment_key"),
            "pdf_attachment_error": pdf_result.get("error"),
            "timings": {
                "create_item_seconds": create_seconds,
                "attach_pdf_seconds": pdf_seconds,
            },
        }


    def attach_pdf(self, parent_key: str, parent_url: str, paper: PaperRecord, config: Dict[str, Any]) -> Dict[str, Any]:
        """Attach a real PDF first; after one HTTP 413, use URI mode for the rest of the run."""
        candidates = resolve_pdf_candidates_from_item_url(parent_url)
        if not candidates:
            return {'attached': False, 'mode': None, 'status': 'no_pdf_candidate'}

        if self.force_link_mode:
            for candidate in candidates:
                fallback_key = self.create_link_attachment_item(parent_key, candidate, config)
                if fallback_key:
                    paper.pdf_url = candidate
                    return {
                        'attached': True,
                        'mode': 'linked_url',
                        'status': 'forced_link_mode_after_413',
                        'attachment_key': fallback_key,
                    }
            return {
                'attached': False,
                'mode': None,
                'status': 'forced_link_mode_failed',
                'error': 'failed_to_create_link_attachment_after_413',
            }

        errors: List[str] = []
        for candidate in candidates:
            download = download_pdf_with_curl(candidate, timeout=max(30, self.timeout * 3))
            if not download.get('ok'):
                errors.append(str(download.get('error') or 'download_failed'))
                continue
            file_path = Path(str(download['path']))
            try:
                upload_result = self.create_imported_pdf_attachment_item(parent_key, candidate, file_path, config)
                if upload_result.get('quota_exceeded'):
                    self.force_link_mode = True
                    attachment_key = upload_result.get('attachment_key')
                    if attachment_key:
                        try:
                            self.delete_item(attachment_key)
                        except Exception:
                            pass
                    fallback_key = self.create_link_attachment_item(parent_key, candidate, config)
                    if fallback_key:
                        paper.pdf_url = candidate
                        return {
                            'attached': True,
                            'mode': 'linked_url',
                            'status': 'quota_fallback_to_linked_url',
                            'attachment_key': fallback_key,
                            'download_method': download.get('download_method'),
                        }
                    return {
                        'attached': False,
                        'mode': None,
                        'status': 'quota_fallback_failed',
                        'error': 'quota_exceeded_and_link_creation_failed',
                    }
                if upload_result.get('attached'):
                    paper.pdf_url = candidate
                    return upload_result
                errors.append(str(upload_result.get('error') or 'upload_failed'))
            finally:
                try:
                    file_path.unlink(missing_ok=True)
                    file_path.parent.rmdir()
                except OSError:
                    pass

        return {
            'attached': False,
            'mode': None,
            'status': 'pdf_download_or_upload_failed',
            'error': '; '.join(errors[:5]) if errors else 'unknown_pdf_attachment_failure',
        }

    def create_imported_pdf_attachment_item(self, parent_key: str, pdf_url: str, file_path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
        attachment_key = self.create_imported_attachment_item(parent_key, pdf_url, file_path.name, config)
        if not attachment_key:
            return {
                'attached': False,
                'mode': None,
                'status': 'attachment_item_creation_failed',
                'error': 'failed_to_create_imported_attachment_item',
            }
        try:
            upload_result = self.upload_attachment_file(attachment_key, file_path)
            upload_result['attachment_key'] = attachment_key
            if upload_result.get('quota_exceeded'):
                upload_result['mode'] = None
            else:
                upload_result['mode'] = 'imported_url' if upload_result.get('attached') else None
            return upload_result
        except Exception as exc:
            try:
                self.delete_item(attachment_key)
            except Exception:
                pass
            return {
                'attached': False,
                'mode': None,
                'status': 'attachment_upload_failed',
                'attachment_key': attachment_key,
                'error': f'{type(exc).__name__}: {exc}',
            }

    def create_imported_attachment_item(self, parent_key: str, pdf_url: str, filename: str, config: Dict[str, Any]) -> str | None:
        payload = [{
            'itemType': 'attachment',
            'parentItem': parent_key,
            'linkMode': 'imported_url',
            'title': 'PDF',
            'url': pdf_url,
            'contentType': 'application/pdf',
            'filename': filename,
            'note': '',
            'relations': {},
            'charset': '',
            'md5': None,
            'mtime': None,
        }]
        response = self._post_json('/items', payload)
        data = response.json()
        success = ((data.get('successful') or {}).get('0') or {})
        return success.get('key')

    def upload_attachment_file(self, attachment_key: str, file_path: Path) -> Dict[str, Any]:
        file_bytes, file_md5 = read_file_bytes_and_md5(file_path)
        metadata = {
            'md5': file_md5,
            'filename': file_path.name,
            'filesize': len(file_bytes),
            'mtime': int(file_path.stat().st_mtime * 1000),
        }
        auth_response = http_request(
            'POST',
            f'{self.base_url}/items/{attachment_key}/file',
            headers={
                **self.headers,
                'If-None-Match': '*',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data=urllib.parse.urlencode(metadata),
            timeout=max(self.timeout, 30),
        )
        if auth_response.status_code == 413:
            return {
                'attached': False,
                'quota_exceeded': True,
                'status': 'quota_exceeded',
                'error': 'HTTP 413 Request Entity Too Large',
            }
        ensure_success(auth_response, f'Zotero file upload authorization for {attachment_key}')
        auth_data = auth_response.json()
        if auth_data.get('exists') == 1:
            return {
                'attached': True,
                'quota_exceeded': False,
                'status': 'already_exists_on_server',
            }
        upload_url = auth_data.get('url')
        upload_key = auth_data.get('uploadKey')
        content_type = auth_data.get('contentType')
        prefix = auth_data.get('prefix')
        suffix = auth_data.get('suffix')
        if not all([upload_url, upload_key, content_type, prefix is not None, suffix is not None]):
            raise RuntimeError('incomplete_upload_authorization_response')
        upload_response = http_request(
            'POST',
            str(upload_url),
            headers={'Content-Type': str(content_type)},
            data=prefix.encode('utf-8') + file_bytes + suffix.encode('utf-8'),
            timeout=max(self.timeout * 3, 120),
        )
        ensure_success(upload_response, f'Zotero binary upload for {attachment_key}')
        register_response = http_request(
            'POST',
            f'{self.base_url}/items/{attachment_key}/file',
            headers={
                **self.headers,
                'If-None-Match': '*',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data=urllib.parse.urlencode({'upload': upload_key}),
            timeout=max(self.timeout, 30),
        )
        ensure_success(register_response, f'Zotero upload registration for {attachment_key}')
        return {
            'attached': True,
            'quota_exceeded': False,
            'status': 'uploaded_to_zotero',
        }

    def create_link_attachment_item(self, parent_key: str, pdf_url: str, config: Dict[str, Any]) -> str | None:
        payload = [{
            "itemType": "attachment",
            "parentItem": parent_key,
            "linkMode": "linked_url",
            "title": "PDF",
            "url": pdf_url,
            "contentType": "application/pdf",
            "note": "",
            "relations": {},
        }]
        response = self._post_json("/items", payload)
        data = response.json()
        success = ((data.get("successful") or {}).get("0") or {})
        return success.get("key")

    def delete_item(self, item_key: str) -> bool:
        response = self._get(f"/items/{item_key}")
        version = response.headers.get("Last-Modified-Version")
        delete_response = http_request(
            "DELETE",
            f"{self.base_url}/items/{item_key}",
            headers={**self.headers, "If-Unmodified-Since-Version": str(version)},
            timeout=self.timeout,
        )
        return delete_response.status_code == 204


    @staticmethod
    def author_to_creator(name: str) -> Dict[str, str]:
        parts = [part for part in name.strip().split() if part]
        if len(parts) <= 1:
            return {"creatorType": "author", "firstName": "", "lastName": name.strip()}
        return {"creatorType": "author", "firstName": " ".join(parts[:-1]), "lastName": parts[-1]}

    def _author_to_creator(self, name: str) -> Dict[str, str]:
        return self.author_to_creator(name)

    @staticmethod
    def _infer_item_type(paper: PaperRecord) -> str:
        venue = normalize_text(paper.venue or paper.journal_ref)
        comments = normalize_text(paper.comments)
        if any(hint in venue for hint in ["journal", "transactions", "letters", "review", "magazine"]):
            return "journalArticle"
        if any(hint in venue for hint in ["conference", "symposium", "workshop", "meeting", "proceedings"]):
            return "conferencePaper"
        if comments and ("accepted" in comments or "presentation" in comments or "conference" in comments or "workshop" in comments):
            return "conferencePaper"
        if paper.arxiv_id and not venue:
            return "preprint"
        return "conferencePaper"

    @staticmethod
    def _item_specific_fields(paper: PaperRecord, item_type: str) -> Dict[str, str]:
        venue = (paper.venue or paper.journal_ref or "").strip()
        fields: Dict[str, str] = {}
        if item_type == "journalArticle":
            fields["publicationTitle"] = venue
            return fields
        if item_type == "conferencePaper":
            if venue:
                fields["proceedingsTitle"] = venue
                fields["conferenceName"] = venue
            return fields
        if venue:
            fields["publicationTitle"] = venue
        return fields

    @staticmethod
    def _build_extra(paper: PaperRecord) -> str:
        lines: List[str] = []
        if paper.arxiv_id:
            lines.append(f"arXiv: {paper.arxiv_id}")
        if paper.journal_ref:
            lines.append(f"Journal Reference: {paper.journal_ref}")
        if paper.comments:
            lines.append(f"Comments: {paper.comments}")
        if paper.source_names:
            lines.append(f"Sources: {', '.join(sorted(set(paper.source_names)))}")
        return "\n".join(lines)


def build_cache_query(query: str, max_terms: int = 12) -> str:
    return derive_cache_query_from_arxiv_search_query(query, max_terms=max_terms)


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return max(1, default)
    return max(1, parsed)


def _fetch_zotero_cache_rows(
    client: ZoteroClient,
    *,
    endpoint: str = "/items/top",
    q: str | None = None,
    qmode: str | None = None,
    tag: str | None = None,
    max_rows: int = 100,
    sort: str | None = None,
    direction: str | None = None,
) -> tuple[List[Dict[str, Any]], int]:
    rows_all: List[Dict[str, Any]] = []
    pages = 0
    start = 0
    remaining = max(0, int(max_rows))
    while remaining > 0:
        batch_limit = min(100, remaining)
        params: Dict[str, Any] = {"limit": batch_limit, "start": start, "format": "json"}
        if q:
            params["q"] = q
        if qmode:
            params["qmode"] = qmode
        if tag:
            params["tag"] = tag
        if sort:
            params["sort"] = sort
        if direction:
            params["direction"] = direction
        rows = client._get(endpoint, **params).json()
        pages += 1
        if not isinstance(rows, list) or not rows:
            break
        rows_all.extend(rows)
        if len(rows) < batch_limit:
            break
        start += batch_limit
        remaining -= batch_limit
    return rows_all, pages

def _cache_row_type_ok(row: Dict[str, Any]) -> bool:
    data = row.get("data") or {}
    return data.get("itemType") in {"journalArticle", "conferencePaper", "preprint"}


def _cache_logical_keys_from_row(row: Dict[str, Any]) -> List[str]:
    data = row.get("data") or {}
    keys: List[str] = []
    norm_title = normalize_text(data.get("title"))
    if norm_title:
        keys.append(f"title:{norm_title}")
    arxiv_id = extract_arxiv_id((data.get("extra") or "")) or extract_arxiv_id(data.get("url"))
    if arxiv_id:
        keys.append(f"arxiv:{arxiv_id}")
    canonical = canonical_url(data.get("url"))
    if canonical:
        keys.append(f"url:{canonical}")
    row_key = str(row.get("key") or "").strip()
    if row_key:
        keys.append(f"item:{row_key}")
    return keys


def _cache_add_row(cache: Dict[str, Any], row: Dict[str, Any]) -> None:
    if not _cache_row_type_ok(row):
        return
    data = row.get("data") or {}
    logical_keys = _cache_logical_keys_from_row(row)
    primary_keys = [key for key in logical_keys if not key.startswith("item:")]
    if primary_keys and any(key in cache["seen_keys"] for key in primary_keys):
        return
    if not logical_keys:
        return
    for key in logical_keys:
        cache["seen_keys"].add(key)
    cache["rows"].append(row)
    norm_title = normalize_text(data.get("title"))
    if norm_title:
        cache["title_pairs"].append((norm_title, row))
        cache["title_exact"].setdefault(norm_title, row)
    existing_arxiv = extract_arxiv_id((data.get("extra") or "")) or extract_arxiv_id(data.get("url"))
    if existing_arxiv:
        cache["arxiv"].setdefault(existing_arxiv, row)


def build_existing_cache(client: ZoteroClient, query: str, config: Dict[str, Any]) -> Dict[str, Any]:
    started = time.perf_counter()
    dedupe_cfg = config.get("dedupe") or {}
    zotero_cfg = config.get("zotero") or {}
    term_limit = int(dedupe_cfg.get("zotero_cache_term_limit", 12) or 12)
    per_query_rows = _positive_int(dedupe_cfg.get("zotero_cache_rows_per_query", 100), 100)
    qmode = "everything" if bool(dedupe_cfg.get("zotero_cache_qmode_everything", True)) else None
    include_skill_tag_cache = bool(dedupe_cfg.get("include_default_tag_cache", True))
    include_target_collection_cache = bool(dedupe_cfg.get("include_target_collection_cache", True))
    terms = derive_cache_terms_from_arxiv_search_query(query, max_terms=term_limit)
    cache_query = build_cache_query(query, max_terms=term_limit)
    cache: Dict[str, Any] = {
        "enabled": True,
        "rows": [],
        "seen_keys": set(),
        "title_exact": {},
        "title_pairs": [],
        "arxiv": {},
        "query": query,
        "cache_query": cache_query,
        "cache_terms": terms,
        "cache_phrases": [],
        "cache_strategy": "term_by_term_plus_skill_scope",
        "fetches": [],
        "pages": 0,
        "row_count": 0,
        "seconds": 0.0,
    }

    def add_fetch(label: str, rows: List[Dict[str, Any]], pages: int) -> None:
        cache["pages"] += pages
        before = len(cache["rows"])
        for row in rows:
            _cache_add_row(cache, row)
        cache["fetches"].append({
            "label": label,
            "rows": len(rows),
            "pages": pages,
            "new_rows": len(cache["rows"]) - before,
        })

    for term in terms:
        rows, pages = _fetch_zotero_cache_rows(
            client,
            q=term,
            qmode=qmode,
            max_rows=per_query_rows,
            sort="dateModified",
            direction="desc",
        )
        add_fetch(f"term:{term}", rows, pages)

    if include_skill_tag_cache:
        for tag in [str(tag).strip() for tag in (zotero_cfg.get("default_tags") or []) if str(tag).strip()]:
            rows, pages = _fetch_zotero_cache_rows(
                client,
                tag=tag,
                max_rows=per_query_rows,
                sort="dateModified",
                direction="desc",
            )
            add_fetch(f"tag:{tag}", rows, pages)

    if include_target_collection_cache:
        collection_key = client.resolve_target_collection_key(config, create_if_missing=False)
        if collection_key:
            rows, pages = _fetch_zotero_cache_rows(
                client,
                endpoint=f"/collections/{collection_key}/items/top",
                max_rows=per_query_rows,
                sort="dateModified",
                direction="desc",
            )
            add_fetch(f"collection:{collection_key}", rows, pages)

    cache["row_count"] = len(cache["rows"])
    cache["seconds"] = round_seconds(time.perf_counter() - started)
    return cache

def find_existing_in_cache(cache: Dict[str, Any] | None, paper: PaperRecord, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not cache or not cache.get("enabled"):
        return None
    dedupe_cfg = config.get("dedupe") or {}
    min_chars = int(dedupe_cfg.get("zotero_title_prefix_min_chars", 42))
    norm_title = normalize_text(paper.title)
    if norm_title:
        exact = cache.get("title_exact", {}).get(norm_title)
        if exact:
            return exact
    paper_arxiv_id = extract_arxiv_id(paper.arxiv_id) or extract_arxiv_id(paper.url) or extract_arxiv_id(paper.pdf_url)
    if paper_arxiv_id:
        cached = cache.get("arxiv", {}).get(paper_arxiv_id)
        if cached:
            return cached
    for existing_title, row in cache.get("title_pairs", []):
        if existing_title and normalized_title_prefix_match(existing_title, paper.title, min_chars=min_chars):
            return row
    return None


def update_existing_cache(cache: Dict[str, Any] | None, paper: PaperRecord, item_key: str) -> None:
    if not cache or not cache.get("enabled") or not item_key:
        return
    row = {
        "key": item_key,
        "data": {
            "title": paper.title,
            "itemType": ZoteroClient._infer_item_type(paper),
            "url": paper.url or "",
            "extra": ZoteroClient._build_extra(paper),
        },
    }
    _cache_add_row(cache, row)
    cache["row_count"] = len(cache.get("rows") or [])


# ---------------------------------------------------------------------------
# 主流程 / Pipeline
# ---------------------------------------------------------------------------
def apply_record_policy(record: PaperRecord, query: str, config: Dict[str, Any]) -> PaperRecord:
    zotero_cfg = config.get("zotero") or {}
    # Keep Zotero tagging deterministic: every imported paper receives only the skill-level default tags.
    record.tags = sorted(set(list(zotero_cfg.get("default_tags", [DEFAULT_SKILL_TAG]))))
    if not record.venue:
        record.venue = infer_venue_from_arxiv_metadata(record.comments, record.journal_ref)
    record.pdf_url = resolve_pdf_url(record)
    return record

def search_once(query: str, config: Dict[str, Any], *, prepared_query: Dict[str, Any] | None = None) -> Dict[str, Any]:
    total_started = time.perf_counter()
    all_records: List[PaperRecord] = []
    source_errors: List[Dict[str, str]] = []
    source_status: List[Dict[str, Any]] = []
    timings: Dict[str, Any] = {
        "arxiv_seconds": 0.0,
        "dedupe_seconds": 0.0,
        "total_seconds": 0.0,
    }
    query_info = prepared_query or auto_quote_arxiv_field_phrases(query)

    arxiv_started = time.perf_counter()
    try:
        arxiv_records = query_arxiv(query_info.get("effective_query") or query, config)
        all_records.extend(arxiv_records)
        source_status.append({"source": "arxiv", "used": True, "count": len(arxiv_records)})
    except Exception as exc:  # noqa: BLE001
        source_errors.append({"source": "arxiv", "error": f"{type(exc).__name__}: {exc}"})
        source_status.append({"source": "arxiv", "used": False, "reason": f"{type(exc).__name__}: {exc}"})
    timings["arxiv_seconds"] = round_seconds(time.perf_counter() - arxiv_started)

    dedupe_started = time.perf_counter()
    final_records = [apply_record_policy(record, query, config) for record in dedupe_records(all_records)]
    timings["dedupe_seconds"] = round_seconds(time.perf_counter() - dedupe_started)
    timings["total_seconds"] = round_seconds(time.perf_counter() - total_started)
    return {
        "query": query_info.get("input_query") or query,
        "effective_query": query_info.get("effective_query") or normalize_query_string(query),
        "query_preparation": query_info,
        "raw_count": len(all_records),
        "candidate_count": len(final_records),
        "source_errors": source_errors,
        "source_status": source_status,
        "timings": timings,
        "records": [record.to_dict() for record in final_records],
    }

def import_once(
    query: str,
    config: Dict[str, Any],
    *,
    client: ZoteroClient,
    existing_cache: Dict[str, Any] | None = None,
    run_state: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    total_started = time.perf_counter()
    prepared_query = auto_quote_arxiv_field_phrases(query)
    search_result = search_once(query, config, prepared_query=prepared_query)
    records = [PaperRecord(**row) for row in search_result["records"]]
    policy_cfg = config.get("import_policy") or {}
    require_pdf = bool(policy_cfg.get("require_pdf", True))
    dry_run = bool((config.get("run") or {}).get("dry_run", False))
    max_new_items = int(policy_cfg.get("max_new_items", 50) or 50)
    state = run_state if isinstance(run_state, dict) else {}
    state.setdefault("created_items", 0)
    state.setdefault("max_new_items", max_new_items)

    accepted: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    imported: List[Dict[str, Any]] = []
    existing_skipped: List[Dict[str, Any]] = []
    timings: Dict[str, Any] = {
        "existing_cache_lookup_seconds": 0.0,
        "create_and_attach_seconds": 0.0,
        "total_seconds": 0.0,
    }
    counters: Dict[str, int] = {
        "created_items": 0,
        "cache_hits": 0,
        "import_limit": int(state.get("max_new_items", max_new_items)),
        "created_before_query": int(state.get("created_items", 0)),
    }
    limit_reached = False

    if not dry_run and int(state.get("created_items", 0)) >= int(state.get("max_new_items", max_new_items)):
        limit_reached = True
    for record in records:
        if limit_reached:
            skipped.append({"title": record.title, "reason": "max_new_items_reached"})
            break
        if require_pdf and not record.pdf_url:
            skipped.append({"title": record.title, "reason": "missing_pdf"})
            continue
        accepted.append(record.to_dict())
        lookup_started = time.perf_counter()
        existing = find_existing_in_cache(existing_cache, record, config)
        timings["existing_cache_lookup_seconds"] += time.perf_counter() - lookup_started
        if existing:
            counters["cache_hits"] += 1
            existing_skipped.append({
                "title": record.title,
                "existing_key": existing.get("key"),
                "existing_title": (existing.get("data") or {}).get("title"),
                "reason": "already_in_zotero",
            })
            continue
        if int(state.get("created_items", 0)) >= int(state.get("max_new_items", max_new_items)):
            skipped.append({"title": record.title, "reason": "max_new_items_reached"})
            limit_reached = True
            break
        if dry_run:
            imported.append({"title": record.title, "dry_run": True, "existing": False})
            continue
        create_started = time.perf_counter()
        result = client.create_item(record, config)
        timings["create_and_attach_seconds"] += time.perf_counter() - create_started
        if result.get("created"):
            counters["created_items"] += 1
            state["created_items"] = int(state.get("created_items", 0)) + 1
            update_existing_cache(existing_cache, record, str(result.get("item_key") or ""))
        imported.append({"title": record.title, **result})

    timings = {key: round_seconds(value) for key, value in timings.items()}
    timings["total_seconds"] = round_seconds(time.perf_counter() - total_started)
    final = {
        "query": query,
        "search": search_result,
        "accepted_count": len(accepted),
        "skipped_count": len(skipped),
        "accepted": accepted,
        "skipped": skipped,
        "existing_skipped": existing_skipped,
        "imported": imported,
        "dry_run": dry_run,
        "timings": timings,
        "counters": counters,
        "import_limit_reached": limit_reached,
        "run_created_items": int(state.get("created_items", 0)),
        "run_max_new_items": int(state.get("max_new_items", max_new_items)),
        "existing_cache": {
            "enabled": bool(existing_cache and existing_cache.get("enabled")),
            "row_count": int((existing_cache or {}).get("row_count", 0)),
            "cache_query": str((existing_cache or {}).get("cache_query", "")),
            "cache_strategy": str((existing_cache or {}).get("cache_strategy", "")),
            "fetches": list((existing_cache or {}).get("fetches") or []),
        },
    }
    return final


def export_summary(payload: Dict[str, Any], config: Dict[str, Any]) -> None:
    run_cfg = config.get("run") or {}
    path_str = str(run_cfg.get("export_summary_path") or "").strip()
    if not path_str:
        return
    path = Path(path_str).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def format_source_status(source_status: List[Dict[str, Any]]) -> str:
    """Format source usage for user-facing reporting."""
    parts: List[str] = []
    for row in source_status:
        source = row.get("source", "unknown")
        if row.get("used"):
            parts.append(f"{source}({row.get('count', 0)})")
        else:
            reason = row.get("reason") or "skipped"
            parts.append(f"{source}(skipped: {reason})")
    return ", ".join(parts)


def build_import_user_report(row: Dict[str, Any]) -> str:
    """Build one concise user-facing summary for the query."""
    search = row.get("search") or {}
    source_status = format_source_status(search.get("source_status") or [])
    imported = row.get("imported") or []
    existing_skipped = row.get("existing_skipped") or []
    skipped = row.get("skipped") or []
    source_errors = search.get("source_errors") or []
    imported_titles = [item.get("title") for item in imported if item.get("created") or item.get("dry_run")]
    search_timings = search.get("timings") or {}
    import_timings = row.get("timings") or {}
    query_preparation = search.get("query_preparation") or {}
    cache_info = row.get("existing_cache") or {}
    cache_fetches = cache_info.get("fetches") or []
    fetch_labels = ", ".join(str(item.get("label")) for item in cache_fetches[:8] if item.get("label"))
    parts = [
        f"Query: {row.get('query')}",
        f"Effective arXiv query: {search.get('effective_query', row.get('query', ''))}",
        f"Sources: {source_status}",
        f"arXiv results: {search.get('raw_count', 0)}",
        f"Unique candidates: {search.get('candidate_count', 0)}",
        f"Zotero cache: strategy {cache_info.get('cache_strategy', 'unknown')}, rows {cache_info.get('row_count', 0)}",
        f"Already in Zotero: {len(existing_skipped)}",
        f"New imports: {sum(1 for item in imported if item.get('created') or item.get('dry_run'))}",
        f"Skipped because already present: {len(existing_skipped)}",
        f"Other skips: {len(skipped)}",
        f"Import cap: {row.get('run_max_new_items', 50)} (created so far {row.get('run_created_items', 0)})",
        f"Timings (s): arXiv {search_timings.get('arxiv_seconds', 0)}, dedupe {search_timings.get('dedupe_seconds', 0)}, cache lookup {import_timings.get('existing_cache_lookup_seconds', 0)}, import {import_timings.get('create_and_attach_seconds', 0)}, total {import_timings.get('total_seconds', search_timings.get('total_seconds', 0))}",
    ]
    if fetch_labels:
        parts.append(f"Zotero cache fetches: {fetch_labels}")
    if query_preparation.get("fix_count"):
        parts.append(
            f"Query safety fix: auto-quoted {query_preparation.get('fix_count', 0)} multi-word field value(s) before calling arXiv."
        )
    if imported_titles:
        parts.append("Imported papers: " + "; ".join(imported_titles[:10]))
    if skipped:
        reason_counts: Dict[str, int] = {}
        for item in skipped:
            reason = str(item.get("reason") or "unknown")
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        parts.append("Skip reasons: " + ", ".join(f"{k}×{v}" for k, v in sorted(reason_counts.items())))
    if row.get("import_limit_reached"):
        parts.append("Import cap reached during this query; later candidates were not imported.")
    if source_errors:
        parts.append("Source errors: " + "; ".join(f"{item.get('source')}: {item.get('error')}" for item in source_errors))
    return "\n".join(parts)

def build_user_message(payload: Dict[str, Any]) -> str:
    """Build the final message that OpenClaw can send to the user directly."""
    row = payload.get("result") or {}
    if not row:
        return "Run finished. No query was processed."
    search = row.get("search") or {}
    imported = row.get("imported") or []
    existing_skipped = row.get("existing_skipped") or []
    skipped = row.get("skipped") or []
    total_new = sum(1 for item in imported if item.get("created") or item.get("dry_run"))
    import_cap = int(payload.get("run_state", {}).get("max_new_items", 50) or 50)
    cap_reached = bool(payload.get("run_state", {}).get("cap_reached"))
    message = (
        f"Run finished. arXiv results {search.get('raw_count', 0)}, unique candidates {search.get('candidate_count', 0)}, "
        f"already in Zotero {len(existing_skipped)}, newly imported {total_new} (cap {import_cap}), other skips {len(skipped)}."
    )
    query_fix_count = int(((search.get("query_preparation") or {}).get("fix_count", 0)) or 0)
    if cap_reached:
        message += " Import cap reached; later candidates were not imported."
    if query_fix_count:
        message += f" Query safety fix applied to {query_fix_count} multi-word field value(s)."
    if search.get("source_errors"):
        message += f" Source errors: {len(search.get('source_errors') or [])}."
    return message

def attach_user_report(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Attach user-facing summaries for the single-query workflow."""
    row = payload.get("result") or {}
    report = build_import_user_report(row) if row else ""
    payload["user_report"] = report
    payload["user_message"] = build_user_message(payload)
    payload["notify_user"] = True
    if row:
        row["user_report"] = report
    return payload

def parse_query(config: Dict[str, Any]) -> str:
    value = normalize_query_string(config.get("query"))
    if value:
        return value
    raise ValueError("No query provided. Pass --query with one raw arXiv search_query string, or save a default query in config.json.")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"{APP_NAME} {APP_VERSION}")
    parser.add_argument("--config", help="Path to config.json. If omitted, use the bundled config.json next to the skill.")
    parser.add_argument("--query", help="One raw arXiv search_query string. The script URL-encodes it before calling arXiv.")
    return parser

def apply_runtime_overrides(config: Dict[str, Any], args: argparse.Namespace) -> Dict[str, Any]:
    updated = json.loads(json.dumps(config))
    query = normalize_query_string(args.query)
    if query:
        updated["query"] = query
    return updated

def attach_aggregate_timings(payload: Dict[str, Any]) -> Dict[str, Any]:
    row = payload.get("result") or {}
    search = row.get("search") or {}
    cache = payload.get("existing_cache") or {}
    payload["timings"] = {
        "existing_cache_seconds": round_seconds(float(cache.get("seconds", 0) or 0)),
        "search_total_seconds": round_seconds(float((search.get("timings") or {}).get("total_seconds", 0) or 0)),
        "import_total_seconds": round_seconds(float((row.get("timings") or {}).get("total_seconds", 0) or 0)),
        "queries": 1 if row else 0,
    }
    return payload

def handle_import(config: Dict[str, Any]) -> Dict[str, Any]:
    query = parse_query(config)
    prepared_query = auto_quote_arxiv_field_phrases(query)
    client = ZoteroClient(
        library_id=(config.get("zotero") or {}).get("library_id"),
        library_type=(config.get("zotero") or {}).get("library_type"),
        api_key=resolve_zotero_api_key(config),
        timeout=int((config.get("run") or {}).get("timeout_seconds", 20)),
    )
    existing_cache = build_existing_cache(client, prepared_query.get("effective_query") or query, config)
    max_new_items = int(((config.get("import_policy") or {}).get("max_new_items", 50)) or 50)
    run_state: Dict[str, Any] = {"created_items": 0, "max_new_items": max(1, max_new_items), "cap_reached": False}
    result = import_once(prepared_query.get("input_query") or query, config, client=client, existing_cache=existing_cache, run_state=run_state)
    if result.get("import_limit_reached"):
        run_state["cap_reached"] = True
    final = {
        "run_state": {
            "created_items": int(run_state.get("created_items", 0)),
            "max_new_items": int(run_state.get("max_new_items", max_new_items)),
            "cap_reached": bool(run_state.get("cap_reached")),
        },
        "query_preparation": prepared_query,
        "existing_cache": {
            "enabled": True,
            "query": existing_cache.get("query", ""),
            "cache_query": existing_cache.get("cache_query", ""),
            "cache_terms": existing_cache.get("cache_terms", []),
            "cache_phrases": existing_cache.get("cache_phrases", []),
            "cache_strategy": existing_cache.get("cache_strategy", ""),
            "fetches": existing_cache.get("fetches", []),
            "pages": existing_cache.get("pages", 0),
            "row_count": existing_cache.get("row_count", 0),
            "seconds": existing_cache.get("seconds", 0),
        },
        "result": result,
    }
    final = attach_aggregate_timings(attach_user_report(final))
    export_summary(final, config)
    existing_cache.clear()
    return final

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = load_skill_config(args.config)
    config = apply_runtime_overrides(config, args)
    validate_config(config, "import")
    result = handle_import(config)
    print(json.dumps(result, ensure_ascii=False, indent=2))



if __name__ == "__main__":
    main()
