#!/usr/bin/env python3
"""
Fetch podcast and YouTube episode metadata from unified sources configuration.
"""

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from urllib.error import URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

try:
    import feedparser

    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False

TIMEOUT = 30
MAX_EPISODES_PER_SOURCE = 20
YOUTUBE_PLAYLIST_ITEM_SPEC = f"1:{MAX_EPISODES_PER_SOURCE},-{MAX_EPISODES_PER_SOURCE}:"
YOUTUBE_METADATA_WORKERS = 4
PODCAST_CACHE_PATH = "/tmp/follow-news-podcast-cache.json"
METADATA_CACHE_TTL_SECONDS = 3600
METADATA_CACHE_VERSION = 2
TRANSCRIPT_SUCCESS_TTL_SECONDS = 30 * 86400
TRANSCRIPT_FAILURE_TTL_SECONDS = 6 * 3600
XIAOYUZHOU_HOSTS = {"xiaoyuzhoufm.com", "www.xiaoyuzhoufm.com"}
OPENCLI_EMPTY_RESULT_EXIT_CODE = 66


def setup_logging(verbose: bool) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def infer_platform(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}:
        return "youtube"
    if extract_xiaoyuzhou_podcast_id(url):
        return "xiaoyuzhou"
    return "rss"


def extract_xiaoyuzhou_podcast_id(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host not in XIAOYUZHOU_HOSTS:
        return ""
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) == 2 and parts[0] == "podcast" and parts[1]:
        return parts[1]
    return ""


def xiaoyuzhou_episode_id_from_episode(episode: Dict[str, Any]) -> str:
    guid = str(episode.get("guid") or "").strip()
    if guid.startswith("xiaoyuzhou:"):
        return guid.split(":", 1)[1].strip()
    link = str(episode.get("link") or "").strip()
    parsed = urlparse(link)
    host = (parsed.hostname or "").lower()
    if host in XIAOYUZHOU_HOSTS:
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2 and parts[0] == "episode":
            return parts[1]
    return ""


def parse_podcast_date(value: str) -> Optional[datetime]:
    if not value:
        return None
    value = value.strip()
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()


def extract_cdata(value: str) -> str:
    match = re.search(r"<!\[CDATA\[(.*?)\]\]>", value or "", re.DOTALL)
    return match.group(1) if match else (value or "")


def get_tag(xml: str, tag: str) -> str:
    match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", xml, re.DOTALL | re.IGNORECASE)
    return extract_cdata(match.group(1)).strip() if match else ""


def resolve_link(link: str, base_url: str) -> str:
    if not link:
        return ""
    if link.startswith(("http://", "https://")):
        return link
    resolved = urljoin(base_url, link)
    if resolved.startswith(("http://", "https://")):
        return resolved
    return ""


def transcript_config(source: Dict[str, Any]) -> Dict[str, Any]:
    value = source.get("transcript")
    if isinstance(value, dict):
        return value
    return {"enabled": False}


def build_episode(
    source: Dict[str, Any],
    title: str,
    link: str,
    published: datetime,
    guid: str,
    platform: str,
) -> Dict[str, Any]:
    config = transcript_config(source)
    episode = {
        "title": title[:300],
        "link": link,
        "date": published.astimezone(timezone.utc).isoformat(),
        "guid": guid or link,
        "topics": list(source.get("topics", [])),
        "show_name": source.get("name", ""),
        "platform": platform,
        "transcript_status": "disabled",
    }
    if config.get("enabled") is True:
        episode["transcript_status"] = "missing"
    return episode


