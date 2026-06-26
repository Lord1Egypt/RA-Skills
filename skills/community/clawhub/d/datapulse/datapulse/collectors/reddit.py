"""Reddit parser using native `.json` API (no auth)."""

from __future__ import annotations

import json
import logging
import math
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

from datapulse.core.config import read_env_bool, read_env_int
from datapulse.core.models import SourceType
from datapulse.core.utils import clean_text, generate_excerpt

from .base import BaseCollector, ParseResult

logger = logging.getLogger("datapulse.parsers.reddit")


class RedditCollector(BaseCollector):
    name = "reddit"
    source_type = SourceType.REDDIT
    reliability = 0.9
    tier = 1
    setup_hint = ""
    max_comments = 15
    max_reply_depth = 3
    reddit_max_comments_env = "DATAPULSE_REDDIT_MAX_COMMENTS"
    reddit_max_reply_depth_env = "DATAPULSE_REDDIT_MAX_REPLY_DEPTH"
    reddit_extract_comment_links_env = "DATAPULSE_REDDIT_EXTRACT_COMMENT_LINKS"
    reddit_max_comment_links_env = "DATAPULSE_REDDIT_MAX_COMMENT_LINKS"

    def check(self) -> dict[str, str | bool]:
        return {"status": "ok", "message": "public JSON API (no auth)", "available": True}

    reddit_user_agent = "DataPulse/0.1 (+https://github.com/sunyifei83/DataPulse)"

    def can_handle(self, url: str) -> bool:
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        return hostname in {
            "reddit.com",
            "www.reddit.com",
            "old.reddit.com",
            "new.reddit.com",
            "np.reddit.com",
            "m.reddit.com",
        } and "/comments/" in parsed.path

    def parse(self, url: str) -> ParseResult:
        json_url = self._build_json_url(url)
        if not json_url:
            return ParseResult.failure(url, "Invalid Reddit post URL.")

        payload = None
        for attempt in range(2):
            try:
                req = urllib.request.Request(
                    json_url,
                    headers={"User-Agent": self.reddit_user_agent, "Accept": "application/json"},
                )
                with urllib.request.urlopen(req, timeout=20) as resp:
                    payload = json.loads(resp.read().decode())
                break
            except urllib.error.HTTPError as exc:
                if exc.code == 429 and attempt == 0:
                    time.sleep(1.5)
                    continue
                return ParseResult.failure(url, f"HTTP {exc.code}: {exc.reason}")
            except Exception as exc:
                if attempt == 0:
                    time.sleep(1)
                    continue
                return ParseResult.failure(url, str(exc))

        if not isinstance(payload, list) or len(payload) < 1:
            return ParseResult.failure(url, "Unexpected Reddit JSON payload.")

        try:
            post = payload[0]["data"]["children"][0]["data"]
            comments_tree = payload[1] if len(payload) > 1 else {}
        except Exception:
            return ParseResult.failure(url, "Unable to parse Reddit JSON structure.")

        title = post.get("title", "Untitled")
        author = post.get("author", "[deleted]")
        subreddit = post.get("subreddit_name_prefixed", "r/unknown")
        score = post.get("score", 0)
        created_utc = post.get("created_utc", 0)
        num_comments = post.get("num_comments", 0)
        upvote_ratio = post.get("upvote_ratio")
        subreddit_name = post.get("subreddit", "")
        selftext = post.get("selftext", "")
        link = post.get("url", "")
        is_self = post.get("is_self", True)
        flair = post.get("link_flair_text", "")
        max_comments = read_env_int(self.reddit_max_comments_env, self.max_comments, min_value=1, max_value=100)
        max_reply_depth = read_env_int(self.reddit_max_reply_depth_env, self.max_reply_depth, min_value=0, max_value=8)
        extract_comment_links = read_env_bool(self.reddit_extract_comment_links_env, True)
        max_comment_links = read_env_int(self.reddit_max_comment_links_env, 80, min_value=1, max_value=500)

        ts = ""
        if created_utc:
            ts = datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

        parts = [
            f"# {title}",
            f"**{subreddit}** · u/{author} · {ts}",
            f"\n⬆️ {score:,} · 💬 {num_comments:,}",
        ]
        if flair:
            parts.append(f"🏷️ {flair}")

        if selftext:
            parts.append("\n---\n" + selftext)
        elif link and not is_self:
            parts.append(f"\n🔗 {link}")

        comments = self._extract_comments(comments_tree, max_comments=max_comments, max_reply_depth=max_reply_depth)
        comment_links: list[str] = []
        github_repos: list[str] = []
        comment_link_extraction_degraded = False
        if extract_comment_links:
            try:
                comment_links, github_repos = self._extract_comment_links(
                    comments_tree,
                    max_comments=max_comments,
                    max_reply_depth=max_reply_depth,
                    max_links=max_comment_links,
                )
            except Exception:  # pragma: no cover - defensive fail-closed
                comment_link_extraction_degraded = True

        if comments:
            parts.append("\n---\n## Top Comments")
            parts.extend(comments)

        content = clean_text("\n".join(parts))
        tags = ["reddit", subreddit.lower()]
        if flair:
            tags.append((flair or "flair").lower().replace(" ", "-"))
        if not is_self:
            tags.append("link-post")

        confidence_flags = ["native-json", "comments"]
        if upvote_ratio is not None:
            confidence_flags.append("engagement_metrics")
        if score >= 100 or num_comments >= 50:
            confidence_flags.append("high_engagement")
        elif score <= 2 and num_comments <= 8:
            confidence_flags.append("low_engagement")
        community_signal = self._community_signal(
            score=score,
            num_comments=num_comments,
            upvote_ratio=upvote_ratio,
        )

        return ParseResult(
            url=url,
            title=f"[{subreddit}] {title}",
            content=content,
            author=f"u/{author}",
            excerpt=generate_excerpt(content),
            tags=tags,
            source_type=self.source_type,
            confidence_flags=confidence_flags,
            extra={
                "score": score,
                "num_comments": num_comments,
                "created_utc": created_utc,
                "flair": flair,
                "subreddit": subreddit_name,
                "subreddit_name_prefixed": subreddit,
                "upvote_ratio": upvote_ratio,
                "community_signal": community_signal,
                "comments_captured": len(comments),
                "comments_available": num_comments,
                "comments_truncated": bool(num_comments and len(comments) < num_comments),
                "max_comments": max_comments,
                "max_reply_depth": max_reply_depth,
                "comment_links": comment_links,
                "comment_link_count": len(comment_links),
                "github_repos": github_repos,
                "github_repo_count": len(github_repos),
                "comment_link_extraction_degraded": comment_link_extraction_degraded,
            },
        )

    def _build_json_url(self, url: str) -> str:
        normalized = url.rstrip("/")
        if not normalized:
            return ""
        if normalized.endswith(".json"):
            return normalized
        return f"{normalized}/.json"

    def _extract_comments(self, comment_listing: dict, *, max_comments: int, max_reply_depth: int) -> list[str]:
        children = []
        try:
            children = comment_listing.get("data", {}).get("children", [])
        except Exception:
            return []

        filtered = [c for c in children if c.get("kind") == "t1"]
        filtered.sort(key=lambda c: c.get("data", {}).get("score", 0), reverse=True)
        formatted: list[str] = []

        for entry in filtered[:max_comments]:
            data = entry.get("data", {})
            body = clean_text(data.get("body", "")).replace("\n", "\n> ")
            if not body or body in {"[deleted]", "[removed]"}:
                continue
            author = data.get("author", "[deleted]")
            score = data.get("score", 0)
            formatted.append(f"\n### u/{author} (⬆️ {score:,})\n> {body}")
            replies = data.get("replies")
            if isinstance(replies, dict):
                nested = self._extract_nested(
                    replies.get("data", {}).get("children", []),
                    depth=1,
                    max_reply_depth=max_reply_depth,
                )
                if nested:
                    formatted.append("\n" + "\n".join(nested))

        return formatted

    def _extract_nested(self, nodes: list[dict], depth: int, *, max_reply_depth: int) -> list[str]:
        if depth > max_reply_depth or not nodes:
            return []
        out: list[str] = []
        for item in nodes[:3]:
            if item.get("kind") != "t1":
                continue
            data = item.get("data", {})
            body = clean_text(data.get("body", "")).replace("\n", "\n> ")
            if not body:
                continue
            author = data.get("author", "[deleted]")
            out.append(f"> u/{author}: {body}")
            child = data.get("replies")
            if isinstance(child, dict):
                out.extend(
                    self._extract_nested(
                        child.get("data", {}).get("children", []),
                        depth + 1,
                        max_reply_depth=max_reply_depth,
                    )
                )
        return out

    _url_pattern = re.compile(r"https?://[^\s)\]}>\"']+", re.IGNORECASE)

    @classmethod
    def _extract_urls(cls, text: str) -> list[str]:
        if not text:
            return []
        urls: list[str] = []
        for raw in cls._url_pattern.findall(text):
            candidate = raw.strip().rstrip(".,;:!?")
            if candidate:
                urls.append(candidate)
        return urls

    @staticmethod
    def _github_repo_from_url(url: str) -> str:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host not in {"github.com", "www.github.com"}:
            return ""
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2:
            return ""
        owner = parts[0].strip()
        repo = parts[1].strip()
        if not owner or not repo:
            return ""
        if repo.endswith(".git"):
            repo = repo[:-4]
        if not repo:
            return ""
        return f"{owner.lower()}/{repo.lower()}"

    def _extract_comment_links(
        self,
        comment_listing: dict,
        *,
        max_comments: int,
        max_reply_depth: int,
        max_links: int,
    ) -> tuple[list[str], list[str]]:
        children = comment_listing.get("data", {}).get("children", [])
        if not isinstance(children, list):
            return [], []

        filtered = [c for c in children if c.get("kind") == "t1"]
        filtered.sort(key=lambda c: c.get("data", {}).get("score", 0), reverse=True)

        links: list[str] = []
        github_repos: list[str] = []
        seen_links: set[str] = set()
        seen_repos: set[str] = set()

        def _consume_from_data(data: dict) -> None:
            body = str(data.get("body", "") or "")
            for link in self._extract_urls(body):
                if len(links) >= max_links:
                    return
                if link in seen_links:
                    continue
                seen_links.add(link)
                links.append(link)
                repo = self._github_repo_from_url(link)
                if repo and repo not in seen_repos:
                    seen_repos.add(repo)
                    github_repos.append(repo)

        def _walk(nodes: list[dict], depth: int) -> None:
            if not nodes or depth > max_reply_depth or len(links) >= max_links:
                return
            for node in nodes[:3]:
                if len(links) >= max_links:
                    return
                if node.get("kind") != "t1":
                    continue
                data = node.get("data", {})
                if not isinstance(data, dict):
                    continue
                _consume_from_data(data)
                replies = data.get("replies")
                if isinstance(replies, dict):
                    child_nodes = replies.get("data", {}).get("children", [])
                    if isinstance(child_nodes, list):
                        _walk(child_nodes, depth + 1)

        for entry in filtered[:max_comments]:
            if len(links) >= max_links:
                break
            data = entry.get("data", {})
            if not isinstance(data, dict):
                continue
            _consume_from_data(data)
            replies = data.get("replies")
            if isinstance(replies, dict):
                child_nodes = replies.get("data", {}).get("children", [])
                if isinstance(child_nodes, list):
                    _walk(child_nodes, 1)

        return links, github_repos

    @staticmethod
    def _community_signal(*, score: int, num_comments: int, upvote_ratio: float | None) -> float:
        score_norm = min(math.log1p(max(0, int(score))) / math.log1p(1000), 1.0)
        comments_norm = min(math.log1p(max(0, int(num_comments))) / math.log1p(500), 1.0)
        ratio_norm = 0.5 if upvote_ratio is None else min(max(float(upvote_ratio), 0.0), 1.0)
        return round((score_norm * 0.45) + (comments_norm * 0.35) + (ratio_norm * 0.20), 4)
