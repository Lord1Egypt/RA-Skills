"""Reddit evidence fetching via Eddrit mirror."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Pattern, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .models import RedditEvidenceReadResult, StructuredRedditEvidence

BLOCKED_MARKERS = (
    "access denied",
    "attention required",
    "checking if the site connection is secure",
    "developer token",
    "enable javascript and cookies",
    "empty shell",
    "network security",
    "please log in to continue",
    "request blocked",
    "verify you are human",
)

_REDDIT_COMMENTS_URL_RE = re.compile(
    r"^https?://(?:www\.)?reddit\.com"
    r"(?P<path>/r/[^/]+/comments/[^/]+(?:/[^/?#]+)?/?)"
    r"(?:[?#].*)?$",
    re.IGNORECASE,
)
_PLACEHOLDER_URL_RE = re.compile(r"/(?:SUB|POST_ID|REAL_ID|slug)(?:/|$)", re.IGNORECASE)
_SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.IGNORECASE | re.DOTALL)
_BLOCK_RE = re.compile(r"</?(?:p|div|section|article|main|li|ul|ol|h[1-6]|br)[^>]*>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"[ \t]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")
_ARTICLE_RE = re.compile(r"<article\b[^>]*>(?P<html>.*?)</article>", re.IGNORECASE | re.DOTALL)
_COMMENTS_SECTION_RE = re.compile(
    r"<section\b[^>]*aria-label=[\"']comments[\"'][^>]*>(?P<html>.*?)</section>",
    re.IGNORECASE | re.DOTALL,
)
_HEADING_RE = re.compile(r"<h1\b[^>]*>(?P<title>.*?)</h1>", re.IGNORECASE | re.DOTALL)
_SUBREDDIT_RE = re.compile(
    r"<a\b[^>]*href=[\"']/r/(?P<slug>[^\"'/?#]+)[^\"']*[\"'][^>]*>(?P<label>.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)
_TITLE_TAG_RE = re.compile(r"<title\b[^>]*>(?P<title>.*?)</title>", re.IGNORECASE | re.DOTALL)
_AGE_RE = re.compile(
    r"submitted\s+(?P<value>\d+)\s+"
    r"(?P<unit>seconds?|minutes?|hours?|days?|weeks?|months?|years?)\s+ago",
    re.IGNORECASE,
)
_BLOCKED_PAGE_PATTERNS: tuple[Pattern[str], ...] = (
    re.compile(r"\baccess denied\b"),
    re.compile(r"\battention required\b"),
    re.compile(r"\b(?:cloudflare|anubis)\b.{0,80}\b(?:blocked|challenge|verify|security)\b", re.DOTALL),
    re.compile(r"\b(?:blocked|request blocked)\b.{0,80}\b(?:security|network|firewall)\b", re.DOTALL),
    re.compile(r"\bchecking if the site connection is secure\b"),
    re.compile(r"\benable javascript and cookies\b"),
    re.compile(r"\bplease log in to continue\b"),
    re.compile(r"\bverify you are human\b"),
)
_PLACEHOLDER_BODY_RE = re.compile(
    r"^(?:title|same as title|see title|following|bump|any advice\??|help\??)\.?$",
    re.IGNORECASE,
)
_CHROME_LINES = {
    "eddrit",
    "open menu",
    "log in",
}


class SupportsRead(Protocol):
    def read(self) -> bytes: ...

    def headers(self) -> object: ...


def to_eddrit_url(reddit_url: str) -> str | None:
    """Convert a reddit comments URL to its Eddrit mirror URL."""
    normalized = reddit_url.strip()
    if is_placeholder_reddit_url(normalized):
        return None
    match = _REDDIT_COMMENTS_URL_RE.match(normalized)
    if not match:
        return None
    return f"https://eddrit.com{match.group('path')}"


def is_placeholder_reddit_url(reddit_url: str) -> bool:
    """Return true for template URLs that must never enter an MVP run."""
    return bool(_PLACEHOLDER_URL_RE.search(reddit_url.strip()))


def fetch_reddit_evidence(
    candidate_id: str,
    reddit_url: str,
    run_dir: Path,
    timeout_seconds: float = 20.0,
    opener=urlopen,
) -> RedditEvidenceReadResult:
    """Fetch a Reddit post through Eddrit and persist the evidence artifacts."""
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    raw_html_path = evidence_dir / f"{candidate_id}-raw.html"
    text_snapshot_path = evidence_dir / f"{candidate_id}-text-snapshot.txt"
    source_url_path = evidence_dir / f"{candidate_id}-source-url.txt"
    evidence_url_path = evidence_dir / f"{candidate_id}-evidence-url.txt"
    structured_evidence_path = evidence_dir / f"{candidate_id}-structured-evidence.json"

    source_url = reddit_url.strip()
    evidence_url = to_eddrit_url(source_url) or ""
    source_url_path.write_text(source_url + "\n", encoding="utf-8")
    evidence_url_path.write_text(evidence_url + "\n", encoding="utf-8")

    if not evidence_url:
        return _persist_result(
            candidate_id=candidate_id,
            source_url=source_url,
            evidence_url=evidence_url,
            raw_html="invalid reddit comments url",
            text_snapshot="invalid reddit comments url",
            status="not_verified_read",
            raw_html_path=raw_html_path,
            text_snapshot_path=text_snapshot_path,
            source_url_path=source_url_path,
            evidence_url_path=evidence_url_path,
            structured_evidence_path=structured_evidence_path,
        )

    encountered_http_error = False
    try:
        request = Request(
            evidence_url,
            headers={
                "User-Agent": (
                    "FounderSignal/0.1 (+https://eddrit.com mirror verification; "
                    "contact: local-run)"
                )
            },
        )
        with opener(request, timeout=timeout_seconds) as response:
            body = response.read()
            charset = getattr(response.headers, "get_content_charset", lambda default=None: default)(
                "utf-8"
            )
        raw_html = body.decode(charset or "utf-8", errors="replace")
    except HTTPError as exc:
        encountered_http_error = True
        body = exc.read()
        raw_html = body.decode("utf-8", errors="replace") if body else str(exc)
    except URLError as exc:
        raw_html = str(exc)
    except Exception as exc:  # pragma: no cover
        raw_html = str(exc)

    text_snapshot = html_to_text_snapshot(raw_html)
    structured_evidence = extract_structured_reddit_evidence(raw_html, text_snapshot=text_snapshot)
    blocked = contains_blocked_markers(raw_html) or contains_blocked_markers(text_snapshot)
    verified = has_actual_post_content(text_snapshot, structured_evidence=structured_evidence)
    status = (
        "not_verified_read"
        if encountered_http_error
        else "verified_read_via_mirror" if verified and not blocked else "not_verified_read"
    )

    return _persist_result(
        candidate_id=candidate_id,
        source_url=source_url,
        evidence_url=evidence_url,
        raw_html=raw_html,
        text_snapshot=text_snapshot,
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
        structured_evidence_path=structured_evidence_path,
        structured_evidence=structured_evidence,
    )


def persist_verified_text_snapshot(
    *,
    candidate_id: str,
    reddit_url: str,
    text_snapshot: str,
    run_dir: Path,
    verification_method: str = "agent_browser",
) -> RedditEvidenceReadResult:
    """Persist an agent/browser verified Reddit snapshot when mirrors are blocked."""
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    raw_html_path = evidence_dir / f"{candidate_id}-raw.html"
    text_snapshot_path = evidence_dir / f"{candidate_id}-text-snapshot.txt"
    source_url_path = evidence_dir / f"{candidate_id}-source-url.txt"
    evidence_url_path = evidence_dir / f"{candidate_id}-evidence-url.txt"
    structured_evidence_path = evidence_dir / f"{candidate_id}-structured-evidence.json"

    source_url = reddit_url.strip()
    normalized_method = (verification_method or "agent_browser").strip().lower()
    if normalized_method not in {"agent_browser", "manual_snapshot"}:
        normalized_method = "manual_snapshot"
    normalized_snapshot = text_snapshot.strip()
    structured_evidence = extract_structured_reddit_evidence("", text_snapshot=normalized_snapshot)
    status = (
        f"verified_read_via_{normalized_method}"
        if has_actual_post_content(normalized_snapshot, structured_evidence=structured_evidence)
        else "not_verified_read"
    )
    raw_html = (
        f"Verified snapshot fallback: {normalized_method}\n"
        f"Source URL: {source_url}\n\n"
        f"{normalized_snapshot}"
    )
    return _persist_result(
        candidate_id=candidate_id,
        source_url=source_url,
        evidence_url=source_url,
        raw_html=raw_html,
        text_snapshot=normalized_snapshot,
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
        structured_evidence_path=structured_evidence_path,
        structured_evidence=structured_evidence,
    )


def persist_failed_evidence_read(
    *,
    candidate_id: str,
    reddit_url: str,
    run_dir: Path,
    error_message: str,
) -> RedditEvidenceReadResult:
    """Persist a not-verified evidence record when a candidate fetch fails unexpectedly."""
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    raw_html_path = evidence_dir / f"{candidate_id}-raw.html"
    text_snapshot_path = evidence_dir / f"{candidate_id}-text-snapshot.txt"
    source_url_path = evidence_dir / f"{candidate_id}-source-url.txt"
    evidence_url_path = evidence_dir / f"{candidate_id}-evidence-url.txt"
    structured_evidence_path = evidence_dir / f"{candidate_id}-structured-evidence.json"

    source_url = reddit_url.strip()
    evidence_url = to_eddrit_url(source_url) or source_url
    failure_text = (
        "Founder Signal evidence fetch failed before verification.\n"
        f"Source URL: {source_url}\n"
        f"Error: {error_message.strip() or 'unknown error'}"
    )
    source_url_path.write_text(source_url + "\n", encoding="utf-8")
    evidence_url_path.write_text(evidence_url + "\n", encoding="utf-8")
    return _persist_result(
        candidate_id=candidate_id,
        source_url=source_url,
        evidence_url=evidence_url,
        raw_html=failure_text,
        text_snapshot=failure_text,
        status="not_verified_read",
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
        structured_evidence_path=structured_evidence_path,
    )


def contains_blocked_markers(text: str) -> bool:
    haystack = text.lower()
    if any(marker in haystack for marker in BLOCKED_MARKERS):
        return True
    return any(pattern.search(haystack) for pattern in _BLOCKED_PAGE_PATTERNS)


def has_actual_post_content(
    text_snapshot: str,
    *,
    structured_evidence: StructuredRedditEvidence | None = None,
) -> bool:
    if contains_blocked_markers(text_snapshot):
        return False
    text = normalize_text(text_snapshot)
    if len(text) < 60:
        return False
    words = [word for word in text.split(" ") if word]
    if len(words) < 8:
        return False
    if structured_evidence is None:
        structured_evidence = extract_structured_reddit_evidence("", text_snapshot=text_snapshot)
    return structured_evidence.extraction_quality != "failed"


def html_to_text_snapshot(raw_html: str) -> str:
    without_scripts = _SCRIPT_STYLE_RE.sub(" ", raw_html)
    with_breaks = _BLOCK_RE.sub("\n", without_scripts)
    without_tags = _TAG_RE.sub(" ", with_breaks)
    unescaped = html.unescape(without_tags)
    return normalize_text(unescaped)


def normalize_text(text: str) -> str:
    normalized_lines: list[str] = []
    for line in text.replace("\r", "\n").split("\n"):
        compact = _SPACE_RE.sub(" ", line).strip()
        if compact:
            normalized_lines.append(compact)
        elif normalized_lines and normalized_lines[-1] != "":
            normalized_lines.append("")
    return _BLANK_LINES_RE.sub("\n\n", "\n".join(normalized_lines)).strip()


def extract_structured_reddit_evidence(
    raw_html: str,
    *,
    text_snapshot: str | None = None,
) -> StructuredRedditEvidence:
    raw_snapshot = normalize_text(text_snapshot or html_to_text_snapshot(raw_html))
    if raw_html and "<" in raw_html and ">" in raw_html:
        structured = _extract_structured_evidence_from_html(raw_html, raw_snapshot=raw_snapshot)
        if any(
            (
                structured.post_title,
                structured.post_body,
                structured.subreddit,
                structured.comments_excerpt,
            )
        ):
            return structured
    return _extract_structured_evidence_from_text_snapshot(raw_snapshot)


def _extract_structured_evidence_from_html(
    raw_html: str,
    *,
    raw_snapshot: str,
) -> StructuredRedditEvidence:
    without_scripts = _SCRIPT_STYLE_RE.sub(" ", raw_html)
    article_html = _first_capture(_ARTICLE_RE, without_scripts)
    comments_html = _first_capture(_COMMENTS_SECTION_RE, without_scripts)

    post_title = ""
    post_body = ""
    if article_html:
        post_title = _clean_html_text(_first_capture(_HEADING_RE, article_html))
        body_html = _HEADING_RE.sub(" ", article_html, count=1)
        post_body = _clean_html_text(body_html)
    if not post_title:
        post_title = _clean_page_title(_clean_html_text(_first_capture(_TITLE_TAG_RE, without_scripts)))

    subreddit = _extract_subreddit(without_scripts, raw_snapshot=raw_snapshot)
    comments_excerpt = _comments_excerpt_from_html(comments_html)
    extraction_quality = _classify_extraction_quality(post_title, post_body)
    return StructuredRedditEvidence(
        post_title=post_title,
        post_body=post_body,
        subreddit=subreddit,
        comments_excerpt=comments_excerpt,
        extraction_quality=extraction_quality,
        raw_text_snapshot=raw_snapshot,
        post_age_days=_parse_post_age_days(raw_snapshot),
    )


def _extract_structured_evidence_from_text_snapshot(raw_snapshot: str) -> StructuredRedditEvidence:
    lines = [line for line in raw_snapshot.splitlines() if line.strip()]
    if not lines:
        return StructuredRedditEvidence("", "", "", "", "failed", "", None)

    cleaned_lines: list[str] = []
    for line in lines:
        compact = normalize_text(line)
        if compact.lower() in _CHROME_LINES:
            continue
        if compact not in cleaned_lines:
            cleaned_lines.append(compact)

    subreddit = ""
    if cleaned_lines and cleaned_lines[0].lower().startswith("r/"):
        subreddit = cleaned_lines.pop(0)

    comment_index = next(
        (index for index, line in enumerate(cleaned_lines) if line.lower() == "comments"),
        None,
    )
    comment_lines: list[str] = []
    if comment_index is not None:
        comment_lines = cleaned_lines[comment_index + 1 :]
        cleaned_lines = cleaned_lines[:comment_index]

    post_title = cleaned_lines[0] if cleaned_lines else ""
    post_body = "\n\n".join(cleaned_lines[1:] if len(cleaned_lines) > 1 else []).strip()
    comments_excerpt = _limit_comment_excerpt(comment_lines)
    extraction_quality = _classify_extraction_quality(post_title, post_body)
    return StructuredRedditEvidence(
        post_title=post_title,
        post_body=post_body,
        subreddit=subreddit,
        comments_excerpt=comments_excerpt,
        extraction_quality=extraction_quality,
        raw_text_snapshot=raw_snapshot,
        post_age_days=_parse_post_age_days(raw_snapshot),
    )


def _first_capture(pattern: Pattern[str], text: str) -> str:
    match = pattern.search(text)
    if not match:
        return ""
    return str(match.group(1)).strip()


def _clean_html_text(fragment: str) -> str:
    return html_to_text_snapshot(fragment) if fragment else ""


def _clean_page_title(title: str) -> str:
    compact = normalize_text(title)
    if not compact:
        return ""
    if " - " in compact and compact.lower().startswith("eddrit - "):
        parts = [part.strip() for part in compact.split(" - ") if part.strip()]
        if parts:
            return parts[-1]
    return compact


def _extract_subreddit(raw_html: str, *, raw_snapshot: str) -> str:
    title_subreddit = _subreddit_from_page_title(raw_html)
    if title_subreddit and title_subreddit.lower() != "r/all":
        return title_subreddit

    fallback = ""
    for match in _SUBREDDIT_RE.finditer(raw_html):
        label = _clean_html_text(match.group("label"))
        if label.lower().startswith("r/"):
            candidate = label
        else:
            slug = str(match.group("slug")).strip()
            candidate = f"r/{slug}" if slug else ""
        if candidate and candidate.lower() != "r/all":
            return candidate
        if candidate and not fallback:
            fallback = candidate

    if fallback:
        return fallback

    for line in raw_snapshot.splitlines():
        if line.lower().startswith("r/"):
            candidate = line.strip()
            if candidate.lower() != "r/all":
                return candidate
            if not fallback:
                fallback = candidate
    return fallback


def _subreddit_from_page_title(raw_html: str) -> str:
    title = _clean_html_text(_first_capture(_TITLE_TAG_RE, raw_html))
    for part in (item.strip() for item in title.split(" - ")):
        if part.lower().startswith("r/"):
            return part
    return ""


def _parse_post_age_days(text: str) -> int | None:
    match = _AGE_RE.search(text)
    if not match:
        return None
    value = int(match.group("value"))
    unit = match.group("unit").lower().rstrip("s")
    multipliers = {
        "second": 1 / 86400,
        "minute": 1 / 1440,
        "hour": 1 / 24,
        "day": 1,
        "week": 7,
        "month": 30,
        "year": 365,
    }
    multiplier = multipliers.get(unit)
    return None if multiplier is None else int(value * multiplier)


def _comments_excerpt_from_html(comments_html: str) -> str:
    if not comments_html:
        return ""
    lines = [
        line
        for line in html_to_text_snapshot(comments_html).splitlines()
        if line.strip() and line.strip().lower() != "comments"
    ]
    return _limit_comment_excerpt(lines)


def _limit_comment_excerpt(lines: list[str]) -> str:
    excerpt_lines = [line for line in lines if line.strip()]
    if not excerpt_lines:
        return ""
    return "\n\n".join(excerpt_lines[:4]).strip()


def _classify_extraction_quality(post_title: str, post_body: str) -> str:
    if _is_usable_post_title(post_title) and _is_usable_post_body(post_body):
        return "high"
    return "failed"


def _is_usable_post_title(post_title: str) -> bool:
    compact = normalize_text(post_title)
    return bool(compact) and len([word for word in compact.split(" ") if word]) >= 3


def _is_usable_post_body(post_body: str) -> bool:
    compact = normalize_text(post_body)
    if not compact or _PLACEHOLDER_BODY_RE.fullmatch(compact):
        return False
    words = [word for word in compact.split(" ") if word]
    return len(words) >= 8 and len(compact) >= 40


def _persist_result(
    *,
    candidate_id: str,
    source_url: str,
    evidence_url: str,
    raw_html: str,
    text_snapshot: str,
    status: str,
    raw_html_path: Path,
    text_snapshot_path: Path,
    source_url_path: Path,
    evidence_url_path: Path,
    structured_evidence_path: Path | None = None,
    structured_evidence: StructuredRedditEvidence | None = None,
) -> RedditEvidenceReadResult:
    normalized_snapshot = text_snapshot.strip()
    if structured_evidence is None:
        structured_evidence = extract_structured_reddit_evidence(raw_html, text_snapshot=normalized_snapshot)
    if structured_evidence_path is None:
        structured_evidence_path = raw_html_path.parent / f"{candidate_id}-structured-evidence.json"
    raw_html_path.write_text(raw_html, encoding="utf-8")
    text_snapshot_path.write_text(normalized_snapshot + "\n", encoding="utf-8")
    structured_evidence_path.write_text(
        json.dumps(structured_evidence.to_dict(), indent=2) + "\n",
        encoding="utf-8",
    )
    return RedditEvidenceReadResult(
        candidate_id=candidate_id,
        source_url=source_url,
        evidence_url=evidence_url,
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
        structured_evidence_path=structured_evidence_path,
        structured_evidence=structured_evidence,
    )
