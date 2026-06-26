#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import time
import urllib.parse
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


ARXIV_API_URL = "https://export.arxiv.org/api/query"
DEFAULT_OUTPUT_ROOT = Path("/tmp")
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
GENERIC_TOPIC_TOKENS = {
    "analysis",
    "content",
    "extraction",
    "from",
    "image",
    "images",
    "information",
    "intelligence",
    "reasoning",
    "semantic",
    "semantics",
    "understanding",
    "visual",
}
TOPIC_CONCEPT_LIBRARY = {
    "ocr": {
        "aliases": ["ocr", "optical character recognition", "文字识别", "光学字符识别"],
        "anchors": ["ocr", "character", "handwritten"],
        "related": [],
        "phrases": [
            "ocr",
            "optical character recognition",
            "scene text recognition",
            "text recognition",
            "text spotting",
            "document ocr",
            "character recognition",
            "handwritten text recognition",
        ],
    },
    "document understanding": {
        "aliases": ["document understanding", "文档理解", "文档智能", "文档分析"],
        "anchors": ["document", "documents", "layout", "form", "pdf", "page", "table", "tables"],
        "related": ["ocr", "table understanding"],
        "phrases": [
            "document understanding",
            "visual document understanding",
            "document intelligence",
            "document parsing",
            "document analysis",
            "document layout analysis",
            "document ai",
            "document reasoning",
            "form understanding",
            "document structure understanding",
            "document image understanding",
            "reading order",
            "layout understanding",
            "key information extraction",
            "information extraction from documents",
            "pdf understanding",
            "pdf parsing",
            "pdf parser",
            "pdf document parsing",
            "table extraction from documents",
            "document table extraction",
            "document table understanding",
            "page understanding",
            "page layout understanding",
            "document element recognition",
        ],
    },
    "chart understanding": {
        "aliases": ["chart understanding", "图表理解", "图表分析"],
        "anchors": ["chart", "diagram", "infographic", "plot"],
        "related": [],
        "phrases": [
            "chart understanding",
            "chart question answering",
            "chart qa",
            "chart reasoning",
            "chart parsing",
            "chart extraction",
            "diagram understanding",
            "infographic understanding",
            "plot understanding",
            "figure understanding",
            "table understanding",
        ],
    },
    "table understanding": {
        "aliases": ["table understanding", "表格理解", "表格分析"],
        "anchors": ["table", "tables", "tabular"],
        "related": [],
        "phrases": [
            "table understanding",
            "table parsing",
            "table extraction",
            "table structure recognition",
            "table recognition",
            "table reasoning",
            "tabular extraction",
            "pdf table extraction",
        ],
    },
}


@dataclass
class Paper:
    arxiv_id: str
    title: str
    abstract: str
    published_utc: str
    updated_utc: str
    url: str
    pdf_url: str


class RunLogger:
    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.log_path = run_dir / "activity.log"

    def log(self, message: str) -> None:
        timestamp = datetime.now().isoformat(timespec="seconds")
        line = f"[{timestamp}] {message}"
        print(line, file=sys.stderr)
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")


class RateLimiter:
    def __init__(self, min_interval_seconds: float) -> None:
        self.min_interval_seconds = min_interval_seconds
        self.last_request_at = 0.0

    def wait(self, logger: RunLogger, label: str) -> None:
        now = time.monotonic()
        elapsed = now - self.last_request_at
        remaining = self.min_interval_seconds - elapsed
        if remaining > 0:
            logger.log(
                f"Sleeping {remaining:.1f}s before {label} to respect request pacing."
            )
            time.sleep(remaining)
        self.last_request_at = time.monotonic()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch arXiv papers for a target date, screen them against a topic, "
            "download matched PDFs, and save all artifacts under the selected output root."
        )
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="Topic phrase to screen against titles and abstracts.",
    )
    parser.add_argument(
        "--topic-spec-file",
        help=(
            "Optional JSON file describing expanded topic signals. "
            "Expected keys include canonical_topic, positive_phrases, anchor_terms, "
            "related_topics, and negative_phrases."
        ),
    )
    parser.add_argument(
        "--date",
        dest="target_date",
        help="Target date in YYYY-MM-DD. Defaults to today in the selected timezone.",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="How many consecutive days to process, starting from --date and walking backward one day at a time. Default: 1",
    )
    parser.add_argument(
        "--timezone",
        default="UTC",
        help="IANA timezone used to interpret 'today'. Default: UTC",
    )
    parser.add_argument(
        "--category",
        default="cs.CV",
        help="arXiv category to query. Default: cs.CV",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=200,
        help="Page size requested from the arXiv API. Default: 200",
    )
    parser.add_argument(
        "--fallback-days",
        type=int,
        default=7,
        help="How many days to walk backward if the requested day has no papers. Default: 7",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Maximum number of fetched papers to keep after release-day filtering. 0 means no limit.",
    )
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Root directory for all logs and downloads. Default: /tmp",
    )
    parser.add_argument(
        "--output",
        choices=("json", "markdown"),
        default="json",
        help="Console output format. Default: json",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include full text content in JSON output. Default: False (more concise output)",
    )
    return parser.parse_args()


