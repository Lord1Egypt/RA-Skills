"""Twitter/X collector with FxTwitter primary and Nitter fallback."""

from __future__ import annotations

import json
import logging
import os
import random
import re
import time
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from datapulse.core.config import read_env_bool, read_env_int
from datapulse.core.jina_client import JinaAPIClient, JinaBlockedByPolicyError, JinaReadOptions
from datapulse.core.models import MediaType, SourceType
from datapulse.core.security import get_secret
from datapulse.core.utils import clean_text, generate_excerpt

from .base import BaseCollector, ParseResult

logger = logging.getLogger("datapulse.parsers.twitter")


_DEFAULT_NITTER = [
    "https://nitter.privacydev.net",
    "https://nitter.poast.org",
    "https://nitter.woodland.cafe",
    "https://nitter.1d4.us",
    "https://nitter.kavin.rocks",
]
_nitter_env = os.getenv("NITTER_INSTANCES")
NITTER_INSTANCES = _nitter_env.split(",") if _nitter_env else _DEFAULT_NITTER


class TwitterCollector(BaseCollector):
    name = "twitter"
    source_type = SourceType.TWITTER
    reliability = 0.92
    tier = 1
    setup_hint = "Ensure network can reach api.fxtwitter.com"

    max_nitter_retries = 3
    max_nitter_response_bytes = 3_000_000
    twitter_media_extract_env = "DATAPULSE_TWITTER_MEDIA_EXTRACT"
    twitter_media_timeout_env = "DATAPULSE_TWITTER_MEDIA_TIMEOUT"
    twitter_media_max_items_env = "DATAPULSE_TWITTER_MEDIA_MAX_ITEMS"

    def check(self) -> dict[str, str | bool]:
        try:
            req = urllib.request.Request("https://api.fxtwitter.com/", method="HEAD",
                                         headers={"User-Agent": "Mozilla/5.0"})
            urllib.request.urlopen(req, timeout=5)
            return {"status": "ok", "message": "FxTwitter API reachable", "available": True}
        except Exception as exc:
            return {"status": "warn", "message": f"FxTwitter unreachable: {exc}", "available": False}
    _nitter_allowed_content_types = ("text/html", "application/xhtml+xml")
    _profile_reserved_paths = {"home", "explore", "search", "messages", "notifications", "settings", "i"}

    def can_handle(self, url: str) -> bool:
        parsed = urlparse(url)
        return (parsed.hostname or "").replace("www.", "") in {"x.com", "twitter.com", "mobile.twitter.com", "mobile.x.com"}

    def parse(self, url: str) -> ParseResult:
        tweet_info = self._extract_tweet_info(url)
        if tweet_info:
            username, tweet_id = tweet_info
            result = self._parse_fxtwitter(url, username, tweet_id)
            if result.success:
                return result

            logger.warning("FxTwitter failed for %s, fallback to nitter: %s", url, result.error)
            path = f"{username}/status/{tweet_id}"
            nitter_result = self._parse_nitter_fallback(url, path)
            if nitter_result.success:
                return nitter_result

            return ParseResult.failure(
                url,
                f"FxTwitter error: {result.error}; Nitter error: {nitter_result.error}",
            )

        # profile URL
        profile = self._extract_profile_username(url)
        if profile:
            result = self._parse_profile(url, profile)
            return result

        return ParseResult.failure(
            url,
            "Twitter/X URL format not recognized. Expected status URL or public profile.",
        )

    def _parse_fxtwitter(self, original_url: str, username: str, tweet_id: str) -> ParseResult:
        api_base = os.getenv("FXTWITTER_API_URL", "https://api.fxtwitter.com").rstrip("/")
        api_url = f"{api_base}/{username}/status/{tweet_id}"

        last_error = ""
        for _ in range(2):
            try:
                req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as resp:
                    data = json.loads(resp.read().decode())
                if data.get("code") != 200:
                    return ParseResult.failure(original_url, f"FxTwitter code {data.get('code')}: {data.get('message', 'unknown')}")

                tweet = data.get("tweet") or {}
                screen_name = data.get("user", {}).get("screen_name", username)
                _display_name = data.get("user", {}).get("name", username)  # noqa: F841
                created_at = tweet.get("created_at", "")
                stats = tweet.get("stats") or {}

                likes = self._to_nonnegative_int(stats.get("likes", 0))
                retweets = self._to_nonnegative_int(stats.get("retweets", 0))
                views = self._to_nonnegative_int(stats.get("views", 0))
                has_engagement = any(metric > 0 for metric in (likes, retweets, views))
                quotes = []

                if tweet.get("is_article"):
                    blocks = tweet.get("article", {}).get("content", {}).get("blocks", [])
                    article_title = tweet.get("article", {}).get("title", "")
                    title = f"📝 {article_title}" if article_title else f"X Article by @{screen_name}"
                    body = "\n\n".join(b.get("text", "") for b in blocks)
                else:
                    title = f"Tweet by @{screen_name}"
                    if created_at:
                        title += f" ({created_at})"
                    body = tweet.get("text", "")

                if not body:
                    body = (
                        str(tweet.get("description", "") or "").strip()
                        or str((tweet.get("note_tweet") or {}).get("text", "")).strip()
                        or str(((tweet.get("legacy") or {}).get("full_text", ""))).strip()
                        or str(data.get("text", "")).strip()
                        or str(data.get("tweetText", "")).strip()
                    )

                if tweet.get("note_tweet"):
                    body += "\n\n[Note Tweet]"
                    quotes.append("note")

                quote = tweet.get("quote")
                if quote:
                    quotes.append("quote")
                    body += f"\n\n[Quoted Tweet] {quote.get('text', '')}"

                media = tweet.get("media", {})
                media_items = media.get("all", []) or []
                media_extraction = self._build_media_extraction(media_items)
                if media_items:
                    body += "\n\n## Media\n"
                    for index, item in enumerate(media_items, 1):
                        media_type = item.get("type", "unknown")
                        media_url = item.get("url", "")
                        if media_type == "photo":
                            body += f"{index}. {media_url}\n"
                        elif media_url:
                            body += f"{index}. {media_type}: {media_url}\n"
                if media_extraction.get("items"):
                    body += "\n## Media Extracted Signals (Unverified)\n"
                    for extracted in media_extraction["items"]:
                        hint = str(extracted.get("method", "unknown"))
                        index = int(extracted.get("index", 0))
                        text = str(extracted.get("text", "")).strip()
                        if not text:
                            continue
                        body += f"- [{hint} #{index}] {text}\n"

                content = clean_text(f"{body}  \n\n👍 {likes}  🔁 {retweets}  👁️ {views}")
                excerpt = generate_excerpt(content)
                confidence_flags = ["fxtwitter"]
                if has_engagement:
                    confidence_flags.append("engagement")
                else:
                    confidence_flags.append("engagement_unavailable")
                if media_extraction.get("status") == "degraded":
                    confidence_flags.append("media_extraction_degraded")
                if media_extraction.get("items"):
                    confidence_flags.append("media_extraction_available")

                return ParseResult(
                    url=original_url,
                    title=title[:180],
                    content=content,
                    author=f"@{screen_name}",
                    excerpt=excerpt,
                    tags=["twitter", "x"],
                    source_type=self.source_type,
                    media_type=(MediaType.IMAGE.value if media_items else MediaType.TEXT.value),
                    confidence_flags=confidence_flags,
                    extra={
                        "tweet_id": tweet_id,
                        "screen_name": screen_name,
                        "likes": likes,
                        "retweets": retweets,
                        "views": views,
                        "engagement_available": has_engagement,
                        "is_article": bool(tweet.get("is_article")),
                        "features": quotes,
                        "media_urls": [str(item.get("url", "")).strip() for item in media_items if str(item.get("url", "")).strip()],
                        "media_extraction": media_extraction,
                    },
                )
            except urllib.error.HTTPError as exc:
                last_error = f"HTTP {exc.code}: {exc.reason}"
                return ParseResult.failure(original_url, last_error)
            except urllib.error.URLError as exc:
                last_error = f"Network error: {exc}"
                time.sleep(1)
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
                break
        return ParseResult.failure(original_url, last_error or "FxTwitter request failed")

    def _build_media_extraction(self, media_items: list[dict[str, Any]]) -> dict[str, Any]:
        if not media_items:
            return {
                "status": "not_applicable",
                "items": [],
                "method": "none",
                "confidence": 0.0,
                "attempted": 0,
                "failed": 0,
                "error_code": "",
                "error_hint": "",
            }

        enable_generated_alt = read_env_bool(self.twitter_media_extract_env, False)
        max_items = read_env_int(self.twitter_media_max_items_env, 4, min_value=1, max_value=12)
        timeout = read_env_int(self.twitter_media_timeout_env, 20, min_value=5, max_value=90)
        has_jina_api_key = bool(get_secret("JINA_API_KEY").strip()) if enable_generated_alt else False

        items: list[dict[str, Any]] = []
        methods_used: set[str] = set()
        attempted = 0
        failed = 0
        error_code = ""
        error_hint = ""

        for index, media in enumerate(media_items[:max_items], 1):
            media_url = str(media.get("url", "")).strip()
            media_type = str(media.get("type", "unknown")).strip().lower() or "unknown"
            if not media_url:
                continue

            text = self._extract_media_text_from_metadata(media)
            method = "fxtwitter_metadata"
            confidence = 0.78

            if not text and enable_generated_alt and media_type in {"photo", "image"}:
                if not has_jina_api_key:
                    if not error_code:
                        error_code = "auth_missing"
                        error_hint = "JINA_API_KEY is required when DATAPULSE_TWITTER_MEDIA_EXTRACT=1"
                    continue
                attempted += 1
                try:
                    text = self._extract_media_text_via_jina(media_url, timeout=timeout)
                    if text:
                        method = "jina_generated_alt"
                        confidence = 0.55
                except Exception as exc:  # noqa: BLE001
                    failed += 1
                    if not error_code:
                        error_code, error_hint = self._classify_media_extraction_error(exc)
                    logger.info("Twitter media extraction degraded for %s: %s", media_url, exc)

            if not text:
                continue

            methods_used.add(method)
            items.append({
                "index": index,
                "type": media_type,
                "url": media_url,
                "text": text,
                "method": method,
                "confidence": round(confidence, 2),
            })

        if error_code or failed > 0:
            status = "degraded"
        elif items:
            status = "ok"
        else:
            status = "skipped"

        if methods_used:
            method = "+".join(sorted(methods_used))
        elif enable_generated_alt:
            method = "jina_generated_alt"
        else:
            method = "fxtwitter_metadata_only"

        avg_confidence = 0.0
        if items:
            avg_confidence = round(sum(float(item["confidence"]) for item in items) / len(items), 2)

        return {
            "status": status,
            "items": items,
            "method": method,
            "confidence": avg_confidence,
            "attempted": attempted,
            "failed": failed,
            "error_code": error_code,
            "error_hint": error_hint,
        }

    def _extract_media_text_via_jina(self, media_url: str, *, timeout: int) -> str:
        client = JinaAPIClient(timeout=timeout)
        result = client.read(
            media_url,
            options=JinaReadOptions(
                response_format="markdown",
                no_cache=True,
                with_generated_alt=True,
            ),
        )
        return self._normalize_generated_alt_text(result.content)

    @staticmethod
    def _classify_media_extraction_error(exc: Exception) -> tuple[str, str]:
        hint = clean_text(str(exc) or exc.__class__.__name__).strip()[:300]
        if isinstance(exc, JinaBlockedByPolicyError):
            return "policy_blocked", hint or "Jina blocked by policy"

        if isinstance(exc, requests.Timeout):
            return "network_timeout", hint or "Request timed out"

        if isinstance(exc, requests.HTTPError):
            status_code = exc.response.status_code if exc.response is not None else 0
            if status_code in {401, 403}:
                return "auth_unauthorized", hint or f"HTTP {status_code}"
            if status_code == 451:
                return "policy_blocked", hint or "HTTP 451"
            if status_code == 429:
                return "rate_limited", hint or "HTTP 429"
            return "http_error", hint or f"HTTP {status_code}"

        if isinstance(exc, requests.RequestException):
            return "network_error", hint or exc.__class__.__name__

        return "unknown_error", hint or exc.__class__.__name__

    @staticmethod
    def _to_nonnegative_int(value: Any) -> int:
        try:
            parsed = int(float(str(value).strip()))
        except (TypeError, ValueError):
            return 0
        return max(0, parsed)

    @staticmethod
    def _extract_media_text_from_metadata(media_item: dict[str, Any]) -> str:
        candidate_keys = (
            "altText",
            "alt_text",
            "description",
            "caption",
            "text",
            "title",
            "ocr_text",
        )
        for key in candidate_keys:
            text = TwitterCollector._normalize_media_text(media_item.get(key))
            if text:
                return text

        nested_keys = ("metadata", "ocr", "ai")
        for key in nested_keys:
            payload = media_item.get(key)
            if not isinstance(payload, dict):
                continue
            for nested_key in ("text", "description", "caption", "alt", "alt_text", "summary"):
                text = TwitterCollector._normalize_media_text(payload.get(nested_key))
                if text:
                    return text
        return ""

    @staticmethod
    def _normalize_generated_alt_text(raw: str) -> str:
        cleaned_lines: list[str] = []
        for line in (raw or "").splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            lower = normalized.lower()
            if lower.startswith("title:") or lower.startswith("url source:") or lower.startswith("markdown content:"):
                continue
            if lower.startswith("http://") or lower.startswith("https://"):
                continue
            normalized = normalized.lstrip("#*- ").strip()
            if normalized:
                cleaned_lines.append(normalized)

        text = clean_text(" ".join(cleaned_lines)).strip()
        if len(text) < 16:
            return ""
        return text[:600]

    @staticmethod
    def _normalize_media_text(value: Any) -> str:
        if isinstance(value, str):
            text = clean_text(value).strip()
            if len(text) < 8:
                return ""
            return text[:600]

        if isinstance(value, list):
            for item in value:
                text = TwitterCollector._normalize_media_text(item)
                if text:
                    return text

        if isinstance(value, dict):
            for key in ("text", "description", "caption", "value"):
                text = TwitterCollector._normalize_media_text(value.get(key))
                if text:
                    return text

        return ""

    def _parse_profile(self, original_url: str, profile: str) -> ParseResult:
        api_url = f"https://api.fxtwitter.com/{profile}"
        try:
            req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode())
            if data.get("code") != 200:
                return ParseResult.failure(original_url, f"Profile API error: {data.get('message', '')}")

            user = data.get("user") or {}
            name = user.get("name", "")
            description = user.get("description", "")
            followers = user.get("followers", 0)
            following = user.get("following", 0)

            sections = [
                f"# X Profile: @{profile}",
                f"Name: {name}",
                f"Followers: {followers}  Following: {following}",
                "",
                f"Bio: {description}",
                f"Source: {user.get('url', original_url)}",
            ]
            content = "\n".join(sections)
            return ParseResult(
                url=original_url,
                title=f"X Profile: @{profile}",
                content=clean_text(content),
                author=f"@{profile}",
                source_type=self.source_type,
                tags=["twitter", "profile"],
                confidence_flags=["fxtwitter", "profile"],
                extra={"followers": followers, "following": following},
            )
        except Exception as exc:  # noqa: BLE001
            return ParseResult.failure(original_url, str(exc))

    def _parse_nitter_fallback(self, original_url: str, tweet_path: str) -> ParseResult:
        chosen = random.sample(list(NITTER_INSTANCES), min(self.max_nitter_retries, len(NITTER_INSTANCES)))
        last_error = ""
        for instance in chosen:
            url = f"{instance}/{tweet_path}"
            try:
                return self._parse_nitter_page(original_url, url)
            except Exception as exc:  # noqa: BLE001
                last_error = str(exc)
        return ParseResult.failure(original_url, last_error or "Nitter unavailable")

    def _parse_nitter_page(self, original_url: str, nitter_url: str) -> ParseResult:
        with requests.get(
            nitter_url,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "text/html"},
            timeout=20,
            stream=True,
        ) as resp:
            resp.raise_for_status()
            safe, reason = __import__("datapulse.core.utils", fromlist=["validate_external_url"]).validate_external_url(resp.url)
            if not safe:
                raise ValueError(f"Blocked redirect target: {reason}")

            content_type = (resp.headers.get("Content-Type") or "").lower()
            if content_type and not any(ct in content_type for ct in self._nitter_allowed_content_types):
                raise ValueError(f"Unsupported content type: {content_type}")

            body = bytearray()
            for chunk in resp.iter_content(chunk_size=8192):
                if not chunk:
                    continue
                body.extend(chunk)
                if len(body) > self.max_nitter_response_bytes:
                    raise ValueError("Nitter payload too large")

            html = body.decode(resp.encoding or resp.apparent_encoding or "utf-8", errors="replace")

        soup = BeautifulSoup(html, "lxml")
        tweet_div = soup.find("div", class_="tweet-content") or soup.find("div", class_="main-tweet")
        if not tweet_div:
            return ParseResult.failure(original_url, "Nitter parse: tweet body missing")

        text = clean_text(tweet_div.get_text("\n", strip=True))
        if not text:
            return ParseResult.failure(original_url, "Nitter parse: empty text")

        author_tag = soup.find("a", class_="fullname") or soup.find("span", class_="username")
        author = author_tag.get_text(strip=True) if author_tag else ""
        return ParseResult(
            url=original_url,
            title=f"Tweet by {author}" if author else "Tweet",
            content=text,
            author=author,
            excerpt=generate_excerpt(text),
            source_type=self.source_type,
            tags=["twitter", "nitter"],
            confidence_flags=["nitter-fallback"],
            extra={"nitter_url": nitter_url},
        )

    @staticmethod
    def _extract_tweet_info(url: str) -> tuple[str, str] | None:
        match = re.search(r"(?:x|twitter)\.com/([a-zA-Z0-9_]{1,15})/status/(\d+)", url)
        if not match:
            return None
        return match.group(1), match.group(2)

    def _extract_profile_username(self, url: str) -> str | None:
        parsed = urlparse(url)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) != 1:
            return None
        username = parts[0]
        if username in self._profile_reserved_paths:
            return None
        return username if re.fullmatch(r"[a-zA-Z0-9_]{1,15}", username) else None
