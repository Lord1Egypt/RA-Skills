"""Utilities shared by parser and storage modules."""

from __future__ import annotations

import asyncio
import hashlib
import ipaddress
import json
import os
import re
import socket
import threading
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, TypeVar
from urllib.parse import urlparse, urlunparse

import tldextract

from datapulse.core.cache import TTLCache

_URL_PATTERN = re.compile(r"https?://(?:[a-zA-Z0-9\-._~:/?#\[\]@!$&'()*+,;=%])+", re.IGNORECASE)
_ALLOWED_SCHEMES = {"http", "https"}
_T = TypeVar("_T")
_CONFIG_CACHE: dict[str, dict[str, str]] = {}


def extract_urls(text: str) -> list[str]:
    """Extract URLs from arbitrary text and deduplicate while preserving order."""
    found: list[str] = []
    seen: set[str] = set()
    for match in _URL_PATTERN.finditer(text):
        url = match.group(0).rstrip(".,;:!?)")
        if url in seen:
            continue
        seen.add(url)
        found.append(url)
    return found


def validate_external_url(url: str) -> tuple[bool, str]:
    """Validate URL against SSRF/host restrictions."""
    parsed = urlparse(url)
    if parsed.scheme.lower() not in _ALLOWED_SCHEMES:
        return False, "Only http/https URLs are allowed."

    host = (parsed.hostname or "").strip().lower().rstrip(".")
    if not host:
        return False, "Missing hostname."

    blocked_hosts = {"localhost", "localhost.localdomain"}
    blocked_suffix = (".local", ".internal", ".lan", ".home")
    if host in blocked_hosts or any(host.endswith(s) for s in blocked_suffix):
        return False, "Local/internal hosts are blocked."

    # literal IP
    try:
        ip_obj = ipaddress.ip_address(host)
        if any([
            ip_obj.is_private,
            ip_obj.is_loopback,
            ip_obj.is_link_local,
            ip_obj.is_multicast,
            ip_obj.is_reserved,
            ip_obj.is_unspecified,
        ]):
            return False, f"Blocked non-public IP: {ip_obj}"
        return True, ""
    except ValueError:
        pass

    try:
        addrs = {a[4][0] for a in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP) if a[4]}
    except socket.gaierror as exc:
        return False, f"DNS resolution failed: {exc}"

    if not addrs:
        return False, "No resolvable IP found."

    for ip in addrs:
        ip_obj = ipaddress.ip_address(ip)
        if any([
            ip_obj.is_private,
            ip_obj.is_loopback,
            ip_obj.is_link_local,
            ip_obj.is_multicast,
            ip_obj.is_reserved,
            ip_obj.is_unspecified,
        ]):
            return False, f"Hostname resolves to non-public IP: {ip}"

    return True, ""


def redact_url_for_log(url: str) -> str:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url
    without_query = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, "", ""))
    if parsed.query or parsed.fragment:
        return f"{without_query} [redacted]"
    return without_query


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text or "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def generate_excerpt(text: str, max_length: int = 260) -> str:
    normalized = clean_text(text)
    if len(normalized) <= max_length:
        return normalized
    cropped = normalized[:max_length].rsplit(" ", 1)[0]
    return f"{cropped}…"


def normalize_language(text: str) -> str:
    if not text:
        return "unknown"
    sample = text[:2000]
    zh_ratio = sum(1 for ch in sample if "\u4e00" <= ch <= "\u9fff") / max(1, len(sample))
    if zh_ratio > 0.05:
        return "zh"
    en_ratio = sum(1 for ch in sample if ch.isascii()) / max(1, len(sample))
    if en_ratio > 0.7:
        return "en"
    return "other"


def generate_slug(text: str, max_length: int = 70) -> str:
    ascii_text = unicodedata.normalize("NFKD", text or "")
    ascii_text = ascii_text.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-zA-Z0-9\s\-_]", "", ascii_text).strip().lower()
    ascii_text = re.sub(r"[\s\-_]+", "-", ascii_text)
    return ascii_text[:max_length] or "untitled"


def build_filename(text: str, url: str) -> str:
    date_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{date_prefix}_{generate_slug(text)[:40]}.{hashlib.sha1(url.encode()).hexdigest()[:10]}.md"


