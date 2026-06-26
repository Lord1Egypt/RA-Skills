#!/usr/bin/env python3
"""Shared helpers for talking to the arXiv API."""

from __future__ import annotations

import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date

ARXIV_QUERY_URL = "https://export.arxiv.org/api/query?{query_string}"
ARXIV_API_ID_URL = "https://export.arxiv.org/api/query?id_list={paper_id}"
ARXIV_ABS_URL = "https://arxiv.org/abs/{paper_id}"
ARXIV_HTML_URL = "https://arxiv.org/html/{paper_id}"
ARXIV_PDF_URL = "https://arxiv.org/pdf/{paper_id}.pdf"
ARXIV_EPRINT_URL = "https://arxiv.org/e-print/{paper_id}"
USER_AGENT = "openclaw-arxiv-paper-reader/0.2"
DEFAULT_TIMEOUT = 30.0
DEFAULT_LIMIT = 5
MAX_LIMIT = 20
VALID_SORTS = {"relevance", "submittedDate", "lastUpdatedDate"}
VALID_ORDERS = {"ascending", "descending"}
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
}
ARXIV_ALLOWED_HOSTS = {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}


@dataclass
class PaperMetadata:
    paper_id: str
    title: str
    abstract: str
    authors: list[str]
    categories: list[str]
    published: str
    updated: str


@dataclass
class SearchResult:
    paper_id: str
    title: str
    abstract: str
    authors: list[str]
    categories: list[str]
    published: str
    updated: str
    abstract_url: str
    pdf_url: str


@dataclass
class SearchResponse:
    entries: list[SearchResult]
    total_results: int
    returned_results: int
    search_query: str
    sort_by: str
    sort_order: str
    start_date: str | None
    end_date: str | None


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _validate_identifier(candidate: str, original_value: str) -> str:
    if candidate.endswith(".pdf"):
        candidate = candidate[:-4]

    if not candidate:
        raise ValueError("empty arXiv identifier")

    if not re.fullmatch(r"[A-Za-z0-9._/-]+(?:v\d+)?", candidate):
        raise ValueError(f"unsupported arXiv identifier: {original_value}")

    return candidate


def _extract_identifier_from_arxiv_url(url: str, *, allow_http: bool) -> str:
    parsed = urllib.parse.urlparse(url)
    scheme = (parsed.scheme or "").lower()
    if scheme != "https" and not (allow_http and scheme == "http"):
        raise ValueError("only HTTPS arXiv URLs are supported; use a raw arXiv ID or a valid arXiv URL")

    host = (parsed.hostname or "").lower()
    if host not in ARXIV_ALLOWED_HOSTS:
        raise ValueError("only arXiv URLs are supported; use a raw arXiv ID or a valid arXiv URL")

    path = parsed.path.strip("/")
    if path.startswith("abs/"):
        return _validate_identifier(path[len("abs/") :], url)
    if path.startswith("html/"):
        return _validate_identifier(path[len("html/") :], url)
    if path.startswith("e-print/"):
        return _validate_identifier(path[len("e-print/") :], url)
    if path.startswith("pdf/") and path.endswith(".pdf"):
        return _validate_identifier(path[len("pdf/") : -4], url)

    raise ValueError("unsupported arXiv URL path; use /abs/, /pdf/, /html/, or /e-print/")


def normalize_identifier(value: str, *, allow_http_url: bool = False) -> str:
    candidate = value.strip()
    candidate = re.sub(r"^arxiv:\s*", "", candidate, flags=re.IGNORECASE)

    if re.match(r"^https?://", candidate, flags=re.IGNORECASE):
        return _extract_identifier_from_arxiv_url(candidate, allow_http=allow_http_url)

    return _validate_identifier(candidate, value)


def safe_dir_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value)


def build_ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


def request_bytes(url: str, timeout: float = DEFAULT_TIMEOUT) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = build_ssl_context()
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
            return response.read()
    except ssl.SSLCertVerificationError as error:
        raise RuntimeError(
            "TLS certificate verification failed while fetching arXiv content. "
            "Install certifi or fix the system CA bundle."
        ) from error
    except urllib.error.URLError as error:
        reason = getattr(error, "reason", None)
        if isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(reason or error):
            raise RuntimeError(
                "TLS certificate verification failed while fetching arXiv content. "
                "Install certifi or fix the system CA bundle."
            ) from error
        raise