def newest_episodes(episodes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(episodes, key=lambda episode: episode["date"], reverse=True)[:MAX_EPISODES_PER_SOURCE]


def parse_rss_episodes(
    content: str,
    source: Dict[str, Any],
    cutoff: datetime,
) -> List[Dict[str, Any]]:
    feed_url = source.get("url", "")
    episodes: List[Dict[str, Any]] = []
    if HAS_FEEDPARSER:
        feed = feedparser.parse(content)
        for entry in feed.entries:
            title = str(entry.get("title", "")).strip()
            link = resolve_link(str(entry.get("link", "")).strip(), feed_url)
            guid = str(entry.get("id") or entry.get("guid") or link)
            date_value = str(entry.get("published") or entry.get("updated") or "")
            published = parse_podcast_date(date_value)
            if title and link and published and published >= cutoff:
                episodes.append(build_episode(source, title, link, published, guid, "rss"))
        if episodes:
            return newest_episodes(episodes)

    for item in re.finditer(r"<item[^>]*>(.*?)</item>", content, re.DOTALL | re.IGNORECASE):
        block = item.group(1)
        title = strip_tags(get_tag(block, "title"))
        link = resolve_link(get_tag(block, "link"), feed_url)
        guid = get_tag(block, "guid") or link
        published = parse_podcast_date(get_tag(block, "pubDate") or get_tag(block, "dc:date"))
        if title and link and published and published >= cutoff:
            episodes.append(build_episode(source, title, link, published, guid, "rss"))
    return newest_episodes(episodes)


def youtube_video_id(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if host == "youtu.be":
        return parsed.path.strip("/")
    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
        query = parsed.query.split("&") if parsed.query else []
        for part in query:
            if part.startswith("v="):
                return part.split("=", 1)[1]
    return ""


def is_http_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https"}


def timestamp_to_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return None


def parse_youtube_date(value: Any) -> Optional[datetime]:
    if not value:
        return None
    text = str(value).strip()
    if re.match(r"^\d{8}$", text):
        try:
            return datetime.strptime(text, "%Y%m%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return parse_podcast_date(text)


def parse_xiaoyuzhou_date(value: Any) -> Optional[datetime]:
    if not value:
        return None
    text = str(value).strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        try:
            return datetime.strptime(text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            return None
    return parse_podcast_date(text)


def xiaoyuzhou_published_before_cutoff(value: Any, published: datetime, cutoff: datetime) -> bool:
    text = str(value or "").strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
        return published.date() < cutoff.date()
    return published < cutoff


def normalize_youtube_metadata(
    payload: Dict[str, Any],
    source: Dict[str, Any],
    cutoff: datetime,
) -> List[Dict[str, Any]]:
    raw_entries = payload.get("entries") if isinstance(payload, dict) else None
    if raw_entries is None:
        raw_entries = [payload]

    episodes: List[Dict[str, Any]] = []
    seen_video_ids: Set[str] = set()
    for entry in raw_entries:
        if not isinstance(entry, dict):
            continue

        title = str(entry.get("title") or "").strip()
        link = str(entry.get("webpage_url") or entry.get("url") or "").strip()
        video_id = str(entry.get("id") or youtube_video_id(link)).strip()
        if link and not is_http_url(link):
            link = ""
        published = youtube_entry_published_at(entry)
        if not link and video_id:
            link = f"https://www.youtube.com/watch?v={video_id}"
        if not title or not link or not video_id or not published or published < cutoff:
            continue
        if video_id in seen_video_ids:
            continue
        seen_video_ids.add(video_id)

        episode = build_episode(
            source,
            title,
            link,
            published,
            f"youtube:{video_id}",
            "youtube",
        )
        duration = entry.get("duration")
        if isinstance(duration, (int, float)) and duration > 0:
            episode["duration_seconds"] = int(duration)
        episodes.append(episode)

    return newest_episodes(episodes)


def normalize_xiaoyuzhou_metadata(
    payload: Any,
    source: Dict[str, Any],
    cutoff: datetime,
) -> List[Dict[str, Any]]:
    if not isinstance(payload, list):
        raise RuntimeError("opencli xiaoyuzhou podcast-episodes output was not a list")

    episodes: List[Dict[str, Any]] = []
    seen_episode_ids: Set[str] = set()
    for entry in payload:
        if not isinstance(entry, dict):
            continue

        episode_id = str(entry.get("eid") or "").strip()
        title = str(entry.get("title") or "").strip()
        raw_date = entry.get("date")
        published = parse_xiaoyuzhou_date(raw_date)
        if not episode_id or not title or not published:
            continue
        if xiaoyuzhou_published_before_cutoff(raw_date, published, cutoff):
            continue
        if episode_id in seen_episode_ids:
            continue
        seen_episode_ids.add(episode_id)

        episode = build_episode(
            source,
            title,
            f"https://www.xiaoyuzhoufm.com/episode/{episode_id}",
            published,
            f"xiaoyuzhou:{episode_id}",
            "xiaoyuzhou",
        )
        episodes.append(episode)

    return newest_episodes(episodes)


def youtube_entry_published_at(entry: Dict[str, Any]) -> Optional[datetime]:
    return timestamp_to_datetime(entry.get("timestamp")) or parse_youtube_date(
        entry.get("upload_date") or entry.get("release_date")
    )


def youtube_entry_has_precise_published_at(entry: Dict[str, Any]) -> bool:
    return timestamp_to_datetime(entry.get("timestamp")) is not None


def youtube_entry_link(entry: Dict[str, Any]) -> str:
    link = str(entry.get("webpage_url") or entry.get("url") or "").strip()
    video_id = str(entry.get("id") or youtube_video_id(link)).strip()
    if link and is_http_url(link):
        return link
    if video_id:
        return f"https://www.youtube.com/watch?v={video_id}"
    return ""


def resolve_ytdlp_bin() -> Optional[str]:
    configured = os.environ.get("YTDLP_BIN") or os.environ.get("YT_DLP_BIN")
    if configured:
        return configured

    from shutil import which

    return which("yt-dlp")


def resolve_opencli_bin() -> Optional[str]:
    configured = os.environ.get("OPENCLI_BIN")
    if configured:
        return configured
    return shutil.which("opencli")


def run_opencli_json(opencli_bin: str, args: List[str], timeout: int = 90) -> Any:
    import subprocess

    cmd = [opencli_bin] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("opencli command timed out") from exc
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc

    if result.returncode == OPENCLI_EMPTY_RESULT_EXIT_CODE:
        return []

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "opencli command failed").strip()
        raise RuntimeError(message[:300])

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("opencli output was not valid JSON") from exc


def source_identity(source: Dict[str, Any]) -> str:
    return str(
        source.get("id")
        or source.get("url")
        or source.get("name")
        or ""
    )


def transcript_cache_key(episode: Dict[str, Any], source: Optional[Dict[str, Any]] = None) -> str:
    episode_key = str(episode.get("guid") or episode.get("link") or episode.get("title") or "")
    source_key = source_identity(source or {})
    if source_key and episode_key:
        return f"{source_key}:{episode_key}"
    return episode_key


def transcript_languages(source: Dict[str, Any]) -> List[str]:
    config = transcript_config(source)
    languages = config.get("languages")
    if isinstance(languages, list) and languages:
        normalized = [
            language.strip()
            for language in languages
            if isinstance(language, str) and language.strip()
        ]
        if normalized:
            return normalized
    return ["en", "zh", "zh-Hans"]


def run_ytdlp_transcript(
    ytdlp_bin: str,
    episode: Dict[str, Any],
    languages: List[str],
    timeout: int = 60,
) -> Dict[str, str]:
    import subprocess

    preferred_languages = [str(language).strip() for language in languages if str(language).strip()]
    if not preferred_languages:
        return {"status": "missing", "error": "No subtitle languages configured"}

    last_error: Optional[Dict[str, str]] = None
    with tempfile.TemporaryDirectory(prefix="follow-news-ytdlp-") as tmpdir:
        for index, language in enumerate(preferred_languages):
            language_dir = Path(tmpdir) / str(index)
            language_dir.mkdir(parents=True, exist_ok=True)
            cmd = [
                ytdlp_bin,
                "--skip-download",
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                language,
                "--sub-format",
                "vtt",
                "--convert-subs",
                "vtt",
                "--output",
                str(language_dir / "%(id)s.%(ext)s"),
                "--no-playlist",
                episode["link"],
            ]
            try:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                return {"status": "timeout", "error": "yt-dlp transcript command timed out"}
            except OSError as exc:
                return {"status": "error", "error": str(exc)[:200]}

            if result.returncode != 0:
                message = (result.stderr or result.stdout or "yt-dlp transcript command failed").strip()
                last_error = {"status": "error", "error": message[:200]}
                continue

            vtt_files = sorted(language_dir.glob("*.vtt"))
            if not vtt_files:
                continue

            for vtt_file in vtt_files:
                try:
                    transcript = parse_vtt_transcript(
                        vtt_file.read_text(encoding="utf-8", errors="replace")
                    )
                except OSError as exc:
                    last_error = {"status": "parse_error", "error": str(exc)[:200]}
                    continue
                if transcript.strip():
                    return {"status": "ok", "transcript": transcript}
                last_error = {
                    "status": "parse_error",
                    "error": "Subtitle file did not contain transcript text",
                }

    return last_error or {"status": "missing", "error": "No subtitle track found"}


def run_opencli_transcript(
    opencli_bin: str,
    episode: Dict[str, Any],
    timeout: int = 120,
) -> Dict[str, str]:
    episode_id = xiaoyuzhou_episode_id_from_episode(episode)
    if not episode_id:
        return {"status": "error", "error": "Xiaoyuzhou episode id not found"}

    with tempfile.TemporaryDirectory(prefix="follow-news-xiaoyuzhou-transcript-") as tmpdir:
        try:
            payload = run_opencli_json(
                opencli_bin,
                [
                    "xiaoyuzhou",
                    "transcript",
                    episode_id,
                    "--output",
                    tmpdir,
                    "-f",
                    "json",
                ],
                timeout=timeout,
            )
        except RuntimeError as exc:
            return {"status": "error", "error": str(exc)[:200]}

        rows = payload if isinstance(payload, list) else [payload]
        output_dir = Path(tmpdir).resolve()
        for row in rows:
            if not isinstance(row, dict):
                continue
            text_file = str(row.get("text_file") or "").strip()
            if not text_file or text_file == "-":
                continue
            text_path = Path(text_file)
            if not text_path.is_absolute():
                text_path = output_dir / text_path
            try:
                resolved_text_path = text_path.resolve()
                if os.path.commonpath([str(output_dir), str(resolved_text_path)]) != str(output_dir):
                    return {
                        "status": "error",
                        "error": "opencli transcript text_file is outside output directory",
                    }
            except ValueError:
                return {
                    "status": "error",
                    "error": "opencli transcript text_file is outside output directory",
                }
            except OSError as exc:
                return {"status": "error", "error": str(exc)[:200]}
            try:
                transcript = resolved_text_path.read_text(encoding="utf-8", errors="replace").strip()
            except OSError as exc:
                return {"status": "error", "error": str(exc)[:200]}
            if transcript:
                return {"status": "ok", "transcript": transcript}

    return {"status": "missing", "error": "No transcript text returned by opencli"}


def parse_vtt_transcript(content: str) -> str:
    lines: List[str] = []
    current_time = ""
    last_text = ""
    in_note = False
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            in_note = False
            continue
        if in_note:
            continue
        if line.startswith("NOTE"):
            in_note = True
            continue
        if line == "WEBVTT" or line.startswith(("Kind:", "Language:")):
            continue
        if "-->" in line:
            current_time = line.split("-->", 1)[0].strip()
            continue
        if re.match(r"^\d+$", line):
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        if text:
            if text == last_text:
                continue
            if current_time:
                lines.append(f"{current_time} {text}")
            else:
                lines.append(text)
            last_text = text
    return "\n".join(lines)


def cache_entry_valid(entry: Dict[str, Any], now: float) -> bool:
    status = entry.get("status")
    ttl = TRANSCRIPT_SUCCESS_TTL_SECONDS if status == "ok" else TRANSCRIPT_FAILURE_TTL_SECONDS
    try:
        ts = float(entry.get("ts", 0))
    except (TypeError, ValueError):
        return False
    return now - ts < ttl


def metadata_cache_key(source: Dict[str, Any], resolved_url: Optional[str] = None) -> str:
    def xiaoyuzhou_cache_key(podcast_id: str) -> str:
        return f"xiaoyuzhou:{podcast_id}:{MAX_EPISODES_PER_SOURCE}:v{METADATA_CACHE_VERSION}"

    source_url = source.get("url", "")
    url = resolved_url or source_url
    configured_platform = source.get("platform")
    platform = str(configured_platform or "").strip()

    if not platform or platform == "auto":
        inferred_platform = infer_platform(url)
        podcast_id = extract_xiaoyuzhou_podcast_id(url)
        if inferred_platform == "xiaoyuzhou" and podcast_id:
            return xiaoyuzhou_cache_key(podcast_id)
        return f"{inferred_platform}:{url}:{MAX_EPISODES_PER_SOURCE}:v{METADATA_CACHE_VERSION}"

    if platform == "xiaoyuzhou":
        podcast_id = extract_xiaoyuzhou_podcast_id(url) or extract_xiaoyuzhou_podcast_id(source_url)
        if podcast_id:
            return xiaoyuzhou_cache_key(podcast_id)

    return f"{platform}:{url}:{MAX_EPISODES_PER_SOURCE}:v{METADATA_CACHE_VERSION}"


def cached_metadata_payload(
    cache: Dict[str, Any],
    cache_key: str,
    now: float,
    expected_type: type,
) -> Optional[Any]:
    cached = cache.get("metadata", {}).get(cache_key)
    if not isinstance(cached, dict) or not metadata_cache_entry_valid(cached, now):
        return None
    payload = cached.get("payload")
    if isinstance(payload, expected_type):
        return payload
    return None


def metadata_cache_entry_valid(entry: Dict[str, Any], now: float) -> bool:
    try:
        ts = float(entry.get("ts", 0))
    except (TypeError, ValueError):
        return False
    return now - ts < METADATA_CACHE_TTL_SECONDS and isinstance(entry.get("payload"), (dict, list))


def enrich_episode_transcript(
    episode: Dict[str, Any],
    source: Dict[str, Any],
    cache: Dict[str, Any],
    no_cache: bool = False,
) -> Dict[str, Any]:
    config = transcript_config(source)
    if config.get("enabled") is not True:
        episode["transcript_status"] = "disabled"
        return episode

    key = transcript_cache_key(episode, source)
    now = time.time()
    if key and not no_cache:
        cached = cache.get("transcripts", {}).get(key)
        if isinstance(cached, dict) and cache_entry_valid(cached, now):
            episode["transcript_status"] = cached.get("status", "error")
            if cached.get("transcript"):
                episode["transcript"] = cached["transcript"]
            if cached.get("error"):
                episode["transcript_error"] = cached["error"]
            return episode

    backend = config.get("backend", "auto")
    if backend not in {"auto", "yt-dlp", "opencli"}:
        episode["transcript_status"] = "error"
        episode["transcript_error"] = f"Unsupported transcript backend: {backend}"
        return episode
    if backend == "opencli" and episode.get("platform") != "xiaoyuzhou":
        episode["transcript_status"] = "error"
        episode["transcript_error"] = (
            "opencli transcript backend is only supported for Xiaoyuzhou episodes"
        )
        episode.pop("transcript", None)
        return episode

    if backend == "opencli" or (backend == "auto" and episode.get("platform") == "xiaoyuzhou"):
        opencli_bin = resolve_opencli_bin()
        if not opencli_bin:
            result = {"status": "backend_unavailable", "error": "opencli is not available"}
        else:
            result = run_opencli_transcript(opencli_bin, episode)
    else:
        ytdlp_bin = resolve_ytdlp_bin()
        if not ytdlp_bin:
            result = {"status": "backend_unavailable", "error": "yt-dlp is not available"}
        else:
            result = run_ytdlp_transcript(ytdlp_bin, episode, transcript_languages(source))

    episode["transcript_status"] = result.get("status", "error")
    episode.pop("transcript", None)
    episode.pop("transcript_error", None)
    if result.get("transcript"):
        episode["transcript"] = result["transcript"]
    if result.get("error"):
        episode["transcript_error"] = result["error"]

    if key:
        cache.setdefault("transcripts", {})[key] = {
            "status": episode["transcript_status"],
            "transcript": episode.get("transcript", ""),
            "error": episode.get("transcript_error", ""),
            "ts": now,
        }
    return episode


def load_podcast_sources(defaults_dir: Path, config_dir: Optional[Path] = None) -> List[Dict[str, Any]]:
    try:
        from config_loader import load_merged_sources
    except ImportError:
        sys.path.append(str(Path(__file__).parent))
        from config_loader import load_merged_sources

    all_sources = load_merged_sources(defaults_dir, config_dir)
    sources = [
        source
        for source in all_sources
        if source.get("type") == "podcast" and source.get("enabled", True)
    ]
    logging.info("Loaded %d enabled podcast sources", len(sources))
    return sources


def load_podcast_cache(no_cache: bool = False) -> Dict[str, Any]:
    if no_cache:
        return {"metadata": {}, "transcripts": {}}

    try:
        with open(PODCAST_CACHE_PATH, "r", encoding="utf-8") as handle:
            cache = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {"metadata": {}, "transcripts": {}}

    if not isinstance(cache, dict):
        return {"metadata": {}, "transcripts": {}}
    if not isinstance(cache.get("metadata"), dict):
        cache["metadata"] = {}
    if not isinstance(cache.get("transcripts"), dict):
        cache["transcripts"] = {}
    return cache


def save_podcast_cache(cache: Dict[str, Any]) -> None:
    cache_path = Path(PODCAST_CACHE_PATH)
    temp_path: Optional[Path] = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=str(cache_path.parent),
            prefix="follow-news-podcast-cache-",
            suffix=".json",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(cache, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_path, cache_path)
    except OSError as exc:
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        logging.warning("Failed to write podcast cache: %s", exc)


def fetch_rss_source(
    source: Dict[str, Any],
    cutoff: datetime,
    cache: Dict[str, Any],
    no_cache: bool,
) -> List[Dict[str, Any]]:
    request = Request(
        source["url"],
        headers={"User-Agent": "FollowNews/2.0"},
    )
    with urlopen(request, timeout=TIMEOUT) as response:
        content = response.read().decode("utf-8", errors="replace")

    episodes = parse_rss_episodes(content, source, cutoff)
    return [
        enrich_episode_transcript(episode, source, cache, no_cache=no_cache)
        for episode in episodes
    ]


def run_ytdlp_metadata(
    ytdlp_bin: str,
    source: Dict[str, Any],
    timeout: int = 90,
) -> Dict[str, Any]:
    import subprocess

    cmd = [
        ytdlp_bin,
        "--dump-single-json",
        "--flat-playlist",
        "--playlist-items",
        YOUTUBE_PLAYLIST_ITEM_SPEC,
        source["url"],
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("yt-dlp metadata command timed out") from exc
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "yt-dlp metadata command failed").strip()
        raise RuntimeError(message[:300])

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("yt-dlp metadata output was not valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("yt-dlp metadata output was not an object")
    return payload


def run_ytdlp_video_metadata(
    ytdlp_bin: str,
    url: str,
    timeout: int = 90,
) -> Dict[str, Any]:
    import subprocess

    cmd = [
        ytdlp_bin,
        "--dump-single-json",
        "--skip-download",
        "--no-playlist",
        url,
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("yt-dlp video metadata command timed out") from exc
    except OSError as exc:
        raise RuntimeError(str(exc)) from exc

    if result.returncode != 0:
        message = (result.stderr or result.stdout or "yt-dlp video metadata command failed").strip()
        raise RuntimeError(message[:300])

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("yt-dlp video metadata output was not valid JSON") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("yt-dlp video metadata output was not an object")
    return payload


def hydrate_youtube_metadata(
    payload: Dict[str, Any],
    ytdlp_bin: str,
) -> Dict[str, Any]:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    raw_entries = payload.get("entries") if isinstance(payload, dict) else None
    if not isinstance(raw_entries, list):
        return payload

    hydrated_entries: List[Dict[str, Any]] = []
    hydrate_jobs: Dict[int, str] = {}
    for entry in raw_entries[:MAX_EPISODES_PER_SOURCE * 2]:
        if not isinstance(entry, dict):
            continue
        hydrated_entries.append(entry)
        if youtube_entry_has_precise_published_at(entry):
            continue

        link = youtube_entry_link(entry)
        if not link:
            continue
        hydrate_jobs[len(hydrated_entries) - 1] = link

    if not hydrate_jobs:
        return {**payload, "entries": hydrated_entries}

    max_workers = min(YOUTUBE_METADATA_WORKERS, len(hydrate_jobs))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(run_ytdlp_video_metadata, ytdlp_bin, link): (index, link)
            for index, link in hydrate_jobs.items()
        }
        for future in as_completed(futures):
            index, link = futures[future]
            try:
                video_metadata = future.result()
            except RuntimeError as exc:
                logging.warning("Failed to hydrate YouTube podcast metadata for %s: %s", link, exc)
                continue
            hydrated_entries[index] = {**hydrated_entries[index], **video_metadata}

    return {**payload, "entries": hydrated_entries}


def fetch_youtube_source(
    source: Dict[str, Any],
    cutoff: datetime,
    cache: Dict[str, Any],
    no_cache: bool,
) -> List[Dict[str, Any]]:
    ytdlp_bin = resolve_ytdlp_bin()
    if not ytdlp_bin:
        raise RuntimeError("yt-dlp is not available")

    cache_key = metadata_cache_key(source)
    now = time.time()
    payload = None if no_cache else cached_metadata_payload(cache, cache_key, now, dict)
    if payload is None:
        payload = run_ytdlp_metadata(ytdlp_bin, source)
        payload = hydrate_youtube_metadata(payload, ytdlp_bin)
        if not no_cache:
            cache.setdefault("metadata", {})[cache_key] = {
                "payload": payload,
                "ts": now,
            }
    episodes = normalize_youtube_metadata(payload, source, cutoff)
    return [
        enrich_episode_transcript(episode, source, cache, no_cache=no_cache)
        for episode in episodes
    ]


def fetch_xiaoyuzhou_source(
    source: Dict[str, Any],
    cutoff: datetime,
    cache: Dict[str, Any],
    no_cache: bool,
) -> List[Dict[str, Any]]:
    podcast_id = extract_xiaoyuzhou_podcast_id(source.get("url", ""))
    if not podcast_id:
        raise RuntimeError("Xiaoyuzhou podcast URL must use the /podcast/{id} path")

    opencli_bin = resolve_opencli_bin()
    if not opencli_bin:
        raise RuntimeError("opencli is not available")

    cache_key = metadata_cache_key(source)
    now = time.time()
    payload = None if no_cache else cached_metadata_payload(cache, cache_key, now, list)
    if payload is None:
        payload = run_opencli_json(
            opencli_bin,
            [
                "xiaoyuzhou",
                "podcast-episodes",
                podcast_id,
                "--limit",
                str(MAX_EPISODES_PER_SOURCE),
                "-f",
                "json",
            ],
        )
        if not no_cache:
            cache.setdefault("metadata", {})[cache_key] = {
                "payload": payload,
                "ts": now,
            }
    episodes = normalize_xiaoyuzhou_metadata(payload, source, cutoff)
    return [
        enrich_episode_transcript(episode, source, cache, no_cache=no_cache)
        for episode in episodes
    ]


def fetch_source(
    source: Dict[str, Any],
    cutoff: datetime,
    cache: Dict[str, Any],
    no_cache: bool = False,
) -> Dict[str, Any]:
    platform = source.get("platform")
    if not platform or platform == "auto":
        platform = infer_platform(source.get("url", ""))

    result = {
        "source_id": source.get("id", ""),
        "source_type": "podcast",
        "name": source.get("name", ""),
        "url": source.get("url", ""),
        "priority": bool(source.get("priority", False)),
        "topics": list(source.get("topics", [])),
        "platform": platform,
        "status": "ok",
        "attempts": 1,
        "count": 0,
        "articles": [],
    }

    try:
        if platform == "youtube":
            articles = fetch_youtube_source(source, cutoff, cache, no_cache)
        elif platform == "xiaoyuzhou":
            articles = fetch_xiaoyuzhou_source(source, cutoff, cache, no_cache)
        elif platform == "rss":
            articles = fetch_rss_source(source, cutoff, cache, no_cache)
        else:
            raise RuntimeError(f"Unsupported podcast platform: {platform}")
    except Exception as exc:
        result["status"] = "error"
        result["error"] = str(exc)[:300]
        return result

    result["articles"] = articles
    result["count"] = len(articles)
    return result


def run_fetch(
    sources: List[Dict[str, Any]],
    hours: int,
    output: Path,
    cache: Dict[str, Any],
    no_cache: bool = False,
    request_params: Optional[Dict[str, Any]] = None,
) -> int:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    source_results = [
        fetch_source(source, cutoff, cache, no_cache=no_cache)
        for source in sources
    ]
    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_type": "podcast",
        "total_sources": len(source_results),
        "total_articles": sum(int(result.get("count", 0)) for result in source_results),
        "sources": source_results,
    }
    if request_params is not None:
        payload["input_params"] = request_params

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


def directory_json_fingerprint(directory: Optional[Path]) -> Optional[str]:
    if directory is None or not directory.exists() or not directory.is_dir():
        return None

    digest = hashlib.sha256()
    files = sorted(path for path in directory.iterdir() if path.is_file() and path.suffix == ".json")
    for path in files:
        data = path.read_bytes()
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(len(data)).encode("ascii"))
        digest.update(b"\0")
        digest.update(data)
    return digest.hexdigest()


def output_request_params(
    defaults_dir: Path,
    config_dir: Optional[Path],
    hours: int,
    no_cache: bool = False,
) -> Dict[str, Any]:
    return {
        "defaults": str(defaults_dir.resolve()),
        "defaults_fingerprint": directory_json_fingerprint(defaults_dir),
        "config": str(config_dir.resolve()) if config_dir else None,
        "config_fingerprint": directory_json_fingerprint(config_dir),
        "hours": hours,
        "no_cache": no_cache,
    }


def output_cache_is_fresh(
    output: Path,
    expected_params: Optional[Dict[str, Any]] = None,
    max_age_seconds: int = 3600,
) -> bool:
    if not output.exists():
        return False
    try:
        payload = json.loads(output.read_text(encoding="utf-8"))
        age = time.time() - output.stat().st_mtime
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict):
        return False
    if payload.get("source_type") != "podcast":
        return False
    if not isinstance(payload.get("sources"), list):
        return False
    if expected_params is not None and payload.get("input_params") != expected_params:
        return False
    return age < max_age_seconds


def create_default_output_path() -> Path:
    fd, path = tempfile.mkstemp(prefix="follow-news-podcast-", suffix=".json")
    os.close(fd)
    return Path(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch podcast episode metadata")
    parser.add_argument("--defaults", type=Path, default=Path("config/defaults"))
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--hours", type=int, default=24)
    parser.add_argument("--output", "-o", type=Path, default=None)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    setup_logging(args.verbose)

    output = args.output or create_default_output_path()
    request_params = output_request_params(args.defaults, args.config, args.hours, args.no_cache)
    if not args.force and output_cache_is_fresh(output, request_params):
        logging.info("Using fresh podcast output: %s", output)
        return 0

    sources = load_podcast_sources(args.defaults, args.config)
    cache = load_podcast_cache(no_cache=args.no_cache)
    result = run_fetch(
        sources,
        args.hours,
        output,
        cache,
        no_cache=args.no_cache,
        request_params=request_params,
    )
    if not args.no_cache:
        save_podcast_cache(cache)
    logging.info("Wrote podcast output: %s", output)
    return result


if __name__ == "__main__":
    sys.exit(main())