def get_domain(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if not host:
        return "unknown"
    try:
        _ = ipaddress.ip_address(host)
        return host
    except ValueError:
        ext = tldextract.extract(url)
        if ext.domain and ext.suffix:
            return f"{ext.domain}.{ext.suffix}".lower()
        return host


def get_domain_tag(url: str) -> str:
    return get_domain(url).replace(".", "_")


def content_hash(content: str) -> str:
    return hashlib.sha256((content or "").encode("utf-8")).hexdigest()


def content_fingerprint(content: str, n_shingles: int = 5) -> str:
    """Generate a fingerprint for content similarity detection.

    Normalizes text → splits into word n-gram shingles → sorts → hashes.
    Identical or near-identical content produces the same fingerprint.
    """
    text = re.sub(r"\s+", " ", (content or "").lower().strip())
    if not text:
        # Return a unique random-ish fingerprint so empty items don't
        # falsely corroborate each other.
        return hashlib.md5(os.urandom(16)).hexdigest()[:16]
    words = text.split()
    if len(words) < n_shingles:
        shingles = [" ".join(words)]
    else:
        shingles = [" ".join(words[i:i + n_shingles]) for i in range(len(words) - n_shingles + 1)]
    shingles.sort()
    combined = "|".join(shingles)
    return hashlib.md5(combined.encode("utf-8")).hexdigest()[:16]


def is_twitter_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {"twitter.com", "x.com", "mobile.twitter.com", "mobile.x.com"}


def is_reddit_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {
        "reddit.com", "www.reddit.com", "old.reddit.com", "new.reddit.com", "np.reddit.com", "m.reddit.com",
    }


def is_youtube_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {"youtube.com", "youtu.be", "www.youtube.com", "m.youtube.com"}


def is_arxiv_url(url: str) -> bool:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
        return True
    return False


def is_hackernews_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "").lower() in {"news.ycombinator.com"}


def is_rss_feed(url: str) -> bool:
    lower = url.lower()
    return lower.endswith(".xml") or "/rss" in lower or "/atom" in lower or "feed" in lower


def is_bilibili_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {"bilibili.com", "www.bilibili.com", "b23.tv"}


def is_telegram_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {"t.me", "telegram.me", "telegram.org"}


def is_xhs_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "") in {"xiaohongshu.com", "www.xiaohongshu.com", "xhslink.com"}


def is_wechat_url(url: str) -> bool:
    return "mp.weixin.qq.com" in (url or "").lower()


def is_weibo_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "").lower() in {
        "weibo.com",
        "www.weibo.com",
        "weibo.cn",
        "www.weibo.cn",
        "m.weibo.cn",
    }


def is_trending_url(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.hostname or "").lower() in {"trends24.in", "www.trends24.in"}


def resolve_platform_hint(url: str) -> str:
    if is_twitter_url(url):
        return "twitter"
    if is_reddit_url(url):
        return "reddit"
    if is_youtube_url(url):
        return "youtube"
    if is_bilibili_url(url):
        return "bilibili"
    if is_telegram_url(url):
        return "telegram"
    if is_wechat_url(url):
        return "wechat"
    if is_weibo_url(url):
        return "weibo"
    if is_xhs_url(url):
        return "xhs"
    if is_arxiv_url(url):
        return "arxiv"
    if is_hackernews_url(url):
        return "hackernews"
    if is_trending_url(url):
        return "trending"
    if is_rss_feed(url):
        return "rss"
    return "generic"


def inbox_path_from_env() -> str:
    explicit_file = os.getenv("INBOX_FILE", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = __import__("pathlib").Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate)
        return str(candidate / "unified_inbox.json")

    return "unified_inbox.json"


def watchlist_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_WATCHLIST_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_watchlist.json"))
        return str(candidate / "datapulse_watchlist.json")

    return "datapulse_watchlist.json"


def alerts_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_ALERTS_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_alerts.json"))
        return str(candidate / "datapulse_alerts.json")

    return "datapulse_alerts.json"


def alerts_markdown_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_ALERTS_MARKDOWN_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_alerts.md"))
        return str(candidate / "datapulse_alerts.md")

    return "datapulse_alerts.md"


def alert_routing_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_ALERT_ROUTING_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_alert_routes.json"))
        return str(candidate / "datapulse_alert_routes.json")

    return "datapulse_alert_routes.json"


def watch_daemon_lock_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_WATCH_DAEMON_LOCK", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix:
            return str(candidate.with_name("datapulse_watch_daemon.lock"))
        return str(candidate / "datapulse_watch_daemon.lock")

    return "datapulse_watch_daemon.lock"


def watch_status_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_WATCH_STATUS_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_watch_status.json"))
        return str(candidate / "datapulse_watch_status.json")

    return "datapulse_watch_status.json"