def parse_target_date(target_date: str | None, tz_name: str) -> tuple[date, ZoneInfo]:
    tz = ZoneInfo(tz_name)
    if target_date:
        return date.fromisoformat(target_date), tz
    return datetime.now(tz).date(), tz


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def tokenize(value: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", normalize_text(value))


def normalize_string_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    return sorted({normalize_text(value) for value in values if normalize_text(value)})


def expand_topic_part(part: str) -> list[str]:
    variants = [part]
    for canonical, spec in TOPIC_CONCEPT_LIBRARY.items():
        aliases = [normalize_text(alias) for alias in spec["aliases"]]
        phrases = [normalize_text(phrase) for phrase in spec["phrases"]]
        if part == normalize_text(canonical) or part in aliases or any(alias in part for alias in aliases):
            variants.extend([canonical, *aliases, *phrases])
            for related_name in spec.get("related", []):
                related_spec = TOPIC_CONCEPT_LIBRARY.get(related_name, {})
                variants.extend(
                    [normalize_text(related_name)]
                    + [normalize_text(alias) for alias in related_spec.get("aliases", [])]
                    + [normalize_text(phrase) for phrase in related_spec.get("phrases", [])]
                )
    return sorted({variant for variant in variants if variant})


def find_library_entry_for_part(part: str) -> dict[str, Any] | None:
    for canonical, spec in TOPIC_CONCEPT_LIBRARY.items():
        aliases = [normalize_text(alias) for alias in spec["aliases"]]
        if part == normalize_text(canonical) or part in aliases or any(alias in part for alias in aliases):
            return {
                "canonical": canonical,
                "aliases": aliases,
                "anchors": [normalize_text(anchor) for anchor in spec.get("anchors", [])],
            }
    return None


def build_topic_variants(topic: str) -> dict[str, Any]:
    normalized = normalize_text(topic)
    parts = [
        segment.strip()
        for segment in re.split(r"\s+(?:or|and)\s+|/|,|\|", normalized)
        if segment.strip()
    ]
    if not parts:
        parts = [normalized]

    concepts: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for part in parts:
        variants = expand_topic_part(part)
        tokens = sorted({token for phrase in variants for token in tokenize(phrase) if token not in STOPWORDS})
        tokens = [token for token in tokens if token not in GENERIC_TOPIC_TOKENS]
        if part not in seen_names:
            library_entry = find_library_entry_for_part(part)
            concepts.append(
                {
                    "name": part,
                    "phrases": sorted(set(variants)),
                    "tokens": tokens,
                    "anchor_tokens": sorted(set(tokenize(" ".join(library_entry["anchors"])))) if library_entry else [],
                    "canonical": library_entry["canonical"] if library_entry else part,
                }
            )
            seen_names.add(part)

    all_phrases = sorted({phrase for concept in concepts for phrase in concept["phrases"]})
    all_tokens = sorted({token for concept in concepts for token in concept["tokens"]})
    return {
        "topic": topic,
        "normalized_topic": normalized,
        "concepts": concepts,
        "all_phrases": all_phrases,
        "all_tokens": all_tokens,
        "negative_phrases": [],
        "negative_tokens": [],
        "topic_source": "library_fallback",
    }


def load_topic_spec_file(path_text: str) -> dict[str, Any]:
    path = Path(path_text).expanduser().resolve()
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Topic spec must be a JSON object: {path}")
    payload["_source_file"] = str(path)
    return payload


def build_topic_variants_from_spec(topic: str, topic_spec: dict[str, Any]) -> dict[str, Any]:
    positive_phrases = normalize_string_list(topic_spec.get("positive_phrases"))
    anchor_terms = normalize_string_list(topic_spec.get("anchor_terms"))
    related_topics = normalize_string_list(topic_spec.get("related_topics"))
    negative_phrases = normalize_string_list(topic_spec.get("negative_phrases"))
    canonical_topic = normalize_text(
        str(topic_spec.get("canonical_topic") or topic_spec.get("topic") or topic)
    )

    if canonical_topic and canonical_topic not in positive_phrases:
        positive_phrases.insert(0, canonical_topic)

    concepts = [
        {
            "name": canonical_topic or normalize_text(topic),
            "canonical": canonical_topic or normalize_text(topic),
            "phrases": positive_phrases,
            "tokens": sorted(
                {
                    token
                    for phrase in positive_phrases + related_topics
                    for token in tokenize(phrase)
                    if token not in STOPWORDS and token not in GENERIC_TOPIC_TOKENS
                }
            ),
            "anchor_tokens": sorted(
                {
                    token
                    for anchor in anchor_terms
                    for token in tokenize(anchor)
                    if token not in STOPWORDS
                }
            ),
        }
    ]

    all_phrases = sorted(set(positive_phrases + related_topics))
    all_tokens = sorted(
        {
            token
            for phrase in all_phrases
            for token in tokenize(phrase)
            if token not in STOPWORDS and token not in GENERIC_TOPIC_TOKENS
        }
    )
    negative_tokens = sorted(
        {
            token
            for phrase in negative_phrases
            for token in tokenize(phrase)
            if token not in STOPWORDS
        }
    )

    return {
        "topic": topic,
        "normalized_topic": normalize_text(topic),
        "canonical_topic": canonical_topic,
        "concepts": concepts,
        "all_phrases": all_phrases,
        "all_tokens": all_tokens,
        "anchor_terms": anchor_terms,
        "related_topics": related_topics,
        "negative_phrases": negative_phrases,
        "negative_tokens": negative_tokens,
        "topic_source": "topic_spec_file",
        "topic_spec_file": topic_spec.get("_source_file"),
        "raw_topic_spec": topic_spec,
    }


def resolve_topic_data(topic: str, topic_spec_file: str | None) -> dict[str, Any]:
    if topic_spec_file:
        return build_topic_variants_from_spec(topic, load_topic_spec_file(topic_spec_file))
    return build_topic_variants(topic)


def sanitize_fragment(value: str, limit: int = 80) -> str:
    collapsed = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return collapsed[:limit] or "untitled"


def ensure_output_root(path_text: str) -> Path:
    path = Path(path_text).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise RuntimeError(f"Output root is not a directory: {path}")
    if not os_access_write(path):
        raise RuntimeError(f"Output root is not writable: {path}")
    return path


def os_access_write(path: Path) -> bool:
    try:
        probe = path / ".write_probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def build_run_dir(output_root: Path, topic: str, requested_date: date, category: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_name = (
        f"{timestamp}_{sanitize_fragment(category)}_"
        f"{sanitize_fragment(topic, limit=48)}_{requested_date.isoformat()}"
    )
    run_dir = output_root / run_name
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def save_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def save_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def http_get(
    url: str,
    *,
    user_agent: str,
    retries: int = 4,
    rate_limiter: RateLimiter | None = None,
    logger: RunLogger | None = None,
    request_label: str = "request",
) -> bytes:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            if rate_limiter and logger:
                rate_limiter.wait(logger, request_label)
            request = urllib.request.Request(url, headers={"User-Agent": user_agent})
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt >= retries:
                raise
            if logger:
                logger.log(
                    f"{request_label} hit HTTP {exc.code}; retrying after backoff "
                    f"(attempt {attempt + 1}/{retries})."
                )
            time.sleep(2 * (attempt + 1))
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt >= retries:
                raise
            if logger:
                logger.log(
                    f"{request_label} hit URL error '{exc}'; retrying after backoff "
                    f"(attempt {attempt + 1}/{retries})."
                )
            time.sleep(2 * (attempt + 1))

    if last_error is not None:
        raise last_error
    raise RuntimeError("Unexpected HTTP failure without a captured exception.")


