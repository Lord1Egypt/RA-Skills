"""V2EX platform adapter."""

from __future__ import annotations

import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen

from ..models import EvidenceReadResult, FounderSignalConfig
from ..reddit_fetcher import contains_blocked_markers, has_actual_post_content, html_to_text_snapshot, normalize_text

PLATFORM = "v2ex"
_TOPIC_URL_RE = re.compile(r"https?://(?:www\.)?v2ex\.com/t/(?P<id>\d+)(?:#[^\s\"'<>]+)?", re.I)
_TOPIC_PATH_RE = re.compile(r"^/t/(?P<id>\d+)(?:#[^\s\"'<>]+)?/?$", re.I)
_NODE_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_MAX_DISCOVERY_PAGES = 12
_DEFAULT_PROVIDERS = ("sov2ex", "site_search", "node_latest", "configured_seed_urls")
_V2EX_BLOCKED_MARKERS = (
    "你要查看的页面需要先登录",
    "需要先登录",
    "此主题已被删除",
    "主题不存在",
    "topic not found",
)


def canonicalize_v2ex_topic_url(url: str) -> str | None:
    text = url.strip()
    if not text or any(marker in text.upper() for marker in ("TOPIC_ID", "REAL_ID", "POST_ID")):
        return None
    match = _TOPIC_URL_RE.match(text)
    if match:
        return f"https://www.v2ex.com/t/{match.group('id')}"
    parsed = urlparse(text)
    if parsed.netloc.lower() in {"v2ex.com", "www.v2ex.com"}:
        path_match = _TOPIC_PATH_RE.match(parsed.path)
        if path_match:
            return f"https://www.v2ex.com/t/{path_match.group('id')}"
    return None


def is_placeholder_v2ex_url(url: str) -> bool:
    return canonicalize_v2ex_topic_url(url) is None and any(
        marker in url.upper() for marker in ("TOPIC_ID", "REAL_ID", "POST_ID")
    )


def canonical_source_id(source_url: str) -> str:
    canonical = canonicalize_v2ex_topic_url(source_url) or source_url.strip()
    return f"{PLATFORM}:{canonical}"


def discover_candidates(
    config: FounderSignalConfig,
    *,
    excluded_source_ids: set[str] | None = None,
    opener=urlopen,
    timeout_seconds: float = 20.0,
) -> list[dict[str, Any]]:
    platform_config = config.platforms.get(PLATFORM)
    if platform_config is None:
        return []
    providers = [provider.strip() for provider in platform_config.discovery_providers if provider.strip()]
    if not providers:
        providers = list(_DEFAULT_PROVIDERS)
    candidates: list[dict[str, Any]] = []
    seen_ids = {source_id for source_id in (excluded_source_ids or set()) if source_id.strip()}

    for provider in providers:
        discovered = _discover_provider(
            provider,
            config=config,
            opener=opener,
            timeout_seconds=timeout_seconds,
        )
        for source_url, discovery_url in discovered:
            _append_candidate(
                candidates=candidates,
                seen_ids=seen_ids,
                source_url=source_url,
                source_type="v2ex_discovery" if provider != "configured_seed_urls" else "configured_v2ex_hint",
                discovery_method=provider,
                discovery_url=discovery_url,
                max_candidates=config.max_candidates,
            )
            if len(candidates) >= config.max_candidates:
                return candidates

    for snapshot in config.verified_evidence_snapshots:
        if snapshot.platform != PLATFORM:
            continue
        canonical = canonicalize_v2ex_topic_url(snapshot.source_url)
        if not canonical:
            continue
        _append_candidate(
            candidates=candidates,
            seen_ids=seen_ids,
            source_url=canonical,
            source_type="verified_evidence_snapshot",
            discovery_method=snapshot.verification_method or "agent_browser",
            discovery_url="",
            max_candidates=config.max_candidates,
            extra={
                "text_snapshot": snapshot.text_snapshot,
                "verification_method": snapshot.verification_method or "agent_browser",
                "verified_by": snapshot.verified_by,
            },
        )
        if len(candidates) >= config.max_candidates:
            return candidates
    return candidates


def hydrate_candidate(candidate: dict[str, Any], run_dir: Path):
    if str(candidate.get("source_type") or "") == "verified_evidence_snapshot":
        return persist_verified_text_snapshot(
            candidate_id=str(candidate["candidate_id"]),
            source_url=str(candidate["source_url"]),
            text_snapshot=str(candidate.get("text_snapshot") or ""),
            run_dir=run_dir,
            verification_method=str(candidate.get("verification_method") or "agent_browser"),
        )
    return fetch_v2ex_evidence(
        candidate_id=str(candidate["candidate_id"]),
        source_url=str(candidate["source_url"]),
        run_dir=run_dir,
    )