def watch_status_html_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_WATCH_STATUS_HTML", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix:
            return str(candidate.with_name("datapulse_watch_status.html"))
        return str(candidate / "datapulse_watch_status.html")

    return "datapulse_watch_status.html"


def stories_path_from_env() -> str:
    explicit_file = os.getenv("DATAPULSE_STORIES_PATH", "").strip()
    if explicit_file:
        return explicit_file

    memory_path = os.getenv("DATAPULSE_MEMORY_DIR", "").strip()
    if memory_path:
        candidate = Path(memory_path)
        if candidate.suffix == ".json":
            return str(candidate.with_name("datapulse_stories.json"))
        return str(candidate / "datapulse_stories.json")

    return "datapulse_stories.json"


def output_path_from_env():
    vault = os.getenv("OBSIDIAN_VAULT", "").strip()
    if vault:
        return str(__import__("pathlib").Path(vault) / "01-收集箱" / "datapulse-inbox.md")
    output_dir = os.getenv("OUTPUT_DIR", "").strip()
    if output_dir:
        return str(__import__("pathlib").Path(output_dir) / "datapulse-hub.md")
    return ""


def run_sync(coro: Awaitable[_T]) -> _T:
    """Run an awaitable from synchronous context with loop-safe semantics."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)  # type: ignore[arg-type]

    exception_holder: list[BaseException] = []
    result_holder: list[_T] = []
    done = threading.Event()

    def _runner() -> None:
        try:
            result_holder.append(asyncio.run(coro))  # type: ignore[arg-type]
        except BaseException as exc:  # noqa: BLE001
            exception_holder.append(exc)
        finally:
            done.set()

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    done.wait()
    thread.join()

    if exception_holder:
        raise exception_holder[0]
    return result_holder[0]


def load_local_context_map(context_env_key: str) -> dict[str, str]:
    """Load a local JSON context map and cache it per env key.

    Expected format example:
    {
      "DATAPULSE_SMOKE_TWITTER_URL": "https://...",
      "DATAPULSE_LOCAL_TEST_CONTEXT": "...",
      ...
    }
    """

    cache = _CONFIG_CACHE.get(context_env_key)
    if cache is not None:
        return cache

    raw_path = os.getenv(context_env_key, "").strip()
    if not raw_path:
        _CONFIG_CACHE[context_env_key] = {}
        return {}

    path = Path(raw_path).expanduser()
    if not path.exists():
        _CONFIG_CACHE[context_env_key] = {}
        return {}

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        _CONFIG_CACHE[context_env_key] = {}
        return {}

    if not isinstance(payload, dict):
        _CONFIG_CACHE[context_env_key] = {}
        return {}

    loaded = {str(k): str(v) for k, v in payload.items() if isinstance(k, str) and isinstance(v, (str, int, float, bool))}
    _CONFIG_CACHE[context_env_key] = loaded
    return loaded


def resolve_env_with_local_context(env_name: str, context_key: str) -> str:
    """Resolve env var, then fallback to local context JSON map by same key."""

    value = os.getenv(env_name, "").strip()
    if value:
        return value

    local_map = load_local_context_map(context_key)
    candidate = local_map.get(env_name, "").strip()
    return candidate


def session_dir() -> Path:
    """Return DataPulse browser session directory."""
    raw = os.getenv("DATAPULSE_SESSION_DIR", str(Path.home() / ".datapulse" / "sessions")).strip()
    directory = Path(raw).expanduser()
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def session_path(platform: str) -> str:
    """Return platform session file path for Playwright login state."""
    safe = re.sub(r"[^a-zA-Z0-9._-]", "", platform.lower())
    return str(session_dir() / f"{safe}.json")


# --- Session TTL cache (positive-only, 12h default) ---

_SESSION_TTL_SECONDS = float(os.getenv("DATAPULSE_SESSION_TTL_HOURS", "12")) * 3600
_session_ttl_cache = TTLCache(maxsize=16, ttl=_SESSION_TTL_SECONDS)


def session_valid(platform: str) -> bool:
    """TTL-cached session file existence check. Only caches positive results."""
    cached = _session_ttl_cache.get(platform)
    if cached is True:
        return True
    # Not cached (or expired) — check filesystem
    exists = Path(session_path(platform)).exists()
    if exists:
        _session_ttl_cache.set(platform, True)
    return exists


def invalidate_session_cache(platform: str) -> None:
    """Manual cache invalidation (logout/re-login)."""
    _session_ttl_cache.delete(platform)
