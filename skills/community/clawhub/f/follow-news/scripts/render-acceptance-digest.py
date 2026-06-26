#!/usr/bin/env python3
"""Render deterministic Markdown/Discord digest output for acceptance tests."""

import argparse
import json
import math
import re
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set
from urllib.parse import parse_qsl, parse_qs, urlencode, urlparse


MIN_QUALITY_SCORE = 5
MAX_GITHUB_TRENDING_ITEMS = 5
MAX_PODCAST_REMIX_ITEMS = 3
HN_DEFAULT_LIMIT = 10
HN_AI_RELATED_LIMIT = 20
HN_AI_KEYWORDS = (
    "ai",
    "artificial intelligence",
    "llm",
    "gpt",
    "claude",
    "gemini",
    "openai",
    "anthropic",
    "deepmind",
    "machine learning",
    "ml",
    "neural",
    "transformer",
    "agent",
    "embedding",
    "fine-tune",
    "finetune",
    "inference",
    "model",
)
TRACKING_QUERY_PARAMS = {
    "fbclid",
    "gclid",
    "igshid",
    "mc_cid",
    "mc_eid",
    "ref_src",
}


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_topic_definitions(path: Path) -> List[Dict[str, Any]]:
    data = load_json(path)
    return [topic for topic in data.get("topics", []) if isinstance(topic, dict)]


def article_link(article: Dict[str, Any]) -> str:
    return (
        article.get("link")
        or article.get("external_url")
        or article.get("reddit_url")
        or ""
    )


def normalize_visible_domain(domain: str) -> str:
    domain = domain.lower()
    if domain.startswith("www."):
        return domain[4:]
    return domain


def normalize_visible_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        domain = normalize_visible_domain(parsed.netloc)
        path = parsed.path.rstrip("/")
        if parsed.params:
            path = f"{path};{parsed.params}"

        if domain in {"youtube.com", "m.youtube.com"} and path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
            if video_id:
                return f"url:youtube:{video_id}"

        if domain == "youtu.be" and path:
            video_id = path.lstrip("/")
            if video_id:
                return f"url:youtube:{video_id}"

        if domain or path:
            query_pairs = [
                (name, value)
                for name, value in parse_qsl(parsed.query, keep_blank_values=True)
                if not name.lower().startswith("utm_")
                and name.lower() not in TRACKING_QUERY_PARAMS
            ]
            query = urlencode(sorted(query_pairs), doseq=True)
            suffix = f"?{query}" if query else ""
            return f"url:{domain}{path}{suffix}"
    except Exception:
        pass

    compact = " ".join(str(url).split())
    return f"url:{compact}" if compact else ""


def normalize_visible_title(title: Any) -> str:
    if not title:
        return ""

    value = str(title)
    value = re.sub(r"^(RT\s+@\w+:\s*)", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"(?<=\d)\.(?=\d)", " ", value)
    value = re.sub(r"[^\w\s]", "", value.lower())
    return value


def article_source_suffixes(article: Dict[str, Any]) -> List[str]:
    candidates = []
    for field in ("source_name", "show_name", "display_name"):
        value = compact_text(article.get(field))
        if value:
            candidates.append(value)
    return candidates


def strip_matching_source_suffix(title: Any, article: Dict[str, Any]) -> str:
    value = compact_text(title)
    for suffix in article_source_suffixes(article):
        for separator in (" | ", " - ", " – "):
            expected = f"{separator}{suffix}"
            if value.lower().endswith(expected.lower()):
                return value[: -len(expected)].strip()
    return value


def article_dedupe_key(article: Dict[str, Any]) -> Optional[str]:
    keys = article_dedupe_keys(article)
    return keys[0] if keys else None


def article_dedupe_keys(article: Dict[str, Any]) -> List[str]:
    keys = []
    url = article_link(article)
    if url:
        normalized_url = normalize_visible_url(url)
        if normalized_url:
            keys.append(normalized_url)

    hn_url = compact_text(article.get("hn_url") or article.get("comments_url"))
    if hn_url:
        normalized_hn_url = normalize_visible_url(hn_url)
        if normalized_hn_url:
            keys.append(normalized_hn_url)
            keys.append(f"hn:{normalized_hn_url}")

    title = strip_matching_source_suffix(article.get("title"), article)
    normalized_title = normalize_visible_title(title)
    if normalized_title:
        keys.append(f"title:{normalized_title}")

    return keys