def _discover_provider(provider: str, *, config: FounderSignalConfig, opener, timeout_seconds: float) -> list[tuple[str, str]]:
    platform_config = config.platforms[PLATFORM]
    if provider == "configured_seed_urls":
        return [
            (canonical, "")
            for url in platform_config.seed_urls
            if (canonical := canonicalize_v2ex_topic_url(url))
        ]
    discovery_urls = _build_discovery_urls(provider, config)
    discovered: list[tuple[str, str]] = []
    for discovery_url in discovery_urls:
        try:
            request = Request(
                discovery_url,
                headers={"User-Agent": "FounderSignal/0.1 (+read-only V2EX discovery)"},
            )
            with opener(request, timeout=timeout_seconds) as response:
                body = response.read()
                charset = getattr(response.headers, "get_content_charset", lambda default=None: default)("utf-8")
            raw = body.decode(charset or "utf-8", errors="replace")
        except Exception:
            continue
        for topic_url in _extract_discovery_topic_urls(provider, raw):
            discovered.append((topic_url, discovery_url))
            if len(discovered) >= config.max_candidates:
                return discovered
    return discovered


def _build_discovery_urls(provider: str, config: FounderSignalConfig) -> list[str]:
    platform_config = config.platforms[PLATFORM]
    terms = [item.strip() for item in [*config.keywords, *config.scoring_terms, config.product_name] if item.strip()]
    nodes = [node.strip() for node in platform_config.communities if node.strip()]
    urls: list[str] = []
    if provider == "sov2ex":
        for term in terms:
            urls.append(f"https://www.sov2ex.com/api/search?q={quote_plus(term)}")
            if len(urls) >= _MAX_DISCOVERY_PAGES:
                return urls
    elif provider == "site_search":
        for term in terms:
            urls.append(f"https://www.google.com/search?q={quote_plus('site:v2ex.com/t ' + term)}")
            if len(urls) >= _MAX_DISCOVERY_PAGES:
                return urls
    elif provider == "node_latest":
        for node in nodes:
            urls.append(f"https://www.v2ex.com/go/{quote_plus(node)}")
            if len(urls) >= _MAX_DISCOVERY_PAGES:
                return urls
    return urls