def parse_feed(feed_bytes: bytes) -> list[Paper]:
    root = ET.fromstring(feed_bytes)
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        entry_id = (entry.findtext("atom:id", default="", namespaces=ATOM_NS) or "").strip()
        arxiv_id = entry_id.rsplit("/", 1)[-1]
        title = " ".join((entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").split())
        abstract = " ".join((entry.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").split())
        published = (entry.findtext("atom:published", default="", namespaces=ATOM_NS) or "").strip()
        updated = (entry.findtext("atom:updated", default="", namespaces=ATOM_NS) or "").strip()
        pdf_url = ""
        for link in entry.findall("atom:link", ATOM_NS):
            if link.attrib.get("title") == "pdf":
                pdf_url = link.attrib.get("href", "")
                break
        if not pdf_url and arxiv_id:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        papers.append(
            Paper(
                arxiv_id=arxiv_id,
                title=title,
                abstract=abstract,
                published_utc=published,
                updated_utc=updated,
                url=entry_id,
                pdf_url=pdf_url,
            )
        )
    return papers


def fetch_release_day_papers(
    category: str,
    target_date: date,
    max_results: int,
    user_agent: str,
    logger: RunLogger,
    rate_limiter: RateLimiter,
) -> list[Paper]:
    papers: list[Paper] = []
    start = 0
    target_iso = target_date.isoformat()
    target_compact = target_date.strftime("%Y%m%d")

    while True:
        search_query = (
            f"cat:{category} AND "
            f"submittedDate:[{target_compact}0000 TO {target_compact}2359]"
        )
        query = urllib.parse.urlencode(
            {
                "search_query": search_query,
                "start": start,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        url = f"{ARXIV_API_URL}?{query}"
        logger.log(f"Fetching arXiv API page start={start} for {category} on {target_iso}.")
        entries = parse_feed(
            http_get(
                url,
                user_agent=user_agent,
                rate_limiter=rate_limiter,
                logger=logger,
                request_label=f"arXiv API page start={start}",
            )
        )
        if not entries:
            break

        matched = [paper for paper in entries if paper.published_utc[:10] == target_iso]
        papers.extend(matched)
        if matched:
            logger.log(
                f"Collected {len(matched)} paper(s) from page start={start} "
                f"for exact release day {target_iso}."
            )

        if len(entries) < max_results:
            break
        start += max_results

    return papers


def find_latest_available_release_day(
    category: str,
    requested_date: date,
    fallback_days: int,
    max_results: int,
    user_agent: str,
    logger: RunLogger,
    rate_limiter: RateLimiter,
) -> tuple[date | None, list[Paper], list[dict[str, Any]]]:
    attempts: list[dict[str, Any]] = []
    for offset in range(max(fallback_days, 0) + 1):
        current_date = requested_date - timedelta(days=offset)
        papers = fetch_release_day_papers(
            category,
            current_date,
            max_results,
            user_agent,
            logger,
            rate_limiter,
        )
        attempts.append(
            {
                "date": current_date.isoformat(),
                "paper_count": len(papers),
            }
        )
        if papers:
            return current_date, papers, attempts
    return None, [], attempts


def screen_title(topic_data: dict[str, Any], title: str) -> dict[str, Any]:
    title_norm = normalize_text(title)
    negative_phrase_hits = [phrase for phrase in topic_data.get("negative_phrases", []) if phrase and phrase in title_norm]
    matched_phrases: list[str] = []
    matched_tokens: list[str] = []
    concept_hits: list[str] = []
    title_tokens = set(tokenize(title_norm))
    best_concept_score = 0

    for concept in topic_data["concepts"]:
        concept_phrase_hits = [phrase for phrase in concept["phrases"] if phrase and phrase in title_norm]
        concept_token_hits = [token for token in concept["tokens"] if token in title_tokens]
        anchor_hits = [token for token in concept.get("anchor_tokens", []) if token in title_tokens]
        concept_score = len(concept_phrase_hits) * 5 + len(concept_token_hits)
        if concept_phrase_hits or (anchor_hits and len(concept_token_hits) >= 2):
            concept_hits.append(concept["name"])
        best_concept_score = max(best_concept_score, concept_score)
        matched_phrases.extend(concept_phrase_hits)
        matched_tokens.extend(concept_token_hits + anchor_hits)

    matched_phrases = sorted(set(matched_phrases))
    matched_tokens = sorted(set(matched_tokens))
    concept_hits = sorted(set(concept_hits))
    score = len(matched_phrases) * 5 + len(matched_tokens) + len(concept_hits) * 2
    has_anchor = any(token in matched_tokens for concept in topic_data["concepts"] for token in concept.get("anchor_tokens", []))
    if negative_phrase_hits:
        status = "negative_by_title"
        score = 0
    elif matched_phrases or (has_anchor and best_concept_score >= 6):
        status = "relevant_by_title"
    elif has_anchor and score >= 3:
        status = "possible_by_title"
    elif has_anchor or concept_hits:
        status = "needs_abstract_review"
    else:
        status = "unclear_by_title"

    return {
        "status": status,
        "score": score,
        "matched_phrases": matched_phrases,
        "matched_tokens": matched_tokens,
        "concept_hits": concept_hits,
        "negative_phrase_hits": negative_phrase_hits,
    }


def screen_abstract(topic_data: dict[str, Any], abstract: str) -> dict[str, Any]:
    abstract_norm = normalize_text(abstract)
    negative_phrase_hits = [
        phrase for phrase in topic_data.get("negative_phrases", []) if phrase and phrase in abstract_norm
    ]
    matched_phrases: list[str] = []
    matched_tokens: list[str] = []
    abstract_tokens = set(tokenize(abstract_norm))
    concept_hits: list[str] = []
    best_concept_score = 0

    for concept in topic_data["concepts"]:
        concept_phrase_hits = [phrase for phrase in concept["phrases"] if phrase and phrase in abstract_norm]
        concept_token_hits = [token for token in concept["tokens"] if token in abstract_tokens]
        anchor_hits = [token for token in concept.get("anchor_tokens", []) if token in abstract_tokens]
        concept_score = len(concept_phrase_hits) * 5 + len(concept_token_hits)
        if concept_phrase_hits or (anchor_hits and len(concept_token_hits) >= 2):
            concept_hits.append(concept["name"])
        best_concept_score = max(best_concept_score, concept_score)
        matched_phrases.extend(concept_phrase_hits)
        matched_tokens.extend(concept_token_hits + anchor_hits)

    matched_phrases = sorted(set(matched_phrases))
    matched_tokens = sorted(set(matched_tokens))
    concept_hits = sorted(set(concept_hits))
    score = len(matched_phrases) * 5 + len(matched_tokens) + len(concept_hits) * 2
    has_anchor = any(token in matched_tokens for concept in topic_data["concepts"] for token in concept.get("anchor_tokens", []))
    if negative_phrase_hits:
        status = "negative_by_abstract"
        score = 0
    elif matched_phrases or (has_anchor and best_concept_score >= 7):
        status = "relevant_by_abstract"
    elif has_anchor and score >= 4:
        status = "possible_match"
    elif has_anchor or concept_hits:
        status = "unclear_needs_pdf_review"
    else:
        status = "not_relevant"

    return {
        "status": status,
        "score": score,
        "matched_phrases": matched_phrases,
        "matched_tokens": matched_tokens,
        "concept_hits": concept_hits,
        "negative_phrase_hits": negative_phrase_hits,
    }


def render_catalog_markdown(
    papers: list[Paper],
    requested_date: date,
    resolved_date: date | None,
    topic: str,
    category: str,
) -> str:
    lines = [
        f"# arXiv {category} papers for topic '{topic}'",
        "",
        f"Requested date: {requested_date.isoformat()}",
        f"Resolved date: {resolved_date.isoformat() if resolved_date else 'none'}",
        f"Category: {category}",
        f"Paper count: {len(papers)}",
        "",
    ]
    if not papers:
        lines.append("No papers were found for the resolved date.")
        return "\n".join(lines) + "\n"

    for index, paper in enumerate(papers, start=1):
        lines.extend(
            [
                f"## {index}. {paper.title}",
                f"- arXiv ID: `{paper.arxiv_id}`",
                f"- Published UTC: `{paper.published_utc}`",
                f"- Updated UTC: `{paper.updated_utc}`",
                f"- URL: {paper.url}",
                f"- PDF: {paper.pdf_url}",
                "",
                "### Abstract",
                textwrap.fill(paper.abstract, width=100),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def download_pdf(
    paper: Paper,
    pdf_dir: Path,
    logger: RunLogger,
    rate_limiter: RateLimiter,
) -> dict[str, Any]:
    pdf_dir.mkdir(parents=True, exist_ok=True)
    safe_id = sanitize_fragment(paper.arxiv_id, limit=64)
    pdf_path = pdf_dir / f"{safe_id}.pdf"
    try:
        logger.log(f"Downloading PDF for {paper.arxiv_id} to {pdf_path}.")
        pdf_bytes = http_get(
            paper.pdf_url,
            user_agent="arxiv-cv-daily/2.0",
            rate_limiter=rate_limiter,
            logger=logger,
            request_label=f"PDF download {paper.arxiv_id}",
        )
        pdf_path.write_bytes(pdf_bytes)
        return {
            "status": "downloaded",
            "pdf_path": str(pdf_path),
            "error": None,
        }
    except Exception as exc:
        logger.log(f"Failed to download PDF for {paper.arxiv_id}: {exc}")
        return {
            "status": "download_failed",
            "pdf_path": str(pdf_path),
            "error": str(exc),
        }


def extract_pdf_text(pdf_path: Path, text_dir: Path, logger: RunLogger) -> dict[str, Any]:
    text_dir.mkdir(parents=True, exist_ok=True)
    text_path = text_dir / f"{pdf_path.stem}.txt"
    command = ["pdftotext", str(pdf_path), str(text_path)]
    try:
        logger.log(f"Extracting text from {pdf_path.name} with pdftotext.")
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            error = completed.stderr.strip() or completed.stdout.strip() or "pdftotext failed"
            logger.log(f"pdftotext failed for {pdf_path.name}: {error}")
            return {
                "status": "extract_failed",
                "text_path": str(text_path),
                "error": error,
            }

        extracted_text = text_path.read_text(encoding="utf-8", errors="ignore")
        excerpt = "\n".join(line.strip() for line in extracted_text.splitlines() if line.strip()[:1])[:4000]
        return {
            "status": "extracted",
            "text_path": str(text_path),
            "char_count": len(extracted_text),
            "preview": excerpt,
            "error": None,
        }
    except Exception as exc:
        logger.log(f"Unexpected text extraction failure for {pdf_path.name}: {exc}")
        return {
            "status": "extract_failed",
            "text_path": str(text_path),
            "error": str(exc),
        }


def build_brief_from_text(paper: Paper, extracted_text: str) -> str:
    cleaned_lines = [line.strip() for line in extracted_text.splitlines() if line.strip()]
    summary_lines: list[str] = []
    for line in cleaned_lines:
        lower = line.lower()
        if lower.startswith("abstract"):
            continue
        if "references" in lower or "acknowledg" in lower:
            break
        if len(line.split()) < 6:
            continue
        summary_lines.append(line)
        if len(" ".join(summary_lines)) > 900:
            break

    if not summary_lines:
        summary_lines = [paper.abstract]
    return " ".join(summary_lines)[:1200]


def assess_full_text_relevance(topic_data: dict[str, Any], extracted_text: str) -> dict[str, Any]:
    text_norm = normalize_text(extracted_text[:120000])
    text_tokens = set(tokenize(text_norm))
    negative_phrase_hits = [
        phrase for phrase in topic_data.get("negative_phrases", []) if phrase and phrase in text_norm
    ]
    matched_phrases: list[str] = []
    matched_tokens: list[str] = []
    concept_hits: list[str] = []

    for concept in topic_data["concepts"]:
        concept_phrase_hits = [phrase for phrase in concept["phrases"] if phrase and phrase in text_norm]
        concept_token_hits = [token for token in concept["tokens"] if token in text_tokens]
        anchor_hits = [token for token in concept.get("anchor_tokens", []) if token in text_tokens]
        if concept_phrase_hits or (anchor_hits and len(concept_token_hits) >= 2):
            concept_hits.append(concept["name"])
        matched_phrases.extend(concept_phrase_hits)
        matched_tokens.extend(concept_token_hits + anchor_hits)

    matched_phrases = sorted(set(matched_phrases))
    matched_tokens = sorted(set(matched_tokens))
    concept_hits = sorted(set(concept_hits))
    score = len(matched_phrases) * 4 + len(matched_tokens) + len(concept_hits) * 3
    has_anchor = any(token in matched_tokens for concept in topic_data["concepts"] for token in concept.get("anchor_tokens", []))
    if negative_phrase_hits:
        status = "negative_by_full_text"
        score = 0
    elif matched_phrases or (has_anchor and score >= 8):
        status = "relevant_by_full_text"
    elif has_anchor and score >= 4:
        status = "possible_by_full_text"
    else:
        status = "not_relevant_by_full_text"

    return {
        "status": status,
        "score": score,
        "matched_phrases": matched_phrases,
        "matched_tokens": matched_tokens,
        "concept_hits": concept_hits,
        "negative_phrase_hits": negative_phrase_hits,
    }


def render_match_summary_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        f"# Topic workflow summary for '{manifest['topic']}'",
        "",
        f"Requested date: {manifest['requested_date']}",
        f"Resolved date: {manifest['resolved_date'] or 'none'}",
        f"Category: {manifest['category']}",
        f"Run directory: {manifest.get('run_dir') or manifest.get('day_dir') or 'unknown'}",
        f"All papers fetched: {manifest['counts']['all_papers']}",
        f"Candidate papers after screening: {manifest['counts']['matched_papers']}",
        "",
    ]

    matched = manifest.get("matched_papers", [])
    if not matched:
        lines.append("No papers matched the topic screening rules.")
        return "\n".join(lines) + "\n"

    for index, paper in enumerate(matched, start=1):
        lines.extend(
            [
                f"## {index}. {paper['title']}",
                f"- arXiv ID: `{paper['arxiv_id']}`",
                f"- Match status: `{paper['match_status']}`",
                f"- Relevance score: `{paper.get('relevance_score', 0)}`",
                f"- Match reason: {paper['match_reason']}",
                f"- PDF status: `{paper['download']['status']}`",
                f"- PDF path: {paper['download']['pdf_path']}",
                f"- Text status: `{paper['full_text']['status']}`",
                f"- Text path: {paper['full_text'].get('text_path', '')}",
                f"- Full-text relevance: `{paper.get('full_text_relevance', {}).get('status', 'not_run') if paper.get('full_text_relevance') else 'not_run'}`",
                "",
                "### Core Content Draft",
                textwrap.fill(paper["core_content_draft"], width=100),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def console_payload(manifest: dict[str, Any], output: str, verbose: bool = False) -> str:
    if output == "markdown":
        if "days" in manifest:
            return render_overall_summary(manifest)
        return render_match_summary_markdown(manifest)
    
    # For JSON output, create a clean copy without verbose fields unless requested
    if not verbose:
        manifest = clean_manifest_for_output(manifest)
    
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def clean_manifest_for_output(manifest: dict[str, Any]) -> dict[str, Any]:
    """Remove verbose fields from manifest for cleaner JSON output."""
    import copy
    cleaned = copy.deepcopy(manifest)
    
    # Remove verbose fields from single-day manifest
    if "matched_papers" in cleaned:
        for paper in cleaned["matched_papers"]:
            # Keep only essential fields, remove full text content
            if "core_content_draft" in paper:
                del paper["core_content_draft"]
            if "abstract" in paper and len(paper["abstract"]) > 200:
                paper["abstract"] = paper["abstract"][:200] + "..."
            # Simplify full_text field
            if "full_text" in paper and isinstance(paper["full_text"], dict):
                if "preview" in paper["full_text"]:
                    del paper["full_text"]["preview"]
    
    # Remove verbose fields from multi-day manifest
    if "days" in cleaned:
        for day in cleaned["days"]:
            if "matched_papers" in day:
                for paper in day["matched_papers"]:
                    if "core_content_draft" in paper:
                        del paper["core_content_draft"]
                    if "abstract" in paper and len(paper["abstract"]) > 200:
                        paper["abstract"] = paper["abstract"][:200] + "..."
                    if "full_text" in paper and isinstance(paper["full_text"], dict):
                        if "preview" in paper["full_text"]:
                            del paper["full_text"]["preview"]
    
    return cleaned


def cache_root_for(output_root: Path) -> Path:
    path = output_root / "cache" / "arxiv_api"
    path.mkdir(parents=True, exist_ok=True)
    return path


def cache_path(output_root: Path, category: str, target_date: date) -> Path:
    category_dir = cache_root_for(output_root) / sanitize_fragment(category, limit=64)
    category_dir.mkdir(parents=True, exist_ok=True)
    return category_dir / f"{target_date.isoformat()}.json"


def save_cached_papers(output_root: Path, category: str, target_date: date, papers: list[Paper]) -> Path:
    path = cache_path(output_root, category, target_date)
    save_json(
        path,
        {
            "category": category,
            "date": target_date.isoformat(),
            "paper_count": len(papers),
            "papers": [asdict(paper) for paper in papers],
        },
    )
    return path


def load_cached_papers(output_root: Path, category: str, target_date: date) -> list[Paper] | None:
    path = cache_path(output_root, category, target_date)
    if not path.exists():
        return None
    payload = load_json(path)
    return [Paper(**paper) for paper in payload.get("papers", [])]


def process_single_day(
    *,
    topic: str,
    requested_date: date,
    tz: ZoneInfo,
    category: str,
    max_results: int,
    fallback_days: int,
    limit: int,
    output_root: Path,
    run_dir: Path,
    logger: RunLogger,
    api_rate_limiter: RateLimiter,
    pdf_rate_limiter: RateLimiter,
    topic_data: dict[str, Any],
    excluded_resolved_dates: set[date] | None = None,
) -> dict[str, Any]:
    day_slug = requested_date.isoformat()
    day_dir = run_dir / "days" / day_slug
    day_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Starting day-by-day processing for {day_slug}.")
    excluded_resolved_dates = excluded_resolved_dates or set()

    request_payload = {
        "topic": topic,
        "topic_variants": topic_data,
        "requested_date": requested_date.isoformat(),
        "timezone": tz.key,
        "category": category,
        "max_results": max_results,
        "fallback_days": fallback_days,
        "limit": limit,
        "output_root": str(output_root),
        "mode": "single_day_with_cache",
        "excluded_resolved_dates": sorted(day.isoformat() for day in excluded_resolved_dates),
    }
    save_json(day_dir / "01_request.json", request_payload)

    fallback_trace: list[dict[str, Any]] = []
    resolved_date: date | None = None
    papers: list[Paper] = []
    cache_hit = False

    for offset in range(max(fallback_days, 0) + 1):
        candidate_date = requested_date - timedelta(days=offset)
        if candidate_date in excluded_resolved_dates:
            logger.log(
                f"Skipping {candidate_date.isoformat()} because it was already resolved "
                f"for an earlier requested day in this multi-day run."
            )
            fallback_trace.append(
                {
                    "date": candidate_date.isoformat(),
                    "paper_count": None,
                    "source": "skipped_duplicate_resolved_date",
                }
            )
            continue
        cached = load_cached_papers(output_root, category, candidate_date)
        if cached is not None:
            logger.log(
                f"Loaded cached daily paper list for {category} on {candidate_date.isoformat()}."
            )
            fallback_trace.append(
                {
                    "date": candidate_date.isoformat(),
                    "paper_count": len(cached),
                    "source": "cache",
                }
            )
            if cached:
                resolved_date = candidate_date
                papers = cached
                cache_hit = True
                break
            continue

        fetched = fetch_release_day_papers(
            category,
            candidate_date,
            max_results,
            "arxiv-cv-daily/2.0",
            logger,
            api_rate_limiter,
        )
        save_cached_papers(output_root, category, candidate_date, fetched)
        fallback_trace.append(
            {
                "date": candidate_date.isoformat(),
                "paper_count": len(fetched),
                "source": "api",
            }
        )
        if fetched:
            resolved_date = candidate_date
            papers = fetched
            break

    if limit > 0:
        papers = papers[:limit]

    all_papers_payload = {
        "requested_date": requested_date.isoformat(),
        "resolved_date": resolved_date.isoformat() if resolved_date else None,
        "category": category,
        "paper_count": len(papers),
        "fallback_trace": fallback_trace,
        "cache_hit": cache_hit,
        "papers": [asdict(paper) for paper in papers],
    }
    save_json(day_dir / "02_all_papers.json", all_papers_payload)
    save_text(
        day_dir / "02_all_papers.md",
        render_catalog_markdown(papers, requested_date, resolved_date, topic, category),
    )
    logger.log(
        f"Saved full paper catalog for {day_slug} with {len(papers)} paper(s); "
        f"resolved date is {resolved_date.isoformat() if resolved_date else 'none'}."
    )

    title_screening: list[dict[str, Any]] = []
    abstract_screening: list[dict[str, Any]] = []
    matched_papers: list[dict[str, Any]] = []

    # Progress tracking
    total_papers = len(papers)
    logger.log(f"Starting title screening for {total_papers} papers.")
    
    for idx, paper in enumerate(papers, start=1):
        # Progress output every 10 papers or for the first/last
        if idx == 1 or idx == total_papers or idx % 10 == 0:
            print(f"[{idx}/{total_papers}] Screening titles...", file=sys.stderr)
        title_result = screen_title(topic_data, paper.title)
        title_screening.append(
            {
                "arxiv_id": paper.arxiv_id,
                "title": paper.title,
                "result": title_result,
            }
        )

        abstract_result: dict[str, Any] | None = None
        match_status = title_result["status"]
        match_reason = "Matched directly from title." if match_status == "relevant_by_title" else ""
        if match_status == "possible_by_title":
            match_reason = "Title shows partial topic evidence; abstract review is required."
        if match_status == "negative_by_title":
            match_reason = "Title matched a negative phrase from the topic spec."

        if match_status not in {"relevant_by_title", "negative_by_title"}:
            abstract_result = screen_abstract(topic_data, paper.abstract)
            abstract_screening.append(
                {
                    "arxiv_id": paper.arxiv_id,
                    "title": paper.title,
                    "result": abstract_result,
                }
            )
            match_status = abstract_result["status"]
            if match_status == "relevant_by_abstract":
                match_reason = "Title was inconclusive; abstract confirmed the topic match."
            elif match_status == "possible_match":
                match_reason = "Title was inconclusive; abstract suggests a possible topic match."
            elif match_status == "unclear_needs_pdf_review":
                match_reason = "Title and abstract were still inconclusive, so the paper should be checked by PDF."
            elif match_status == "negative_by_abstract":
                match_reason = "Abstract matched a negative phrase from the topic spec."
            else:
                match_reason = "Title and abstract did not show strong topical evidence."

        if match_status in {
            "relevant_by_title",
            "possible_by_title",
            "relevant_by_abstract",
            "possible_match",
            "unclear_needs_pdf_review",
        }:
            matched_papers.append(
                {
                    "arxiv_id": paper.arxiv_id,
                    "title": paper.title,
                    "abstract": paper.abstract,
                    "published_utc": paper.published_utc,
                    "updated_utc": paper.updated_utc,
                    "url": paper.url,
                    "pdf_url": paper.pdf_url,
                    "match_status": match_status,
                    "match_reason": match_reason,
                    "relevance_score": max(
                        title_result["score"],
                        abstract_result["score"] if abstract_result else 0,
                    ),
                    "title_screening": title_result,
                    "abstract_screening": abstract_result,
                }
            )

    save_json(day_dir / "03_title_screening.json", title_screening)
    save_json(day_dir / "04_abstract_screening.json", abstract_screening)
    save_json(day_dir / "05_matched_papers.json", matched_papers)
    logger.log(f"Topic screening kept {len(matched_papers)} candidate paper(s) for {day_slug}.")
    print(f"✓ Screening complete: {len(matched_papers)}/{total_papers} papers matched.", file=sys.stderr)

    for matched in matched_papers:
        matched["download"] = {
            "status": "not_requested",
            "pdf_path": None,
            "error": None,
        }
        matched["full_text"] = {
            "status": "not_requested",
            "text_path": None,
            "error": None,
        }
        matched["full_text_relevance"] = None
        matched["core_content_draft"] = matched["abstract"]

    download_dir = day_dir / "downloads"
    text_dir = day_dir / "extracted_text"
    
    # Count papers that need PDF download
    papers_to_download = [
        matched for matched in matched_papers 
        if matched["match_status"] == "unclear_needs_pdf_review"
    ]
    total_downloads = len(papers_to_download)
    
    if total_downloads > 0:
        logger.log(f"Starting PDF download for {total_downloads} papers requiring full-text review.")
        print(f"Downloading {total_downloads} PDFs for full-text review...", file=sys.stderr)
    
    for download_idx, matched in enumerate(matched_papers, start=1):
        if matched["match_status"] != "unclear_needs_pdf_review":
            continue

        # Progress output for downloads
        current_download = sum(1 for m in matched_papers[:download_idx] if m["match_status"] == "unclear_needs_pdf_review")
        print(f"[{current_download}/{total_downloads}] Downloading {matched['arxiv_id']}...", file=sys.stderr)

        paper = Paper(
            arxiv_id=matched["arxiv_id"],
            title=matched["title"],
            abstract=matched["abstract"],
            published_utc=matched["published_utc"],
            updated_utc=matched["updated_utc"],
            url=matched["url"],
            pdf_url=matched["pdf_url"],
        )
        download_result = download_pdf(paper, download_dir, logger, pdf_rate_limiter)
        matched["download"] = download_result

        if download_result["status"] == "downloaded":
            extraction_result = extract_pdf_text(Path(download_result["pdf_path"]), text_dir, logger)
        else:
            extraction_result = {
                "status": "skipped",
                "text_path": None,
                "error": "PDF download failed, so text extraction was skipped.",
            }
        matched["full_text"] = extraction_result

        if extraction_result["status"] == "extracted" and extraction_result.get("text_path"):
            extracted_text = Path(extraction_result["text_path"]).read_text(
                encoding="utf-8",
                errors="ignore",
            )
            matched["full_text_relevance"] = assess_full_text_relevance(topic_data, extracted_text)
            matched["relevance_score"] = max(
                matched["relevance_score"],
                matched["full_text_relevance"]["score"],
            )
            if matched["match_status"] == "unclear_needs_pdf_review":
                if matched["full_text_relevance"]["status"] == "relevant_by_full_text":
                    matched["match_status"] = "relevant_by_full_text"
                    matched["match_reason"] = "Title and abstract were inconclusive; full text confirmed relevance."
                elif matched["full_text_relevance"]["status"] == "possible_by_full_text":
                    matched["match_status"] = "possible_by_full_text"
                    matched["match_reason"] = "Title and abstract were inconclusive; full text suggests possible relevance."
                else:
                    matched["match_status"] = "not_relevant_by_full_text"
                    matched["match_reason"] = "Full text review did not support the topic."
            matched["core_content_draft"] = build_brief_from_text(paper, extracted_text)

    matched_papers = [
        paper
        for paper in matched_papers
        if paper["match_status"]
        in {
            "relevant_by_title",
            "possible_by_title",
            "relevant_by_abstract",
            "possible_match",
            "relevant_by_full_text",
            "possible_by_full_text",
            "unclear_needs_pdf_review",
        }
    ]
    matched_papers.sort(key=lambda paper: paper.get("relevance_score", 0), reverse=True)

    save_json(day_dir / "06_downloads_and_text.json", matched_papers)

    day_manifest = {
        "topic": topic,
        "requested_date": requested_date.isoformat(),
        "resolved_date": resolved_date.isoformat() if resolved_date else None,
        "category": category,
        "timezone": tz.key,
        "day_dir": str(day_dir),
        "cache_hit": cache_hit,
        "files": {
            "request": str(day_dir / "01_request.json"),
            "all_papers_json": str(day_dir / "02_all_papers.json"),
            "all_papers_markdown": str(day_dir / "02_all_papers.md"),
            "title_screening": str(day_dir / "03_title_screening.json"),
            "abstract_screening": str(day_dir / "04_abstract_screening.json"),
            "matched_papers": str(day_dir / "05_matched_papers.json"),
            "downloads_and_text": str(day_dir / "06_downloads_and_text.json"),
            "summary_markdown": str(day_dir / "07_summary.md"),
        },
        "counts": {
            "all_papers": len(papers),
            "matched_papers": len(matched_papers),
            "downloaded_pdfs": sum(1 for paper in matched_papers if paper["download"]["status"] == "downloaded"),
            "extracted_texts": sum(1 for paper in matched_papers if paper["full_text"]["status"] == "extracted"),
        },
        "fallback_trace": fallback_trace,
        "matched_papers": matched_papers,
    }
    save_text(day_dir / "07_summary.md", render_match_summary_markdown(day_manifest))
    save_json(day_dir / "07_manifest.json", day_manifest)
    logger.log(f"Finished day-by-day processing for {day_slug}.")
    return day_manifest


def render_overall_summary(run_manifest: dict[str, Any]) -> str:
    lines = [
        f"# Multi-day topic workflow summary for '{run_manifest['topic']}'",
        "",
        f"Category: {run_manifest['category']}",
        f"Timezone: {run_manifest['timezone']}",
        f"Run directory: {run_manifest['run_dir']}",
        f"Requested day count: {run_manifest['requested_days']}",
        f"Processed day count: {len(run_manifest['days'])}",
        "",
    ]
    for day in run_manifest["days"]:
        lines.extend(
            [
                f"## Requested day {day['requested_date']}",
                f"- Resolved date: {day['resolved_date'] or 'none'}",
                f"- Cache hit: {day['cache_hit']}",
                f"- All papers: {day['counts']['all_papers']}",
                f"- Matched papers: {day['counts']['matched_papers']}",
                f"- Day directory: {day['day_dir']}",
                "",
            ]
        )
        if day["matched_papers"]:
            for index, paper in enumerate(day["matched_papers"], start=1):
                lines.extend(
                    [
                        f"### {index}. {paper['title']}",
                        f"- arXiv ID: `{paper['arxiv_id']}`",
                        f"- Relevance score: `{paper.get('relevance_score', 0)}`",
                        f"- Match status: `{paper['match_status']}`",
                        f"- PDF path: {paper.get('download', {}).get('pdf_path', '')}",
                        "",
                    ]
                )
        else:
            lines.extend(
                [
                    "No matched papers for this requested day.",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    requested_date, tz = parse_target_date(args.target_date, args.timezone)

    try:
        output_root = ensure_output_root(args.output_root)
    except Exception as exc:
        print(f"Failed to prepare output root: {exc}", file=sys.stderr)
        return 1

    run_dir = build_run_dir(output_root, args.topic, requested_date, args.category)
    logger = RunLogger(run_dir)
    api_rate_limiter = RateLimiter(min_interval_seconds=4.0)
    pdf_rate_limiter = RateLimiter(min_interval_seconds=2.0)
    try:
        topic_data = resolve_topic_data(args.topic, args.topic_spec_file)
    except Exception as exc:
        print(f"Failed to resolve topic spec: {exc}", file=sys.stderr)
        return 1
    logger.log(
        f"Starting workflow for topic='{args.topic}', start_date='{requested_date.isoformat()}', "
        f"days='{args.days}', category='{args.category}', timezone='{tz.key}'."
    )

    top_request_payload = {
        "topic": args.topic,
        "requested_start_date": requested_date.isoformat(),
        "requested_days": args.days,
        "timezone": tz.key,
        "category": args.category,
        "topic_spec_file": args.topic_spec_file,
        "resolved_topic_data": topic_data,
        "max_results": args.max_results,
        "fallback_days": args.fallback_days,
        "limit": args.limit,
        "output_root": str(output_root),
        "api_min_interval_seconds": api_rate_limiter.min_interval_seconds,
        "pdf_min_interval_seconds": pdf_rate_limiter.min_interval_seconds,
    }
    save_json(run_dir / "01_request.json", top_request_payload)

    day_manifests: list[dict[str, Any]] = []
    used_resolved_dates: set[date] = set()
    try:
        for day_offset in range(max(args.days, 1)):
            current_requested_date = requested_date - timedelta(days=day_offset)
            day_manifest = process_single_day(
                topic=args.topic,
                requested_date=current_requested_date,
                tz=tz,
                category=args.category,
                max_results=args.max_results,
                fallback_days=args.fallback_days,
                limit=args.limit,
                output_root=output_root,
                run_dir=run_dir,
                logger=logger,
                api_rate_limiter=api_rate_limiter,
                pdf_rate_limiter=pdf_rate_limiter,
                topic_data=topic_data,
                excluded_resolved_dates=used_resolved_dates,
            )
            day_manifests.append(day_manifest)
            if day_manifest["resolved_date"]:
                used_resolved_dates.add(date.fromisoformat(day_manifest["resolved_date"]))
    except Exception as exc:
        logger.log(f"Workflow failed during day-by-day processing: {exc}")
        save_json(
            run_dir / "99_error.json",
            {
                "status": "failed",
                "stage": "process_single_day",
                "topic": args.topic,
                "requested_start_date": requested_date.isoformat(),
                "requested_days": args.days,
                "category": args.category,
                "timezone": tz.key,
                "run_dir": str(run_dir),
                "error": str(exc),
                "activity_log": str(run_dir / "activity.log"),
                "request_file": str(run_dir / "01_request.json"),
                "completed_days": [day["requested_date"] for day in day_manifests],
            },
        )
        print(f"Failed to fetch arXiv data: {exc}", file=sys.stderr)
        return 1

    manifest = {
        "topic": args.topic,
        "requested_start_date": requested_date.isoformat(),
        "requested_days": args.days,
        "category": args.category,
        "timezone": tz.key,
        "run_dir": str(run_dir),
        "files": {
            "request": str(run_dir / "01_request.json"),
            "activity_log": str(run_dir / "activity.log"),
            "summary_markdown": str(run_dir / "07_summary.md"),
            "manifest_json": str(run_dir / "07_manifest.json"),
        },
        "counts": {
            "processed_days": len(day_manifests),
            "all_papers": sum(day["counts"]["all_papers"] for day in day_manifests),
            "matched_papers": sum(day["counts"]["matched_papers"] for day in day_manifests),
            "downloaded_pdfs": sum(day["counts"]["downloaded_pdfs"] for day in day_manifests),
            "extracted_texts": sum(day["counts"]["extracted_texts"] for day in day_manifests),
        },
        "days": day_manifests,
        "next_step_for_model": (
            "Tell the user which requested day is already processed, then summarize the matched papers "
            "day by day using the saved extracted_text/*.txt files when available. Save the final user-facing "
            "summary to 08_user_summary.md under the run directory."
        ),
    }
    save_text(run_dir / "07_summary.md", render_overall_summary(manifest))
    save_json(run_dir / "07_manifest.json", manifest)
    logger.log("Workflow finished successfully.")
    print(console_payload(manifest, args.output, args.verbose))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