class VisibleArticleRegistry:
    def __init__(self) -> None:
        self.seen_keys = set()
        self.parent: Dict[str, str] = {}

    def is_seen(self, article: Dict[str, Any]) -> bool:
        keys = article_dedupe_keys(article)
        if not keys:
            return False
        self.register_aliases([article])
        return bool(self._component_keys(keys) & self.seen_keys)

    def mark(self, article: Dict[str, Any]) -> None:
        keys = article_dedupe_keys(article)
        if not keys:
            return
        self.register_aliases([article])
        self.seen_keys.update(self._component_keys(keys))

    def filter_unseen(self, articles: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        candidates = [(article, article_dedupe_keys(article)) for article in articles]
        self.register_aliases(article for article, _ in candidates)
        visible = []
        for article, keys in candidates:
            if not keys:
                visible.append(article)
                continue

            component_keys = self._component_keys(keys)
            if component_keys & self.seen_keys:
                self.seen_keys.update(component_keys)
                continue

            self.seen_keys.update(component_keys)
            visible.append(article)
        return visible

    def filter_unseen_limited(
        self,
        articles: Iterable[Dict[str, Any]],
        limit: int,
    ) -> List[Dict[str, Any]]:
        candidates = [(article, article_dedupe_keys(article)) for article in articles]
        self.register_aliases(article for article, _ in candidates)
        visible = []
        for article, keys in candidates:
            if not keys:
                visible.append(article)
            else:
                component_keys = self._component_keys(keys)
                if component_keys & self.seen_keys:
                    self.seen_keys.update(component_keys)
                    continue

                self.seen_keys.update(component_keys)
                visible.append(article)

            if len(visible) >= limit:
                break
        return visible

    def register_aliases(self, articles: Iterable[Dict[str, Any]]) -> None:
        for article in articles:
            keys = article_dedupe_keys(article)
            if not keys:
                continue
            first = keys[0]
            self._find(first)
            for key in keys[1:]:
                self._union(first, key)

    def _find(self, key: str) -> str:
        self.parent.setdefault(key, key)
        root = key
        while self.parent[root] != root:
            root = self.parent[root]

        while self.parent[key] != key:
            parent = self.parent[key]
            self.parent[key] = root
            key = parent

        return root

    def _union(self, first: str, second: str) -> None:
        first_root = self._find(first)
        second_root = self._find(second)
        if first_root != second_root:
            self.parent[second_root] = first_root

    def _component_keys(self, keys: List[str]) -> Set[str]:
        roots = {self._find(key) for key in keys}
        return {key for key in self.parent if self._find(key) in roots}


def render_link(url: str) -> str:
    return f"  🔗 {url}"


def parse_quality_score(article: Dict[str, Any]) -> Optional[float]:
    value = article.get("quality_score", 0)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if not math.isfinite(number):
        return None
    return number


def quality_score(article: Dict[str, Any]) -> float:
    score = parse_quality_score(article)
    return score if score is not None else 0.0


def has_quality_score_value(article: Dict[str, Any]) -> bool:
    return "quality_score" in article and article.get("quality_score") not in (None, "")


def should_render_chat_topic_article(article: Dict[str, Any]) -> bool:
    if not article_link(article):
        return False

    score = parse_quality_score(article)
    if score is not None:
        return score >= MIN_QUALITY_SCORE

    return has_quality_score_value(article)


def format_count(value: Any) -> str:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = 0

    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M".replace(".0M", "M")
    if number >= 1_000:
        return f"{number / 1_000:.1f}K".replace(".0K", "K")
    return str(number)


def compact_text(value: Any) -> str:
    return " ".join(str(value).split()) if value else ""


def chat_summary(article: Dict[str, Any]) -> str:
    for field in (
        "chat_summary",
        "full_text",
        "summary",
        "snippet",
        "description",
        "transcript",
        "title",
    ):
        text = compact_text(article.get(field))
        if text:
            return text
    return "No summary material is available."


def bold_chat_title_text(value: Any) -> str:
    text = str(value)
    chars = []
    for char in text:
        code = ord(char)
        if ord("A") <= code <= ord("Z"):
            chars.append(chr(0x1D400 + code - ord("A")))
        elif ord("a") <= code <= ord("z"):
            chars.append(chr(0x1D41A + code - ord("a")))
        elif ord("0") <= code <= ord("9"):
            chars.append(chr(0x1D7CE + code - ord("0")))
        else:
            chars.append(char)
    return "".join(chars)


def chat_title_line(
    article: Dict[str, Any],
    index: int,
    emoji: str,
) -> str:
    title = article.get("title") or article.get("repo") or "Untitled"
    return f"{index}. {bold_chat_title_text(title)}"


def render_chat_item(
    article: Dict[str, Any],
    index: int,
    emoji: str,
) -> str:
    return "\n".join(
        [
            chat_title_line(article, index, emoji),
            "",
            chat_summary(article),
            "",
            f"🔗 {article_link(article)}",
        ]
    )


def iter_articles(data: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for topic in data.get("topics", {}).values():
        if not isinstance(topic, dict):
            continue
        for article in topic.get("articles", []):
            if isinstance(article, dict):
                yield article


def fixed_kol_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if article.get("source_type") == "twitter" and article_link(article)
    ]


def fixed_github_release_articles(
    data: Dict[str, Any],
    filter_low_signal: bool = False,
) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if article.get("source_type") == "github"
        and article_link(article)
        and (
            not filter_low_signal
            or not is_low_signal_github_release(article)
        )
    ]


def fixed_github_trending_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if article.get("source_type") == "github_trending" and article_link(article)
    ]


def fixed_blog_pick_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if article.get("is_blog_pick") and article_link(article)
    ]


def fixed_hacker_news_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if is_hacker_news_article(article)
        and has_hacker_news_metadata(article)
        and (hacker_news_url(article) or hacker_news_article_url(article))
    ]


def fixed_podcast_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        article
        for article in iter_articles(data)
        if article.get("source_type") == "podcast"
        and article_link(article)
    ]


def podcast_has_transcript(article: Dict[str, Any]) -> bool:
    return bool(
        article.get("transcript_status") == "ok"
        and compact_text(article.get("transcript"))
    )


def podcast_remix_sort_key(article: Dict[str, Any]) -> tuple:
    return (
        not podcast_has_transcript(article),
        -quality_score(article),
        compact_text(article.get("title")),
    )