def decode_bytes(payload: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    return payload.decode("utf-8", errors="replace")


def request_text(url: str, timeout: float = DEFAULT_TIMEOUT) -> str:
    return decode_bytes(request_bytes(url, timeout))


def build_query_text(query: str) -> str:
    text = normalize_space(query).replace('"', "")
    if not text:
        raise ValueError("query cannot be empty")
    if re.fullmatch(r"[A-Za-z0-9._+-]+", text):
        return f"all:{text}"
    return f'all:"{text}"'


def build_search_query(query: str | None) -> str:
    if not query or not normalize_space(query):
        raise ValueError("query is required")
    return build_query_text(query)


def validate_date_value(value: str, field_name: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format") from error
    return parsed.isoformat()


def validate_date_range(start_date: str | None, end_date: str | None) -> tuple[str | None, str | None]:
    if start_date is None and end_date is None:
        return None, None
    if not start_date or not end_date:
        raise ValueError("start_date and end_date must be provided together")

    normalized_start = validate_date_value(start_date, "start_date")
    normalized_end = validate_date_value(end_date, "end_date")
    if normalized_start > normalized_end:
        raise ValueError("start_date must be less than or equal to end_date")
    return normalized_start, normalized_end


def build_submitted_date_query(start_date: str | None, end_date: str | None) -> str | None:
    normalized_start, normalized_end = validate_date_range(start_date, end_date)
    if normalized_start is None or normalized_end is None:
        return None
    start_token = normalized_start.replace("-", "")
    end_token = normalized_end.replace("-", "")
    return f"submittedDate:[{start_token}0000 TO {end_token}2359]"


def build_search_query_with_dates(query: str | None, start_date: str | None, end_date: str | None) -> tuple[str, str | None, str | None]:
    query_part = build_search_query(query)
    date_part = build_submitted_date_query(start_date, end_date)
    if not date_part:
        return query_part, None, None
    normalized_start, normalized_end = validate_date_range(start_date, end_date)
    return f"{query_part} AND {date_part}", normalized_start, normalized_end


def validate_limit(limit: int) -> int:
    if not 1 <= limit <= MAX_LIMIT:
        raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
    return limit


def default_sort_for() -> str:
    return "relevance"


def validate_sort(sort_by: str) -> str:
    if sort_by not in VALID_SORTS:
        raise ValueError(f"unsupported sort: {sort_by}")
    return sort_by


def validate_order(sort_order: str) -> str:
    if sort_order not in VALID_ORDERS:
        raise ValueError(f"unsupported order: {sort_order}")
    return sort_order


def parse_search_entry(entry: ET.Element) -> SearchResult:
    paper_id = normalize_identifier(entry.findtext("atom:id", default="", namespaces=ATOM_NS), allow_http_url=True)
    authors = [
        normalize_space(node.text or "")
        for node in entry.findall("atom:author/atom:name", ATOM_NS)
        if normalize_space(node.text or "")
    ]
    categories = [node.attrib["term"] for node in entry.findall("atom:category", ATOM_NS) if "term" in node.attrib]
    return SearchResult(
        paper_id=paper_id,
        title=normalize_space(entry.findtext("atom:title", default="", namespaces=ATOM_NS)),
        abstract=normalize_space(entry.findtext("atom:summary", default="", namespaces=ATOM_NS)),
        authors=authors,
        categories=categories,
        published=normalize_space(entry.findtext("atom:published", default="", namespaces=ATOM_NS)),
        updated=normalize_space(entry.findtext("atom:updated", default="", namespaces=ATOM_NS)),
        abstract_url=ARXIV_ABS_URL.format(paper_id=paper_id),
        pdf_url=ARXIV_PDF_URL.format(paper_id=paper_id),
    )


def parse_search_response(
    xml_text: str,
    search_query: str,
    sort_by: str,
    sort_order: str,
    start_date: str | None,
    end_date: str | None,
) -> SearchResponse:
    root = ET.fromstring(xml_text)
    entries = [parse_search_entry(entry) for entry in root.findall("atom:entry", ATOM_NS)]
    total_results = int(root.findtext("opensearch:totalResults", default="0", namespaces=ATOM_NS))
    return SearchResponse(
        entries=entries,
        total_results=total_results,
        returned_results=len(entries),
        search_query=search_query,
        sort_by=sort_by,
        sort_order=sort_order,
        start_date=start_date,
        end_date=end_date,
    )


def fetch_metadata(paper_id: str, timeout: float = DEFAULT_TIMEOUT) -> PaperMetadata:
    xml_text = request_text(ARXIV_API_ID_URL.format(paper_id=urllib.parse.quote(paper_id)), timeout)
    root = ET.fromstring(xml_text)
    entry = root.find("atom:entry", ATOM_NS)
    if entry is None:
        raise RuntimeError(f"paper not found in arXiv API: {paper_id}")

    authors = [
        normalize_space(node.text or "")
        for node in entry.findall("atom:author/atom:name", ATOM_NS)
        if normalize_space(node.text or "")
    ]
    categories = [node.attrib["term"] for node in entry.findall("atom:category", ATOM_NS) if "term" in node.attrib]

    return PaperMetadata(
        paper_id=paper_id,
        title=normalize_space(entry.findtext("atom:title", default="", namespaces=ATOM_NS)),
        abstract=normalize_space(entry.findtext("atom:summary", default="", namespaces=ATOM_NS)),
        authors=authors,
        categories=categories,
        published=normalize_space(entry.findtext("atom:published", default="", namespaces=ATOM_NS)),
        updated=normalize_space(entry.findtext("atom:updated", default="", namespaces=ATOM_NS)),
    )


def search_papers(
    query: str | None,
    *,
    start_date: str | None = None,
    end_date: str | None = None,
    sort_by: str | None = None,
    sort_order: str = "descending",
    limit: int = DEFAULT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT,
) -> SearchResponse:
    limit = validate_limit(limit)
    search_query, normalized_start, normalized_end = build_search_query_with_dates(query, start_date, end_date)
    resolved_sort = validate_sort(sort_by or default_sort_for())
    resolved_order = validate_order(sort_order)
    params = urllib.parse.urlencode(
        {
            "search_query": search_query,
            "start": 0,
            "max_results": limit,
            "sortBy": resolved_sort,
            "sortOrder": resolved_order,
        }
    )
    xml_text = request_text(ARXIV_QUERY_URL.format(query_string=params), timeout)
    return parse_search_response(
        xml_text,
        search_query,
        resolved_sort,
        resolved_order,
        normalized_start,
        normalized_end,
    )