def extract_v2ex_topic_urls(raw: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for candidate in _extract_url_candidates(raw):
        canonical = canonicalize_v2ex_topic_url(candidate)
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        urls.append(canonical)
    return urls


def extract_sov2ex_topic_urls(raw: str) -> list[str]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return _dedupe_topic_urls(_extract_sov2ex_json_topic_urls(payload))


def _extract_discovery_topic_urls(provider: str, raw: str) -> list[str]:
    if provider == "sov2ex":
        urls = extract_sov2ex_topic_urls(raw)
        if urls:
            return urls
    return extract_v2ex_topic_urls(raw)


def _extract_url_candidates(raw: str) -> list[str]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        payload = None
    if payload is not None:
        return _extract_json_topic_urls(payload)

    candidates = [html.unescape(match.group(0)) for match in _TOPIC_URL_RE.finditer(raw)]
    for path_match in re.finditer(r"(?:href|url)=[\"'](?P<path>/t/\d+(?:#[^\"']+)?)", raw, re.I):
        candidates.append(f"https://www.v2ex.com{html.unescape(path_match.group('path'))}")
    return candidates


def _dedupe_topic_urls(url_candidates: list[str]) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for candidate in url_candidates:
        canonical = canonicalize_v2ex_topic_url(candidate)
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        urls.append(canonical)
    return urls


def _extract_sov2ex_json_topic_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        source = value.get("_source")
        if isinstance(source, dict):
            topic_id = source.get("id") or source.get("topic_id")
            if topic_id is not None and str(topic_id).isdigit():
                urls.append(f"https://www.v2ex.com/t/{topic_id}")
            topic_url = source.get("url")
            if isinstance(topic_url, str):
                urls.append(topic_url)
        for key in ("hits", "results", "data"):
            child = value.get(key)
            if child is not None:
                urls.extend(_extract_sov2ex_json_topic_urls(child))
        if "_source" not in value:
            for child in value.values():
                urls.extend(_extract_sov2ex_json_topic_urls(child))
    elif isinstance(value, list):
        for item in value:
            urls.extend(_extract_sov2ex_json_topic_urls(item))
    return urls


def _extract_json_topic_urls(value: Any) -> list[str]:
    urls: list[str] = []
    if isinstance(value, dict):
        topic_id = value.get("id") or value.get("topic_id")
        if topic_id is not None and str(topic_id).isdigit():
            urls.append(f"https://www.v2ex.com/t/{topic_id}")
        for key in ("url", "link", "source_url"):
            if isinstance(value.get(key), str):
                urls.append(value[key])
        for child in value.values():
            urls.extend(_extract_json_topic_urls(child))
    elif isinstance(value, list):
        for item in value:
            urls.extend(_extract_json_topic_urls(item))
    return urls


def fetch_v2ex_evidence(
    candidate_id: str,
    source_url: str,
    run_dir: Path,
    timeout_seconds: float = 20.0,
    opener=urlopen,
) -> EvidenceReadResult:
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    raw_html_path = evidence_dir / f"{candidate_id}-raw.html"
    text_snapshot_path = evidence_dir / f"{candidate_id}-text-snapshot.txt"
    source_url_path = evidence_dir / f"{candidate_id}-source-url.txt"
    evidence_url_path = evidence_dir / f"{candidate_id}-evidence-url.txt"

    canonical = canonicalize_v2ex_topic_url(source_url) or ""
    source_url_path.write_text((canonical or source_url.strip()) + "\n", encoding="utf-8")
    evidence_url_path.write_text(canonical + "\n", encoding="utf-8")
    if not canonical:
        return _persist_result(
            candidate_id=candidate_id,
            source_url=source_url.strip(),
            evidence_url="",
            raw_html="invalid v2ex topic url",
            text_snapshot="invalid v2ex topic url",
            status="not_verified_read",
            raw_html_path=raw_html_path,
            text_snapshot_path=text_snapshot_path,
            source_url_path=source_url_path,
            evidence_url_path=evidence_url_path,
        )

    encountered_error = False
    try:
        request = Request(canonical, headers={"User-Agent": "FounderSignal/0.1 (+read-only V2EX evidence)"})
        with opener(request, timeout=timeout_seconds) as response:
            body = response.read()
            charset = getattr(response.headers, "get_content_charset", lambda default=None: default)("utf-8")
        raw_html = body.decode(charset or "utf-8", errors="replace")
    except Exception as exc:
        encountered_error = True
        raw_html = str(exc)

    text_snapshot = html_to_text_snapshot(raw_html)
    blocked = _contains_v2ex_blocked_markers(raw_html) or _contains_v2ex_blocked_markers(text_snapshot)
    verified = _has_verified_v2ex_content(raw_html, text_snapshot)
    status = "verified_read_via_original" if verified and not blocked and not encountered_error else "not_verified_read"
    return _persist_result(
        candidate_id=candidate_id,
        source_url=canonical,
        evidence_url=canonical,
        raw_html=raw_html,
        text_snapshot=text_snapshot,
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
    )


def persist_verified_text_snapshot(
    *,
    candidate_id: str,
    source_url: str,
    text_snapshot: str,
    run_dir: Path,
    verification_method: str = "agent_browser",
) -> EvidenceReadResult:
    evidence_dir = run_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    raw_html_path = evidence_dir / f"{candidate_id}-raw.html"
    text_snapshot_path = evidence_dir / f"{candidate_id}-text-snapshot.txt"
    source_url_path = evidence_dir / f"{candidate_id}-source-url.txt"
    evidence_url_path = evidence_dir / f"{candidate_id}-evidence-url.txt"
    canonical = canonicalize_v2ex_topic_url(source_url) or source_url.strip()
    source_url_path.write_text(canonical + "\n", encoding="utf-8")
    evidence_url_path.write_text(canonical + "\n", encoding="utf-8")
    normalized_method = (verification_method or "agent_browser").strip().lower()
    if normalized_method not in {"agent_browser", "manual_snapshot"}:
        normalized_method = "manual_snapshot"
    status = (
        f"verified_read_via_{normalized_method}"
        if _has_verified_v2ex_content("", text_snapshot)
        else "not_verified_read"
    )
    raw_html = f"Verified snapshot fallback: {normalized_method}\nSource URL: {canonical}\n\n{text_snapshot.strip()}"
    return _persist_result(
        candidate_id=candidate_id,
        source_url=canonical,
        evidence_url=canonical,
        raw_html=raw_html,
        text_snapshot=text_snapshot.strip(),
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
    )


def validate_config_urls(config: FounderSignalConfig) -> None:
    platform_config = config.platforms.get(PLATFORM)
    if platform_config is None:
        return
    for node in platform_config.communities:
        if node.strip() and not _NODE_RE.match(node.strip()):
            raise ValueError(f"profile '{config.profile_id}' contains an invalid V2EX node: {node}")
    for url in [*platform_config.seed_urls, *platform_config.excluded_urls]:
        if is_placeholder_v2ex_url(url):
            raise ValueError(f"profile '{config.profile_id}' contains a placeholder V2EX URL: {url}")
        if url.strip() and not canonicalize_v2ex_topic_url(url):
            raise ValueError(f"profile '{config.profile_id}' contains a non-topic V2EX URL: {url}")


def _contains_v2ex_blocked_markers(text: str) -> bool:
    lowered = text.lower()
    return contains_blocked_markers(text) or any(marker in lowered for marker in _V2EX_BLOCKED_MARKERS)


def _has_verified_v2ex_content(raw_html: str, text_snapshot: str) -> bool:
    if _contains_v2ex_blocked_markers(raw_html) or _contains_v2ex_blocked_markers(text_snapshot):
        return False
    topic_text = _extract_v2ex_topic_content_text(raw_html)
    if topic_text:
        return _has_substantial_v2ex_text(topic_text)
    return _has_substantial_v2ex_text(text_snapshot)


def _extract_v2ex_topic_content_text(raw_html: str) -> str:
    if not raw_html.strip():
        return ""
    parser = _V2EXTopicContentParser()
    try:
        parser.feed(raw_html)
        parser.close()
    except Exception:
        return ""
    return parser.get_text()


class _V2EXTopicContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._capture_depth = 0
        self._stack: list[bool] = []
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        class_value = " ".join((value or "") for key, value in attrs if key == "class")
        class_names = {item.strip().lower() for item in class_value.split() if item.strip()}
        starts_capture = "topic_content" in class_names
        self._stack.append(starts_capture)
        if starts_capture:
            self._capture_depth += 1
        if self._capture_depth and tag in {"br", "p", "div", "li", "blockquote"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._capture_depth and tag in {"p", "div", "li", "blockquote"}:
            self._chunks.append("\n")
        if self._stack:
            starts_capture = self._stack.pop()
            if starts_capture and self._capture_depth:
                self._capture_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._capture_depth:
            self._chunks.append(data)

    def get_text(self) -> str:
        return html_to_text_snapshot(" ".join(self._chunks))


def _has_substantial_v2ex_text(text: str) -> bool:
    if _contains_v2ex_blocked_markers(text):
        return False
    normalized = normalize_text(text)
    if has_actual_post_content(normalized):
        return True
    cjk_chars = sum(1 for char in normalized if "\u4e00" <= char <= "\u9fff")
    if cjk_chars >= 24:
        return True
    words = [word for word in normalized.split(" ") if word]
    return len(words) >= 8 and len(normalized) >= 40


def _append_candidate(
    *,
    candidates: list[dict[str, Any]],
    seen_ids: set[str],
    source_url: str,
    source_type: str,
    discovery_method: str,
    discovery_url: str,
    max_candidates: int,
    extra: dict[str, Any] | None = None,
) -> None:
    canonical = canonicalize_v2ex_topic_url(source_url) or ""
    source_id = canonical_source_id(canonical)
    if not canonical or source_id in seen_ids or canonical in seen_ids or len(candidates) >= max_candidates:
        return
    seen_ids.add(source_id)
    candidate_id = f"cand-{len(candidates) + 1:03d}"
    payload: dict[str, Any] = {
        "candidate_id": candidate_id,
        "platform": PLATFORM,
        "source_platform": PLATFORM,
        "source_id": source_id,
        "source_url": canonical,
        "source_type": source_type,
        "discovery_method": discovery_method,
    }
    if discovery_url:
        payload["discovery_url"] = discovery_url
    if extra:
        payload.update(extra)
    candidates.append(payload)


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
) -> EvidenceReadResult:
    raw_html_path.write_text(raw_html, encoding="utf-8")
    text_snapshot_path.write_text(text_snapshot + "\n", encoding="utf-8")
    return EvidenceReadResult(
        candidate_id=candidate_id,
        source_url=source_url,
        evidence_url=evidence_url,
        status=status,
        raw_html_path=raw_html_path,
        text_snapshot_path=text_snapshot_path,
        source_url_path=source_url_path,
        evidence_url_path=evidence_url_path,
        platform=PLATFORM,
    )