def podcast_remix_candidates(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    episodes = fixed_podcast_articles(data)
    return sorted(episodes, key=podcast_remix_sort_key)


def podcast_remix_articles(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return podcast_remix_candidates(data)[:MAX_PODCAST_REMIX_ITEMS]


def chat_topic_articles(topic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    articles = [
        article
        for article in topic_data.get("articles", [])
        if isinstance(article, dict) and should_render_chat_topic_article(article)
    ]
    return sorted(articles, key=quality_score, reverse=True)


def visible_alias_candidates(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    template: str,
) -> List[Dict[str, Any]]:
    candidates = []
    topics = data.get("topics", {})

    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        topic_data = topics.get(topic_id)
        if not isinstance(topic_data, dict):
            continue

        candidates.extend(topic_render_candidate_articles(topic_id, topic_data, template))

    candidates.extend(fixed_kol_articles(data))
    candidates.extend(
        fixed_github_release_articles(
            data,
            filter_low_signal=(template == "chat"),
        )
    )
    if not has_renderable_hackernews_topic(data, topic_defs):
        candidates.extend(fixed_hacker_news_articles(data))
    candidates.extend(fixed_github_trending_articles(data))
    candidates.extend(fixed_blog_pick_articles(data))
    candidates.extend(podcast_remix_candidates(data))
    return candidates


def topic_render_candidate_articles(
    topic_id: Any,
    topic_data: Dict[str, Any],
    template: str,
) -> List[Dict[str, Any]]:
    if is_hackernews_topic(topic_id):
        return select_hackernews_topic_articles(topic_data.get("articles", []) or [])

    if template == "chat":
        articles = chat_topic_articles(topic_data)
    else:
        articles = sorted_topic_articles(topic_data)

    return [
        article
        for article in articles
        if not is_non_hackernews_topic_hn_article(topic_id, article)
    ]


def sorted_topic_articles(topic_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    articles = [
        article
        for article in topic_data.get("articles", [])
        if isinstance(article, dict)
        and quality_score(article) >= MIN_QUALITY_SCORE
        and article_link(article)
    ]
    return sorted(articles, key=quality_score, reverse=True)


def render_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    visible_registry: VisibleArticleRegistry,
) -> List[str]:
    sections = []
    topics = data.get("topics", {})

    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        topic_data = topics.get(topic_id)
        if not isinstance(topic_data, dict):
            continue

        articles = topic_render_candidate_articles(topic_id, topic_data, "discord")
        if is_hackernews_topic(topic_id):
            articles = visible_registry.filter_unseen_limited(
                articles,
                HN_DEFAULT_LIMIT,
            )
        else:
            articles = visible_registry.filter_unseen(articles)
        if not articles:
            continue

        lines = [
            f"## {topic_def.get('emoji', '')} {topic_def.get('label', topic_id)}".rstrip(),
            "",
        ]
        for article in articles:
            if is_hackernews_topic(topic_id) and is_hacker_news_article(article):
                lines.extend(render_hackernews_topic_item(article))
            else:
                lines.append(f"• {article.get('title', '?')}")
                lines.append(render_link(article_link(article)))
                if article.get("multi_source"):
                    lines.append(f"  *[{article.get('source_count', 2)} sources]*")
            lines.append("")
        sections.append("\n".join(lines).rstrip())

    return sections


def render_chat_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    visible_registry: VisibleArticleRegistry,
) -> List[str]:
    sections = []
    topics = data.get("topics", {})

    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        topic_data = topics.get(topic_id)
        if not isinstance(topic_data, dict):
            continue

        articles = topic_render_candidate_articles(topic_id, topic_data, "chat")
        if is_hackernews_topic(topic_id):
            articles = visible_registry.filter_unseen_limited(
                articles,
                HN_DEFAULT_LIMIT,
            )
        else:
            articles = visible_registry.filter_unseen(articles)
        if not articles:
            continue

        emoji = topic_def.get("emoji", "")
        lines = [
            f"## {emoji} {topic_def.get('label', topic_id)}".rstrip(),
            "",
        ]
        for index, article in enumerate(articles, 1):
            if is_hackernews_topic(topic_id) and is_hacker_news_article(article):
                lines.extend(render_chat_hackernews_topic_item(article, index, emoji))
            else:
                lines.append(render_chat_item(article, index, emoji))
            lines.append("")
        sections.append("\n".join(lines).rstrip())

    return sections


def render_kol_updates(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    tweets = fixed_kol_articles(data)
    if not tweets:
        return None

    tweets = sorted(tweets, key=quality_score, reverse=True)
    tweets = visible_registry.filter_unseen(tweets)
    if not tweets:
        return None

    lines = ["## 📢 KOL Updates", ""]
    for article in tweets:
        display_name = (
            article.get("display_name") or article.get("source_name") or "Unknown"
        )
        handle = article.get("handle") or article.get("source_id") or "unknown"
        summary = article.get("summary") or article.get("snippet") or article.get(
            "title", ""
        )
        lines.append(f"• **{display_name}** (@{handle}) — {summary}")
        lines.append(render_link(article_link(article)))
        lines.append("")

    return "\n".join(lines).rstrip()


def is_low_signal_github_release(article: Dict[str, Any]) -> bool:
    title = compact_text(article.get("title")).lower()
    tag = release_tag_text(article)
    summary = compact_text(article.get("summary") or article.get("snippet")).lower()
    dependency_text = " ".join([title, tag, summary])

    if article.get("prerelease") is True:
        return True

    low_signal_tokens = ("nightly", "snapshot", "canary", "alpha", "beta")
    if any(token in tag for token in low_signal_tokens):
        return True

    if re.search(
        r"(?:^|[._-])(?:a|b|rc|pre)[._-]?\d+$|[0-9](?:a|b|rc|pre)\d+$",
        tag,
    ):
        return True

    dependency_patterns = (
        r"\b(?:bump|update|upgrade|pin|vendor)\s+(?:deps?|dependencies|packages?)\b",
        r"\b(?:bump|update|upgrade|pin|vendor)\s+[a-z0-9_.@/-]+\s+(?:from|to)\b",
        r"\b(?:deps?|dependencies)\s+(?:bump|update|upgrade)\b",
        r"\bdependency\s+(?:bump|update|upgrade)\b",
        r"\bdependency\s+update\s*:",
        r"\b(?:update|upgrade)\s+dependencies\s*:",
        r"\b(?:update|upgrade)\s+dependency\s+[a-z0-9_.@/-]+\s+(?:from|to)\b",
        r"\b(?:update|upgrade)\s+dependency\s+[a-z0-9_.@/-]+\s+v?\d",
        r"\bdependabot\b",
    )
    signal_terms = (
        "api",
        "feature",
        "security",
        "performance",
        "stable",
        "support",
        "breaking",
        "fix",
    )
    has_dependency_update = any(
        re.search(pattern, dependency_text)
        for pattern in dependency_patterns
    )
    has_product_signal = any(
        re.search(rf"\b{re.escape(term)}\b", summary)
        for term in signal_terms
    )
    return has_dependency_update and not has_product_signal


def release_tag_text(article: Dict[str, Any]) -> str:
    explicit_tag = compact_text(article.get("tag_name") or article.get("version")).lower()
    if explicit_tag:
        return explicit_tag

    title = compact_text(article.get("title")).lower()
    matches = re.findall(
        r"\b(?:v?\d+(?:[._-]\d+)*(?:[._-]?(?:a|b|rc|pre)[._-]?\d+|[._-]?(?:alpha|beta)\d*)?|nightly|snapshot|canary)\b",
        title,
    )
    return " ".join(matches)


def is_hacker_news_article(article: Dict[str, Any]) -> bool:
    if compact_text(article.get("hn_url")):
        return True
    if article.get("source_id") == "hn-rss":
        return True
    if article.get("source_name") == "Hacker News Frontpage":
        return True
    all_sources = article.get("all_sources", [])
    return isinstance(all_sources, list) and "Hacker News Frontpage" in all_sources


def is_hackernews_topic(topic_id: Any) -> bool:
    return compact_text(topic_id).lower() == "hackernews"


def is_non_hackernews_topic_hn_article(
    topic_id: Any,
    article: Dict[str, Any],
) -> bool:
    return not is_hackernews_topic(topic_id) and is_hacker_news_section_article(article)


def is_direct_hacker_news_article(article: Dict[str, Any]) -> bool:
    return (
        article.get("source_id") == "hn-rss"
        or article.get("source_name") == "Hacker News Frontpage"
    )


def has_hacker_news_metadata(article: Dict[str, Any]) -> bool:
    return (
        hacker_news_score_value(article) is not None
        and hacker_news_comments_value(article) is not None
    )


def is_hacker_news_section_article(article: Dict[str, Any]) -> bool:
    return has_hacker_news_metadata(article) and (
        bool(hacker_news_url(article)) or is_direct_hacker_news_article(article)
    )


def is_renderable_hackernews_topic_article(article: Dict[str, Any]) -> bool:
    return is_hacker_news_article(article) and has_hacker_news_metadata(article) and bool(
        hacker_news_url(article)
    )


def hacker_news_url(article: Dict[str, Any]) -> str:
    return compact_text(article.get("hn_url") or article.get("comments_url"))


def hacker_news_article_url(article: Dict[str, Any]) -> str:
    return compact_text(article.get("external_url") or article_link(article))


def hacker_news_primary_url(article: Dict[str, Any]) -> str:
    return hacker_news_url(article) or hacker_news_article_url(article)


def parse_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def parse_optional_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def hacker_news_score_value(article: Dict[str, Any]) -> Optional[int]:
    hn_score = parse_optional_int(article.get("hn_score"))
    if hn_score is not None:
        return hn_score
    if hacker_news_url(article) or is_direct_hacker_news_article(article):
        return parse_optional_int(article.get("score"))
    return None


def hacker_news_score(article: Dict[str, Any]) -> int:
    return hacker_news_score_value(article) or 0


def hacker_news_comments_value(article: Dict[str, Any]) -> Optional[int]:
    hn_comments = parse_optional_int(
        article.get("hn_comments")
        or article.get("hn_comments_count")
        or article.get("hn_num_comments")
    )
    if hn_comments is not None:
        return hn_comments
    if hacker_news_url(article) or is_direct_hacker_news_article(article):
        return parse_optional_int(
            article.get("num_comments") or article.get("comments_count")
        )
    return None


def hacker_news_comments(article: Dict[str, Any]) -> int:
    return hacker_news_comments_value(article) or 0


def hacker_news_rank(article: Dict[str, Any]) -> int:
    rank = parse_int(article.get("hn_rank") or article.get("rank"))
    return rank if rank > 0 else 9999


def is_ai_related_hacker_news_article(article: Dict[str, Any]) -> bool:
    haystack = compact_text(article.get("title")).lower()
    return any(keyword_matches_text(keyword, haystack) for keyword in HN_AI_KEYWORDS)


def keyword_matches_text(keyword: str, text: str) -> bool:
    pattern = re.escape(keyword.lower()).replace(r"\ ", r"[\s-]+")
    return re.search(rf"(?<![a-z0-9]){pattern}(?![a-z0-9])", text) is not None


def select_hacker_news_top_articles(
    articles: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    sorted_articles = sorted(
        articles,
        key=lambda article: (
            -hacker_news_score(article),
            hacker_news_rank(article),
            compact_text(article.get("title")),
        ),
    )
    default_articles = sorted_articles[:HN_DEFAULT_LIMIT]
    default_article_ids = {id(article) for article in default_articles}
    ai_related_extras = [
        article
        for article in sorted(
            articles,
            key=lambda article: (
                hacker_news_rank(article),
                -hacker_news_score(article),
                compact_text(article.get("title")),
            ),
        )
        if id(article) not in default_article_ids
        and HN_DEFAULT_LIMIT < hacker_news_rank(article) <= HN_AI_RELATED_LIMIT
        and is_ai_related_hacker_news_article(article)
    ]
    return default_articles + ai_related_extras


def hackernews_topic_sort_key(article: Dict[str, Any]) -> tuple:
    rank = hacker_news_rank(article)
    has_rank = rank < 9999
    return (
        not has_rank,
        rank,
        -hacker_news_score(article),
        compact_text(article.get("title")),
    )


def select_hackernews_topic_articles(
    articles: Sequence[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    eligible = [
        article
        for article in articles
        if isinstance(article, dict) and is_renderable_hackernews_topic_article(article)
    ]
    return sorted(eligible, key=hackernews_topic_sort_key)


def find_hackernews_topic_data(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    topics = data.get("topics", {})
    if not isinstance(topics, dict):
        return None

    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        if not is_hackernews_topic(topic_id):
            continue

        topic_data = topics.get(topic_id)
        if isinstance(topic_data, dict):
            return topic_data

    return None


def has_renderable_hackernews_topic(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
) -> bool:
    topic_data = find_hackernews_topic_data(data, topic_defs)
    if topic_data is None:
        return False

    return bool(select_hackernews_topic_articles(topic_data.get("articles", []) or []))


def hacker_news_summary(article: Dict[str, Any]) -> str:
    return (
        compact_text(article.get("chat_summary"))
        or compact_text(article.get("summary"))
        or compact_text(article.get("snippet"))
        or compact_text(article.get("description"))
        or compact_text(article.get("title"))
    )


def render_hacker_news_top(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    articles = fixed_hacker_news_articles(data)
    if not articles:
        return None

    articles = select_hacker_news_top_articles(articles)
    articles = visible_registry.filter_unseen(articles)
    if not articles:
        return None

    lines = ["## 📰 Hacker News Top", ""]
    for index, article in enumerate(articles, 1):
        title = article.get("title", "?")
        score = hacker_news_score(article)
        comments = hacker_news_comments(article)
        lines.append(f"{index}. **{title}** — {score}↑ · {comments} comments")
        summary = hacker_news_summary(article)
        if summary:
            lines.append(f"   {summary}")
        lines.append(f"   🔗 {hacker_news_primary_url(article)}")
        primary_url = hacker_news_primary_url(article)
        article_url = hacker_news_article_url(article)
        if article_url and article_url != primary_url:
            lines.append(f"   ↗ {article_url}")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_hackernews_topic_item(article: Dict[str, Any]) -> List[str]:
    title = article.get("title", "?")
    lines = [
        f"• {title} — {hacker_news_score(article)}↑ · {hacker_news_comments(article)} comments",
        render_link(hacker_news_primary_url(article)),
    ]
    primary_url = hacker_news_primary_url(article)
    article_url = hacker_news_article_url(article)
    if article_url and article_url != primary_url:
        lines.append(f"  ↗ {article_url}")
    if article.get("multi_source"):
        lines.append(f"  *[{article.get('source_count', 2)} sources]*")
    return lines


def render_github_releases(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    releases = fixed_github_release_articles(data)
    if not releases:
        return None

    releases = sorted(releases, key=quality_score, reverse=True)
    releases = visible_registry.filter_unseen(releases)
    if not releases:
        return None

    lines = ["## 📦 GitHub Releases", ""]
    for article in releases:
        repo = article.get("repo") or article.get("source_name") or article.get(
            "title", "?"
        )
        tag = article.get("tag_name") or article.get("version") or "release"
        summary = article.get("summary") or article.get("snippet") or article.get(
            "title", ""
        )
        lines.append(f"• **{repo}** `{tag}` — {summary}")
        lines.append(render_link(article_link(article)))
        lines.append("")

    return "\n".join(lines).rstrip()


def render_github_trending(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    repos = fixed_github_trending_articles(data)
    if not repos:
        return None

    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    repos = visible_registry.filter_unseen(repos)
    repos = repos[:MAX_GITHUB_TRENDING_ITEMS]
    if not repos:
        return None

    lines = ["## 🐙 GitHub Trending", ""]
    for article in repos:
        repo = article.get("repo") or article.get("title", "?")
        stars = format_count(article.get("stars"))
        language = article.get("language") or "Unknown"
        description = article.get("description") or article.get("snippet") or ""
        lines.append(
            f"• **{repo}** ⭐ {stars} | {language} — {description}"
        )
        lines.append(render_link(article_link(article)))
        lines.append("")

    return "\n".join(lines).rstrip()


def render_blog_picks(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    picks = fixed_blog_pick_articles(data)
    if not picks:
        return None

    picks = sorted(picks, key=quality_score, reverse=True)
    picks = visible_registry.filter_unseen(picks)
    if not picks:
        return None

    lines = ["## 📝 Blog Picks", ""]
    for article in picks:
        author = article.get("author") or article.get("source_name") or "Unknown"
        summary = (
            article.get("full_text")
            or article.get("summary")
            or article.get("snippet")
            or ""
        )
        lines.append(f"• **{article.get('title', '?')}** — {author} | {summary}")
        lines.append(render_link(article_link(article)))
        lines.append("")

    return "\n".join(lines).rstrip()


def render_podcast_remix(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    episodes = podcast_remix_candidates(data)
    if not episodes:
        return None

    episodes = visible_registry.filter_unseen_limited(episodes, MAX_PODCAST_REMIX_ITEMS)
    if not episodes:
        return None

    lines = ["## 🎙️ Podcast Remix", ""]
    for article in episodes:
        show_name = article.get("show_name") or article.get("source_name") or "Unknown"
        lines.append(f"• **{article.get('title', '?')}** — {show_name}")
        lines.append(f"  {podcast_digest_summary(article)}")
        quote = podcast_quote(article)
        if quote:
            lines.append(f'  Quote: "{quote}"')
        lines.append(render_link(article_link(article)))
        lines.append("")

    return "\n".join(lines).rstrip()


def podcast_digest_summary(
    article: Dict[str, Any],
    prefer_chat_summary: bool = False,
) -> str:
    summary_fields = (
        ("chat_summary", "summary", "snippet", "description")
        if prefer_chat_summary
        else ("summary", "snippet", "description")
    )
    explicit_summary = next(
        (
            text
            for text in (
                compact_text(article.get(field))
                for field in summary_fields
            )
            if text
        ),
        "",
    )
    if explicit_summary:
        return explicit_summary

    title = compact_text(article.get("title")) or "This episode"
    show_name = compact_text(article.get("show_name") or article.get("source_name"))
    show_context = f" from {show_name}" if show_name else ""
    if podcast_has_transcript(article):
        return (
            f"{title}{show_context} has a usable transcript, but no prepared "
            "summary field was provided. Use the transcript quote below as the "
            "only specific evidence in this deterministic preview."
        )

    return (
        f"{title}{show_context} has no available transcript, so this metadata-only "
        "preview does not infer claims beyond the title and source metadata."
    )


def podcast_quote(article: Dict[str, Any]) -> str:
    if not podcast_has_transcript(article):
        return ""

    transcript = str(article.get("transcript", ""))
    for raw_line in transcript.splitlines():
        line = compact_text(raw_line)
        if not line:
            continue
        line = re.sub(
            r"^[^|]{1,40}\|\s*"
            r"\d{1,2}:\d{2}(?::\d{2})?\s*-\s*"
            r"\d{1,2}:\d{2}(?::\d{2})?\s*",
            "",
            line,
        )
        if not line:
            continue
        return line[:220]
    return ""


def render_chat_article_section(
    title: str,
    emoji: str,
    articles: Sequence[Dict[str, Any]],
) -> Optional[str]:
    visible_articles = [article for article in articles if article_link(article)]
    if not visible_articles:
        return None

    lines = [title, ""]
    for index, article in enumerate(visible_articles, 1):
        lines.append(render_chat_item(article, index, emoji))
        lines.append("")
    return "\n".join(lines).rstrip()


def render_chat_kol_updates(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    tweets = fixed_kol_articles(data)
    if not tweets:
        return None

    tweets = sorted(tweets, key=quality_score, reverse=True)
    tweets = visible_registry.filter_unseen(tweets)
    if not tweets:
        return None

    lines = ["## 📢 KOL Updates / 观点动态", ""]
    for index, article in enumerate(tweets, 1):
        lines.append(chat_title_line(article, index, "📢"))
        lines.append("")
        lines.append(chat_summary(article))
        lines.append("")
        lines.append(f"🔗 {article_link(article)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_chat_github_releases(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    releases = fixed_github_release_articles(data, filter_low_signal=True)
    releases = sorted(releases, key=quality_score, reverse=True)
    releases = visible_registry.filter_unseen(releases)
    return render_chat_article_section("## 📦 GitHub Releases / 发布", "📦", releases)


def render_chat_hacker_news_top(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    articles = fixed_hacker_news_articles(data)
    articles = select_hacker_news_top_articles(articles)
    articles = visible_registry.filter_unseen(articles)
    if not articles:
        return None

    lines = ["## 📰 Hacker News Top / 热榜", ""]
    for index, article in enumerate(articles, 1):
        lines.append(chat_title_line(article, index, "📰"))
        lines.append("")
        lines.append(
            f"{hacker_news_score(article)}↑ · "
            f"{hacker_news_comments(article)} comments · "
            f"{hacker_news_summary(article)}"
        )
        lines.append("")
        lines.append(f"🔗 {hacker_news_primary_url(article)}")
        primary_url = hacker_news_primary_url(article)
        article_url = hacker_news_article_url(article)
        if article_url and article_url != primary_url:
            lines.append(f"↗ {article_url}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_chat_hackernews_topic_item(
    article: Dict[str, Any],
    index: int,
    emoji: str,
) -> List[str]:
    lines = [
        chat_title_line(article, index, emoji),
        "",
        (
            f"{hacker_news_score(article)}↑ · "
            f"{hacker_news_comments(article)} comments · "
            f"{hacker_news_summary(article)}"
        ),
        "",
        f"🔗 {hacker_news_primary_url(article)}",
    ]
    primary_url = hacker_news_primary_url(article)
    article_url = hacker_news_article_url(article)
    if article_url and article_url != primary_url:
        lines.append(f"↗ {article_url}")
    return lines


def render_chat_github_trending(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    repos = fixed_github_trending_articles(data)
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    repos = visible_registry.filter_unseen(repos)
    repos = repos[:MAX_GITHUB_TRENDING_ITEMS]
    return render_chat_article_section("## 🐙 GitHub Trending / 趋势", "🐙", repos)


def render_chat_blog_picks(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    picks = fixed_blog_pick_articles(data)
    picks = sorted(picks, key=quality_score, reverse=True)
    picks = visible_registry.filter_unseen(picks)
    return render_chat_article_section("## 📝 Blog Picks / 博客精选", "📝", picks)


def render_chat_podcast_remix(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
    episodes = podcast_remix_candidates(data)
    episodes = visible_registry.filter_unseen_limited(episodes, MAX_PODCAST_REMIX_ITEMS)
    if not episodes:
        return None

    lines = ["## 🎙️ Podcast Remix / 播客精选", ""]
    for index, article in enumerate(episodes, 1):
        lines.append(chat_title_line(article, index, "🎙️"))
        lines.append("")
        lines.append(podcast_digest_summary(article, prefer_chat_summary=True))
        quote = podcast_quote(article)
        if quote:
            lines.append(f'Quote: "{quote}"')
        lines.append("")
        lines.append(f"🔗 {article_link(article)}")
        lines.append("")
    return "\n".join(lines).rstrip()


def first_sentence(text: str) -> str:
    compact = compact_text(text)
    for index, char in enumerate(compact):
        if char not in ("。", ".", "！", "!", "？", "?"):
            continue
        if (
            char == "."
            and index > 0
            and index + 1 < len(compact)
            and compact[index - 1].isdigit()
            and compact[index + 1].isdigit()
        ):
            continue
        if (
            char == "."
            and index > 0
            and index + 1 < len(compact)
            and compact[index - 1].isupper()
            and (
                compact[index + 1].isupper()
                or (
                    index >= 2
                    and compact[index - 2] == "."
                )
            )
        ):
            continue
        if char == "." and is_known_sentence_abbreviation(compact, index):
            continue
        return compact[: index + 1]
    return compact


def is_known_sentence_abbreviation(text: str, period_index: int) -> bool:
    start = period_index - 1
    while start >= 0 and text[start].isalpha():
        start -= 1
    token = text[start + 1:period_index].lower()
    if token in {
        "dr",
        "jr",
        "mr",
        "mrs",
        "ms",
        "prof",
        "sr",
    }:
        return True

    if token not in {"co", "corp", "inc", "ltd"}:
        return False

    next_start = period_index + 1
    while next_start < len(text) and text[next_start].isspace():
        next_start += 1
    return next_start < len(text) and text[next_start].islower()


def render_chat_intro(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
) -> Optional[str]:
    candidates: List[Dict[str, Any]] = []
    registry = VisibleArticleRegistry()
    registry.register_aliases(visible_alias_candidates(data, topic_defs, template="chat"))

    topics = data.get("topics", {})
    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        topic_data = topics.get(topic_id)
        if not isinstance(topic_data, dict):
            continue
        topic_articles = topic_render_candidate_articles(topic_id, topic_data, "chat")
        if is_hackernews_topic(topic_id):
            candidates.extend(
                registry.filter_unseen_limited(topic_articles, HN_DEFAULT_LIMIT)
            )
        else:
            candidates.extend(registry.filter_unseen(topic_articles))

    highlights = sorted(candidates, key=quality_score, reverse=True)[:3]
    lines = []
    if highlights:
        lines.append("今日看点")
        for article in highlights:
            summary = first_sentence(chat_summary(article))
            lines.append(f"• {summary}")

    return "\n".join(lines) if lines else None


def source_count(data: Dict[str, Any], key: str) -> int:
    input_sources = data.get("input_sources", {})
    value = input_sources.get(key, 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def source_count_first_present(data: Dict[str, Any], keys: Sequence[str]) -> int:
    input_sources = data.get("input_sources", {})
    for key in keys:
        if key in input_sources:
            return source_count(data, key)
    return 0


def render_footer(data: Dict[str, Any], version: str) -> str:
    stats = data.get("output_stats", {})
    merged = stats.get("total_articles", 0)
    trending_count = source_count_first_present(
        data,
        ("github_trending", "trending_repositories"),
    )
    return "\n".join(
        [
            "---",
            (
                "📊 Data Sources: "
                f"RSS {source_count(data, 'rss_articles')} | "
                f"Twitter {source_count(data, 'twitter_articles')} | "
                f"Reddit {source_count(data, 'reddit_posts')} | "
                f"Web {source_count(data, 'web_articles')} | "
                f"GitHub {source_count(data, 'github_articles')} releases + "
                f"{trending_count} trending | "
                f"Podcast {source_count(data, 'podcast_episodes')} episodes | "
                f"Dedup: {merged} articles"
            ),
            (
                f"🤖 Generated by follow-news v{version} | "
                "🔗 https://github.com/tangwz/follow-news | Powered by OpenClaw"
            ),
        ]
    )


def render_digest(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    report_date: str,
    version: str,
    template: str = "discord",
) -> str:
    if template == "chat":
        return render_chat_digest(data, topic_defs, report_date, version)
    if template != "discord":
        raise ValueError(f"Unsupported template: {template}")

    sections = [f"# 🚀 Tech Digest - {report_date}"]
    visible_registry = VisibleArticleRegistry()
    visible_registry.register_aliases(
        visible_alias_candidates(data, topic_defs, template="discord")
    )
    sections.extend(render_topic_sections(data, topic_defs, visible_registry))
    skip_hacker_news_top = has_renderable_hackernews_topic(data, topic_defs)

    for renderer in (
        render_kol_updates,
        render_hacker_news_top,
        render_github_releases,
        render_github_trending,
        render_blog_picks,
        render_podcast_remix,
    ):
        if skip_hacker_news_top and renderer is render_hacker_news_top:
            continue
        section = renderer(data, visible_registry)
        if section:
            sections.append(section)

    sections.append(render_footer(data, version))
    return "\n\n".join(sections).rstrip() + "\n"


def render_chat_digest(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    report_date: str,
    version: str,
) -> str:
    visible_registry = VisibleArticleRegistry()
    visible_registry.register_aliases(
        visible_alias_candidates(data, topic_defs, template="chat")
    )
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    intro = render_chat_intro(data, topic_defs)
    if intro:
        sections.append(intro)
    sections.extend(render_chat_topic_sections(data, topic_defs, visible_registry))
    skip_hacker_news_top = has_renderable_hackernews_topic(data, topic_defs)

    for renderer in (
        render_chat_kol_updates,
        render_chat_hacker_news_top,
        render_chat_github_releases,
        render_chat_github_trending,
        render_chat_blog_picks,
        render_chat_podcast_remix,
    ):
        if skip_hacker_news_top and renderer is render_chat_hacker_news_top:
            continue
        section = renderer(data, visible_registry)
        if section:
            sections.append(section)

    sections.append(render_footer(data, version))
    return "\n\n".join(sections).rstrip() + "\n"


def summarize_fixture(data: Dict[str, Any]) -> str:
    stats = data.get("output_stats", {})
    topics = data.get("topics", {})
    total_articles = stats.get("total_articles", 0)

    lines = [
        "Acceptance digest fixture summary",
        f"Total articles: {total_articles}",
        f"Topics: {len(topics)}",
        "",
    ]

    for topic_id in sorted(topics):
        topic_data = topics.get(topic_id, {})
        if not isinstance(topic_data, dict):
            continue

        articles = [
            article
            for article in topic_data.get("articles", [])
            if isinstance(article, dict)
        ]
        lines.append(f"## {topic_id} ({len(articles)} articles)")
        for article in sorted(articles, key=lambda item: item.get("title", "")):
            title = article.get("title", "?")
            source_type = article.get("source_type", "unknown")
            summary = (
                article.get("summary")
                or article.get("snippet")
                or article.get("description")
                or article.get("full_text")
                or ""
            )
            lines.append(f"- [{source_type}] {title}")
            if summary:
                lines.append(f"  Summary: {summary}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_codex_prompt(report_date: str, version: str, template: str) -> str:
    return "\n".join(
        [
            "# Manual Codex Acceptance Context",
            "",
            "Use this folder to review the deterministic digest renderer manually.",
            "",
            "Rules:",
            "- Do not run the network pipeline.",
            "- Use merged.json as the only source fixture.",
            "- Use summarized.txt for a quick fixture overview.",
            (
                "- Follow references/digest-prompt.md and "
                f"references/templates/{template}.md as the source-of-truth "
                "Markdown and Discord formatting rules."
            ),
            (
                "- Treat expected.md as a deterministic comparison sample, "
                "not as the prompt source of truth."
            ),
            "- Save the generated report as `actual.md` in this directory.",
            "- Compare expected.md vs actual.md with `diff -u expected.md actual.md`.",
            "- Keep golden updates gated by UPDATE_GOLDEN=1.",
            f"- Report date: {report_date}",
            f"- follow-news version: {version}",
            "",
        ]
    )


def prepare_codex_acceptance_context(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    source_fixture: Path,
    output_dir: Path,
    report_date: str,
    version: str,
    template: str = "discord",
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(source_fixture, output_dir / "merged.json")
    (output_dir / "summarized.txt").write_text(
        summarize_fixture(data),
        encoding="utf-8",
    )
    (output_dir / "prompt.md").write_text(
        build_codex_prompt(report_date, version, template),
        encoding="utf-8",
    )
    (output_dir / "expected.md").write_text(
        render_digest(data, topic_defs, report_date, version, template=template),
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render deterministic Markdown/Discord digest acceptance output."
    )
    parser.add_argument("--input", type=Path, required=True, help="Merged JSON input")
    parser.add_argument("--topics", type=Path, required=True, help="Topics JSON file")
    parser.add_argument("--date", required=True, help="Report date in YYYY-MM-DD format")
    parser.add_argument("--version", required=True, help="follow-news version string")
    parser.add_argument(
        "--template",
        choices=("discord", "chat"),
        default="discord",
        help="Output template to render",
    )
    parser.add_argument("--output", type=Path, help="Markdown output path")
    parser.add_argument(
        "--prepare-codex-context",
        type=Path,
        help="Directory for manual Codex acceptance context files",
    )
    return parser


def parse_args() -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_json(args.input)
    topic_defs = load_topic_definitions(args.topics)
    if args.prepare_codex_context:
        prepare_codex_acceptance_context(
            data,
            topic_defs,
            args.input,
            args.prepare_codex_context,
            args.date,
            args.version,
            template=args.template,
        )
        return 0

    if not args.output:
        parser = build_parser()
        parser.error("--output is required unless --prepare-codex-context is used")

    output = render_digest(
        data,
        topic_defs,
        args.date,
        args.version,
        template=args.template,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
