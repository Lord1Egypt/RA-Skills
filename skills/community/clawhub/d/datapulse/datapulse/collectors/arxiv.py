"""arXiv paper collector via Atom API."""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

import requests

from datapulse.core.models import SourceType
from datapulse.core.retry import retry
from datapulse.core.utils import generate_excerpt

from .base import BaseCollector, ParseResult

_ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
_ARXIV_URL_PATTERN = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})")
_ATOM_NS = "{http://www.w3.org/2005/Atom}"
_MAX_AUTHORS = 10


def extract_arxiv_id(url: str) -> str | None:
    """Extract arXiv ID from URL or 'arxiv:XXXX.XXXXX' notation."""
    m = _ARXIV_URL_PATTERN.search(url)
    if m:
        return m.group(1)
    if "arxiv:" in url.lower():
        m2 = _ARXIV_ID_PATTERN.search(url)
        if m2:
            return m2.group(1)
    return None


class ArxivCollector(BaseCollector):
    name = "arxiv"
    source_type = SourceType.ARXIV
    reliability = 0.88
    tier = 0
    setup_hint = ""

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "requests available", "available": True}

    def can_handle(self, url: str) -> bool:
        lower = url.lower()
        if "arxiv.org/abs/" in lower or "arxiv.org/pdf/" in lower:
            return True
        if re.search(r"arxiv:\d{4}\.\d{4,5}", lower):
            return True
        return False

    def parse(self, url: str) -> ParseResult:
        arxiv_id = extract_arxiv_id(url)
        if not arxiv_id:
            return ParseResult.failure(url, "Could not extract arXiv ID")

        try:
            xml_text = self._fetch_atom(arxiv_id)
        except requests.RequestException as exc:
            return ParseResult.failure(url, f"arXiv API fetch failed: {exc}")

        return self._parse_atom_response(url, arxiv_id, xml_text)

    def _parse_atom_response(self, url: str, arxiv_id: str, xml_text: str) -> ParseResult:
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            return ParseResult.failure(url, f"arXiv XML parse error: {exc}")

        entry = root.find(f"{_ATOM_NS}entry")
        if entry is None:
            return ParseResult.failure(url, "No entry found in arXiv response")

        title = (entry.findtext(f"{_ATOM_NS}title") or "").strip()
        title = re.sub(r"\s+", " ", title)
        abstract = (entry.findtext(f"{_ATOM_NS}summary") or "").strip()

        authors_els = entry.findall(f"{_ATOM_NS}author")
        authors = []
        for a in authors_els[:_MAX_AUTHORS]:
            name = a.findtext(f"{_ATOM_NS}name")
            if name:
                authors.append(name.strip())
        if len(authors_els) > _MAX_AUTHORS:
            authors.append(f"et al. ({len(authors_els)} total)")

        categories = []
        for cat in entry.findall(f"{_ATOM_NS}category"):
            term = cat.get("term")
            if term:
                categories.append(term)

        published = entry.findtext(f"{_ATOM_NS}published") or ""
        updated = entry.findtext(f"{_ATOM_NS}updated") or ""

        pdf_url = ""
        for link in entry.findall(f"{_ATOM_NS}link"):
            if link.get("title") == "pdf":
                pdf_url = link.get("href", "")
                break
        if not pdf_url:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        author_str = ", ".join(authors[:3])
        if len(authors) > 3:
            author_str += " et al."

        content = f"**{title}**\n\n{author_str}\n\n{abstract}"

        return ParseResult(
            url=f"https://arxiv.org/abs/{arxiv_id}",
            title=title or f"arXiv:{arxiv_id}",
            content=content,
            author=author_str,
            excerpt=generate_excerpt(abstract),
            source_type=self.source_type,
            tags=["arxiv", *categories[:5]],
            confidence_flags=["arxiv_api", "structured_metadata"],
            extra={
                "arxiv_id": arxiv_id,
                "authors": authors,
                "categories": categories,
                "published": published,
                "updated": updated,
                "pdf_url": pdf_url,
            },
        )

    @retry(max_attempts=2, retryable=(requests.RequestException,))
    def _fetch_atom(self, arxiv_id: str) -> str:
        resp = requests.get(
            f"https://export.arxiv.org/api/query?id_list={arxiv_id}",
            timeout=20,
            headers={"User-Agent": "DataPulse/0.4"},
        )
        resp.raise_for_status()
        return resp.text
