#!/usr/bin/env python3
"""Acceptance tests for final Markdown/Discord digest output."""

import difflib
import importlib.util
import json
import os
import re
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch


ROOT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"
GOLDEN_DIR = ROOT_DIR / "tests" / "golden"
TOPICS_FILE = ROOT_DIR / "config" / "defaults" / "topics.json"
ACCEPTANCE_FIXTURE = FIXTURES_DIR / "acceptance-merged.json"
DAILY_GOLDEN = GOLDEN_DIR / "daily-discord.md"
DAILY_CHAT_GOLDEN = GOLDEN_DIR / "daily-chat.md"
FIXED_DIGEST_SECTIONS = {
    "## 📢 KOL Updates",
    "## 📰 Hacker News Top",
    "## 📦 GitHub Releases",
    "## 🐙 GitHub Trending",
    "## 📝 Blog Picks",
    "## 🎙️ Podcast Remix",
}

spec = importlib.util.spec_from_file_location(
    "render_acceptance_digest",
    SCRIPTS_DIR / "render-acceptance-digest.py",
)
render_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mod)

merge_spec = importlib.util.spec_from_file_location(
    "merge_sources",
    SCRIPTS_DIR / "merge-sources.py",
)
merge_mod = importlib.util.module_from_spec(merge_spec)
merge_spec.loader.exec_module(merge_mod)

fetch_github_spec = importlib.util.spec_from_file_location(
    "fetch_github",
    SCRIPTS_DIR / "fetch-github.py",
)
fetch_github_mod = importlib.util.module_from_spec(fetch_github_spec)
fetch_github_spec.loader.exec_module(fetch_github_mod)

fetch_rss_spec = importlib.util.spec_from_file_location(
    "fetch_rss",
    SCRIPTS_DIR / "fetch-rss.py",
)
fetch_rss_mod = importlib.util.module_from_spec(fetch_rss_spec)
fetch_rss_spec.loader.exec_module(fetch_rss_mod)


def load_acceptance_fixture():
    return json.loads(ACCEPTANCE_FIXTURE.read_text(encoding="utf-8"))


def render_daily_digest():
    data = load_acceptance_fixture()
    topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)
    return render_mod.render_digest(
        data,
        topic_defs,
        report_date="2026-02-27",
        version="3.17.0",
    )


def render_daily_chat_digest():
    data = load_acceptance_fixture()
    topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)
    return render_mod.render_digest(
        data,
        topic_defs,
        report_date="2026-02-27",
        version="3.17.0",
        template="chat",
    )


def duplicate_visible_fixture():
    return {
        "input_sources": {},
        "output_stats": {"total_articles": 3},
        "topics": {
            "llm": {
                "articles": [
                    {
                        "title": "Independent blog post about agent evals",
                        "link": "https://example.com/blog/agent-evals?utm_source=rss",
                        "quality_score": 12,
                        "source_type": "rss",
                        "source_name": "Example Blog",
                        "author": "Example Author",
                        "is_blog_pick": True,
                        "summary": "The post explains a compact agent evaluation pattern.",
                    },
                    {
                        "title": "Agent planning podcast episode",
                        "link": "https://www.youtube.com/watch?v=abc123&utm_source=rss",
                        "quality_score": 11,
                        "source_type": "podcast",
                        "source_name": "Training Data",
                        "show_name": "Training Data",
                        "transcript_status": "ok",
                        "transcript": "The episode discusses planning, evaluation, and rollout checks.",
                        "snippet": "A podcast episode about planning and evaluation.",
                    },
                ]
            },
            "ai-agent": {
                "articles": [
                    {
                        "title": "KOL note about agent reliability",
                        "link": "https://x.com/example/status/1?utm_source=rss",
                        "quality_score": 10,
                        "source_type": "twitter",
                        "source_name": "Example Lab",
                        "display_name": "Example Lab",
                        "handle": "example",
                        "summary": "Example Lab shared a note about agent reliability.",
                        "metrics": {
                            "impression_count": 1000,
                            "reply_count": 2,
                            "retweet_count": 3,
                            "like_count": 4,
                        },
                    }
                ]
            },
        },
    }


def topic_topic_duplicate_fixture():
    duplicate_article = {
        "title": "Duplicate agent evals article",
        "link": "https://example.com/shared/agent-evals",
        "quality_score": 12,
        "source_type": "rss",
        "summary": "A shared article that appears in two topic sections.",
    }
    return {
        "input_sources": {},
        "output_stats": {"total_articles": 2},
        "topics": {
            "llm": {"articles": [duplicate_article]},
            "ai-agent": {"articles": [dict(duplicate_article)]},
        },
    }


def same_title_duplicate_fixture():
    return {
        "input_sources": {},
        "output_stats": {"total_articles": 2},
        "topics": {
            "llm": {
                "articles": [
                    {
                        "title": "Same Story",
                        "link": "https://example.com/a",
                        "quality_score": 12,
                        "source_type": "rss",
                        "summary": "The first visible instance of the story.",
                    }
                ]
            },
            "ai-agent": {
                "articles": [
                    {
                        "title": "Same Story!",
                        "link": "https://other.example/b",
                        "quality_score": 11,
                        "source_type": "rss",
                        "summary": "The duplicate story with a different URL.",
                    }
                ]
            },
        },
    }


def cross_fixed_bridge_fixture():
    return {
        "input_sources": {},
        "output_stats": {"total_articles": 3},
        "topics": {
            "supplemental": {
                "articles": [
                    {
                        "title": "Canonical",
                        "link": "https://x.com/example/status/a",
                        "quality_score": 12,
                        "source_type": "twitter",
                        "display_name": "Example Lab",
                        "handle": "example",
                        "summary": "The first fixed-section item.",
                    },
                    {
                        "title": "Bridge",
                        "link": "https://github.com/example/bridge/releases/tag/v1.0.0",
                        "quality_score": 11,
                        "source_type": "github",
                        "repo": "example/bridge",
                        "tag_name": "v1.0.0",
                        "summary": "This earlier fixed renderer item is connected later.",
                    },
                    {
                        "title": "Bridge",
                        "link": "https://x.com/example/status/a",
                        "quality_score": 10,
                        "source_type": "rss",
                        "is_blog_pick": True,
                        "author": "Example Author",
                        "full_text": "The late bridge that connects the prior fixed items.",
                    },
                ]
            }
        },
    }


def extract_chat_summary(text, title_line):
    lines = text.splitlines()
    index = lines.index(title_line)
    return lines[index + 2]


def assert_or_update_golden(testcase, expected_path, actual):
    if os.environ.get("UPDATE_GOLDEN") == "1":
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(actual, encoding="utf-8")
        print(f"golden updated: {expected_path}")
        return

    if not expected_path.exists():
        raise AssertionError(
            f"Golden file is missing: {expected_path}. "
            "Run with UPDATE_GOLDEN=1 to create it."
        )

    expected = expected_path.read_text(encoding="utf-8")
    if actual != expected:
        diff = "".join(
            difflib.unified_diff(
                expected.splitlines(keepends=True),
                actual.splitlines(keepends=True),
                fromfile=str(expected_path),
                tofile="rendered daily digest",
            )
        )
        testcase.fail(f"Golden mismatch for {expected_path}:\n" + diff)


class TestAcceptanceFixture(unittest.TestCase):
    def test_fixture_covers_acceptance_sections(self):
        data = load_acceptance_fixture()
        self.assertEqual(data["output_stats"]["total_articles"], 9)
        self.assertEqual(data["output_stats"]["topics_count"], len(data["topics"]))

        articles = [
            article
            for topic in data["topics"].values()
            for article in topic.get("articles", [])
        ]
        actual_topic_distribution = {
            topic_name: len(topic.get("articles", []))
            for topic_name, topic in data["topics"].items()
        }
        source_types = {article.get("source_type") for article in articles}

        self.assertEqual(
            data["output_stats"]["topic_distribution"],
            actual_topic_distribution,
        )
        self.assertIn("rss", source_types)
        self.assertIn("twitter", source_types)
        self.assertIn("github", source_types)
        self.assertIn("github_trending", source_types)
        self.assertIn("podcast", source_types)
        self.assertTrue(any(article.get("multi_source") for article in articles))
        self.assertTrue(any(article.get("is_blog_pick") for article in articles))
        self.assertTrue(
            any(
                article.get("transcript_status") == "ok"
                and article.get("transcript")
                for article in articles
            )
        )


class TestVisibleArticleDedupe(unittest.TestCase):
    def test_article_dedupe_key_normalizes_equivalent_urls(self):
        first = {
            "title": "First title",
            "link": "https://www.youtube.com/watch?v=abc123&utm_source=rss",
        }
        second = {
            "title": "Different title",
            "link": "https://youtu.be/abc123",
        }

        self.assertEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_preserves_meaningful_query_parameters(self):
        first = {"link": "https://news.ycombinator.com/item?id=1"}
        second = {"link": "https://news.ycombinator.com/item?id=2"}

        self.assertNotEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_visible_registry_matches_hackernews_link_with_hn_url(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark(
            {
                "title": "Prior discussion link",
                "link": "https://news.ycombinator.com/item?id=3",
            }
        )

        self.assertTrue(
            registry.is_seen(
                {
                    "title": "Different article title",
                    "link": "https://example.com/story-3",
                    "hn_url": "https://news.ycombinator.com/item?id=3",
                }
            )
        )

    def test_article_dedupe_key_preserves_ref_query_parameters(self):
        first = {"link": "https://example.com/post?ref=a"}
        second = {"link": "https://example.com/post?ref=b"}

        self.assertNotEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_preserves_path_parameters(self):
        first = {"link": "https://example.com/post;v=1"}
        second = {"link": "https://example.com/post;v=2"}

        self.assertNotEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_drops_tracking_query_parameters(self):
        first = {"link": "https://example.com/post?utm_source=rss&fbclid=x"}
        second = {"link": "https://www.example.com/post?utm_medium=email"}

        self.assertEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_keeps_meaningful_query_without_tracking_noise(self):
        first = {"link": "https://example.com/post?id=1&utm_source=rss"}
        second = {"link": "https://www.example.com/post?utm_medium=email&id=1"}

        self.assertEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_visible_registry_propagates_aliases_from_skipped_duplicates(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark({"title": "Same Story", "link": "https://example.com/a"})

        visible = registry.filter_unseen(
            [
                {"title": "Same Story!", "link": "https://example.com/b"},
                {"title": "Different Label", "link": "https://example.com/b"},
            ]
        )

        self.assertEqual(visible, [])

    def test_visible_registry_propagates_late_bridge_aliases_before_rendering(self):
        registry = render_mod.VisibleArticleRegistry()

        visible = registry.filter_unseen(
            [
                {"title": "Canonical", "link": "https://example.com/a"},
                {"title": "Bridge", "link": "https://example.com/b"},
                {"title": "Bridge", "link": "https://example.com/a"},
            ]
        )

        self.assertEqual(
            [article["link"] for article in visible],
            ["https://example.com/a"],
        )

    def test_visible_registry_applies_prior_seen_late_bridge_aliases(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark({"title": "Canonical", "link": "https://example.com/a"})

        visible = registry.filter_unseen(
            [
                {"title": "Bridge", "link": "https://example.com/b"},
                {"title": "Bridge", "link": "https://example.com/a"},
            ]
        )

        self.assertEqual(visible, [])

    def test_visible_registry_limited_filter_pre_registers_late_bridge_aliases(self):
        registry = render_mod.VisibleArticleRegistry()

        visible = registry.filter_unseen_limited(
            [
                {"title": "Canonical", "link": "https://example.com/a"},
                {"title": "Bridge", "link": "https://example.com/b"},
                {"title": "Bridge", "link": "https://example.com/a"},
            ],
            limit=2,
        )

        self.assertEqual(
            [article["link"] for article in visible],
            ["https://example.com/a"],
        )

    def test_visible_registry_passes_no_key_articles_without_dedupe(self):
        registry = render_mod.VisibleArticleRegistry()
        articles = [{"source_type": "rss"}, {"source_type": "web"}]

        self.assertEqual(registry.filter_unseen(articles), articles)

    def test_visible_registry_handles_deep_alias_chains(self):
        registry = render_mod.VisibleArticleRegistry()
        articles = [
            {
                "title": "Shared release title",
                "link": f"https://example.com/releases/{index}",
            }
            for index in range(1200)
        ]

        visible = registry.filter_unseen(articles)

        self.assertEqual(visible, articles[:1])

    def test_article_dedupe_key_only_strips_leading_www(self):
        self.assertEqual(
            render_mod.article_dedupe_key(
                {"link": "https://www.example.com/post"}
            ),
            render_mod.article_dedupe_key({"link": "https://example.com/post"}),
        )
        self.assertNotEqual(
            render_mod.article_dedupe_key(
                {"link": "https://api.www.example.com/post"}
            ),
            render_mod.article_dedupe_key(
                {"link": "https://api.example.com/post"}
            ),
        )

    def test_visible_registry_matches_same_title_with_different_urls(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark({"title": "Same Story", "link": "https://example.com/a"})

        self.assertTrue(
            registry.is_seen(
                {"title": "Same Story!", "link": "https://other.example/b"}
            )
        )

    def test_article_dedupe_key_keeps_versioned_titles_distinct(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark(
            {"title": "OpenAI releases GPT-5", "link": "https://example.com/gpt-5"}
        )

        self.assertFalse(
            registry.is_seen(
                {
                    "title": "OpenAI releases GPT-4",
                    "link": "https://example.com/gpt-4",
                }
            )
        )

    def test_article_dedupe_key_keeps_punctuation_version_titles_distinct(self):
        first = {"title": "OpenAI releases GPT-4.1"}
        second = {"title": "OpenAI releases GPT-41"}

        self.assertNotEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_keeps_dash_subtitles_distinct(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark(
            {
                "title": "Claude Code - repository-wide planning mode",
                "link": "https://example.com/planning",
            }
        )

        self.assertFalse(
            registry.is_seen(
                {
                    "title": "Claude Code - terminal UI refresh",
                    "link": "https://example.com/ui",
                }
            )
        )

    def test_article_dedupe_key_keeps_title_case_dash_subtitles_distinct(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark(
            {
                "title": "Claude Code - Runtime Internals",
                "link": "https://example.com/runtime",
            }
        )

        self.assertFalse(
            registry.is_seen(
                {
                    "title": "Claude Code - Deployment Guide",
                    "link": "https://example.com/deploy",
                }
            )
        )

    def test_article_dedupe_key_keeps_pipe_subtitles_distinct(self):
        registry = render_mod.VisibleArticleRegistry()
        registry.mark(
            {
                "title": "Claude Code | Runtime Internals",
                "link": "https://example.com/runtime",
            }
        )

        self.assertFalse(
            registry.is_seen(
                {
                    "title": "Claude Code | Deployment Guide",
                    "link": "https://example.com/deploy",
                }
            )
        )

    def test_fixed_sections_propagate_aliases_before_unique_collapse(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 3},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Same Story",
                            "link": "https://x.com/example/status/a",
                            "quality_score": 12,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "The first visible item.",
                        },
                        {
                            "title": "Bridge Title",
                            "link": "https://x.com/example/status/a",
                            "quality_score": 11,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "A duplicate raw URL that carries a title alias.",
                        },
                        {
                            "title": "Bridge Title!",
                            "link": "https://x.com/example/status/b",
                            "quality_score": 10,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "This later alias URL must not render.",
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertEqual(text.count("https://x.com/example/status/a"), 1)
        self.assertNotIn("https://x.com/example/status/b", text)

    def test_article_dedupe_key_keeps_hyphenated_titles_intact(self):
        self.assertEqual(
            render_mod.normalize_visible_title("State-of-the-art agents"),
            "stateoftheart agents",
        )

    def test_article_dedupe_key_strips_matching_source_suffixes(self):
        title = "OpenAI releases GPT-5"

        self.assertEqual(
            render_mod.article_dedupe_keys(
                {"title": f"{title} | Example News", "source_name": "Example News"}
            )[-1],
            render_mod.article_dedupe_keys(
                {"title": title, "source_name": "Example News"}
            )[-1],
        )
        self.assertEqual(
            render_mod.article_dedupe_keys(
                {"title": f"{title} - Example News", "source_name": "Example News"}
            )[-1],
            render_mod.article_dedupe_keys(
                {"title": title, "source_name": "Example News"}
            )[-1],
        )
        self.assertEqual(
            render_mod.article_dedupe_keys(
                {"title": f"{title} – Example News", "source_name": "Example News"}
            )[-1],
            render_mod.article_dedupe_keys(
                {"title": title, "source_name": "Example News"}
            )[-1],
        )

    def test_article_dedupe_key_keeps_non_matching_source_suffixes(self):
        self.assertNotEqual(
            render_mod.article_dedupe_keys(
                {
                    "title": "Claude Code | Runtime Internals",
                    "source_name": "Example News",
                }
            )[-1],
            render_mod.article_dedupe_keys(
                {"title": "Claude Code", "source_name": "Example News"}
            )[-1],
        )

    def test_article_dedupe_key_falls_back_to_normalized_title(self):
        first = {"title": "RT @user: OpenAI releases GPT-5!"}
        second = {"title": "OpenAI releases GPT-5"}

        self.assertEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_returns_none_without_url_or_title(self):
        self.assertIsNone(render_mod.article_dedupe_key({"source_type": "rss"}))


class TestAcceptanceRenderer(unittest.TestCase):
    def test_chat_title_uses_unicode_bold_text(self):
        self.assertEqual(
            render_mod.bold_chat_title_text("OpenAI 123 发布"),
            "𝐎𝐩𝐞𝐧𝐀𝐈 𝟏𝟐𝟑 发布",
        )

    def test_daily_digest_matches_golden(self):
        assert_or_update_golden(self, DAILY_GOLDEN, render_daily_digest())

    def test_daily_chat_digest_matches_golden(self):
        assert_or_update_golden(self, DAILY_CHAT_GOLDEN, render_daily_chat_digest())

    def test_daily_chat_digest_structure_contract(self):
        text = render_daily_chat_digest()
        lines = text.splitlines()

        self.assertTrue(text.startswith("# 🚀 Tech Digest - 2026-02-27\n"))
        self.assertNotIn("评分说明：", text)
        self.assertIn("今日看点", text)
        self.assertIn("## 🧠 LLM / 大模型", text)
        self.assertIn(
            f"1. {render_mod.bold_chat_title_text('OpenAI ships structured agent evaluation suite')}",
            text,
        )
        self.assertNotRegex(text, r"(?m)^[0-9]+\. \[[0-9]+(?:\.[0-9]+)?/10\] ")
        self.assertNotIn("1. 🧠", text)
        self.assertNotIn("来源：", text)
        self.assertIn("🔗 https://openai.com/research/agent-evals", text)
        self.assertNotIn("<https://", text)
        self.assertNotIn("Low scoring model rumor should not render", text)

        title_lines = [
            line
            for line in lines
            if re.match(r"^[0-9]+\. .+", line)
        ]
        self.assertGreater(len(title_lines), 0)

        for index, line in enumerate(lines):
            if not re.match(r"^[0-9]+\. .+", line):
                continue
            self.assertLess(index + 4, len(lines))
            self.assertEqual(lines[index + 1], "")
            self.assertNotEqual(lines[index + 2], "")
            self.assertEqual(lines[index + 3], "")
            self.assertRegex(lines[index + 4], r"^🔗 https?://.+$")

        section_starts = [
            index for index, line in enumerate(lines) if line.startswith("## ")
        ]
        for position, start in enumerate(section_starts):
            end = (
                section_starts[position + 1]
                if position + 1 < len(section_starts)
                else len(lines)
            )
            section_text = "\n".join(lines[start:end])
            self.assertRegex(
                section_text,
                r"(?m)^[0-9]+\. .+",
                lines[start],
            )

    def test_chat_fixed_sections_use_consistent_numbered_item_shape(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.0",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.0",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.0",
                            "summary": "The release ships a stable API.",
                            "quality_score": 10,
                        },
                        {
                            "title": "Example Blog Pick",
                            "link": "https://example.com/blog",
                            "source_type": "rss",
                            "is_blog_pick": True,
                            "author": "Example Author",
                            "full_text": "The post explains a concise engineering pattern.",
                            "quality_score": 9,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 📦 GitHub Releases / 发布", text)
        self.assertIn("## 📝 Blog Picks / 博客精选", text)
        fixed_text = text.split("## 📦 GitHub Releases / 发布", 1)[1]
        self.assertIn(
            f"1. {render_mod.bold_chat_title_text('Example Tool v1.0.0')}",
            fixed_text,
        )
        self.assertNotIn("来源：", fixed_text)
        self.assertNotRegex(fixed_text, r"(?m)^• ")

    def test_chat_github_releases_filter_low_signal_prereleases(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "picoclaw nightly",
                            "link": "https://github.com/sipeed/picoclaw/releases/tag/nightly",
                            "source_type": "github",
                            "repo": "sipeed/picoclaw",
                            "tag_name": "nightly",
                            "summary": "Nightly build.",
                            "quality_score": 10,
                        },
                        {
                            "title": "crewAI 1.14.5a7",
                            "link": "https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a7",
                            "source_type": "github",
                            "repo": "crewAIInc/crewAI",
                            "tag_name": "1.14.5a7",
                            "summary": "Alpha pre-release.",
                            "quality_score": 10,
                            "prerelease": True,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("picoclaw nightly", text)
        self.assertNotIn("crewAI 1.14.5a7", text)

    def test_discord_github_releases_keep_low_signal_releases(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "picoclaw nightly",
                            "link": "https://github.com/sipeed/picoclaw/releases/tag/nightly",
                            "source_type": "github",
                            "repo": "sipeed/picoclaw",
                            "tag_name": "nightly",
                            "summary": "Nightly build.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="discord",
        )

        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("sipeed/picoclaw", text)
        self.assertIn("`nightly`", text)

    def test_chat_github_releases_keep_real_package_release(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.0",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.0",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.0",
                            "summary": "Adds a Python package for CLI users.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 📦 GitHub Releases / 发布", text)
        self.assertIn(render_mod.bold_chat_title_text("Example Tool v1.0.0"), text)

    def test_chat_github_releases_filter_named_dependency_bump(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.1",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.1",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.1",
                            "summary": "Bump lodash from 4.17.20 to 4.17.21.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.0.1", text)

    def test_chat_github_releases_filter_dependency_update_with_package_signal_word(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.2",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.2",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.2",
                            "summary": "Update dependencies: fastapi and pydantic.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.0.2", text)

    def test_chat_github_releases_filter_alpha_tag_from_title(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "crewAI 1.14.5a7",
                            "link": "https://github.com/crewAIInc/crewAI/releases/tag/1.14.5a7",
                            "source_type": "github",
                            "repo": "crewAIInc/crewAI",
                            "summary": "Release notes include minor changes.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("crewAI 1.14.5a7", text)

    def test_chat_github_releases_keep_stable_project_with_alpha_in_name(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "AlphaFold v1.0.0",
                            "link": "https://github.com/example/alphafold/releases/tag/v1.0.0",
                            "source_type": "github",
                            "repo": "example/alphafold",
                            "tag_name": "v1.0.0",
                            "summary": "Stable release.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 📦 GitHub Releases / 发布", text)
        self.assertIn(render_mod.bold_chat_title_text("AlphaFold v1.0.0"), text)

    def test_chat_github_releases_filter_dotted_release_candidate_tag(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.0-rc.1",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.0-rc.1",
                            "source_type": "github",
                            "repo": "example/tool",
                            "summary": "Release candidate notes.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.0.0-rc.1", text)

    def test_chat_github_releases_filter_pre_release_tag_from_title(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.0-pre.1",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.0-pre.1",
                            "source_type": "github",
                            "repo": "example/tool",
                            "summary": "Pre-release notes.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.0.0-pre.1", text)

    def test_chat_github_releases_filter_attached_release_candidate_tag(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.2.0rc1",
                            "link": "https://github.com/example/tool/releases/tag/v1.2.0rc1",
                            "source_type": "github",
                            "repo": "example/tool",
                            "summary": "Release candidate notes.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.2.0rc1", text)

    def test_chat_github_releases_filter_singular_dependency_update(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.0.3",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.3",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.3",
                            "summary": "Dependency update: lodash 4.17.21.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("Example Tool v1.0.3", text)

    def test_chat_github_releases_filter_dependency_bump_for_api_repo(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "foo/api v1.0.1",
                            "link": "https://github.com/foo/api/releases/tag/v1.0.1",
                            "source_type": "github",
                            "repo": "foo/api",
                            "tag_name": "v1.0.1",
                            "summary": "Bump lodash from 4.17.20 to 4.17.21.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("foo/api v1.0.1", text)

    def test_chat_github_releases_keep_dependency_injection_update(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Example Tool v1.1.0",
                            "link": "https://github.com/example/tool/releases/tag/v1.1.0",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.1.0",
                            "summary": "Update dependency injection container for plugin loading.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn(render_mod.bold_chat_title_text("Example Tool v1.1.0"), text)

    def test_group_by_topics_prefers_content_keyword_match_over_topic_order(self):
        articles = [
            {
                "title": "GDS weighs in on the NHS open source decision",
                "snippet": "Government Digital Service discussed public sector open source policy.",
                "topics": ["llm", "frontier-tech"],
            }
        ]
        topic_priority = {"llm": 0, "frontier-tech": 1, "uncategorized": 2}
        topic_keywords = {
            "llm": ["large language model", "foundation model", "大模型"],
            "frontier-tech": ["open source", "public sector", "policy"],
        }

        groups = merge_mod.group_by_topics(
            articles,
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertNotIn("llm", groups)
        self.assertIn("frontier-tech", groups)

    def test_group_by_topics_scores_legacy_ai_agent_keyword_alias(self):
        articles = [
            {
                "title": "AI agent framework ships benchmark report",
                "snippet": "A coding agent benchmark for repository workflows.",
                "topics": ["llm", "ai_agent"],
            }
        ]
        topic_priority = {"llm": 0, "ai-agent": 1, "ai_agent": 1}
        topic_keywords = {
            "llm": ["large language model"],
            "ai-agent": ["AI agent", "agent framework", "coding agent"],
        }

        groups = merge_mod.group_by_topics(
            articles,
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertNotIn("llm", groups)
        self.assertIn("ai-agent", groups)
        self.assertNotIn("ai_agent", groups)

    def test_group_by_topics_maps_legacy_builder_topic_to_kol(self):
        articles = [
            {
                "title": "Founder explains product launch lessons",
                "snippet": "A founder shared practical execution notes for an AI startup.",
                "topics": ["builder"],
            }
        ]
        topic_priority = {"kol": 0, "uncategorized": 1}
        topic_keywords = {
            "kol": ["founder", "startup", "execution"],
        }

        groups = merge_mod.group_by_topics(
            articles,
            topic_priority=topic_priority,
            allowed_topics={"kol"},
            topic_keywords=topic_keywords,
        )

        self.assertIn("kol", groups)
        self.assertNotIn("builder", groups)
        self.assertEqual(groups["kol"][0]["primary_topic"], "kol")
        self.assertEqual(groups["kol"][0]["all_topics"], ["kol"])

    def test_group_by_topics_preserves_builder_when_configured(self):
        articles = [
            {
                "title": "Founder explains product launch lessons",
                "snippet": "A founder shared practical execution notes for an AI startup.",
                "topics": ["builder"],
            }
        ]
        topic_priority = {"builder": 0, "uncategorized": 1}
        topic_keywords = {
            "builder": ["founder", "startup", "execution"],
        }

        groups = merge_mod.group_by_topics(
            articles,
            topic_priority=topic_priority,
            allowed_topics={"builder"},
            topic_keywords=topic_keywords,
        )

        self.assertIn("builder", groups)
        self.assertNotIn("kol", groups)
        self.assertEqual(groups["builder"][0]["primary_topic"], "builder")
        self.assertEqual(groups["builder"][0]["all_topics"], ["builder"])

    def test_group_by_topics_uses_builder_keywords_when_routing_to_kol(self):
        articles = [
            {
                "title": "Founder explains product launch lessons",
                "snippet": "A founder shared practical execution notes for an AI startup.",
                "topics": ["builder", "llm"],
            }
        ]
        topic_priority = {"llm": 0, "kol": 1, "uncategorized": 2}
        topic_keywords = {
            "builder": ["founder", "startup", "execution"],
            "llm": ["large language model"],
        }

        groups = merge_mod.group_by_topics(
            articles,
            topic_priority=topic_priority,
            allowed_topics={"kol", "llm"},
            topic_keywords=topic_keywords,
        )

        self.assertIn("kol", groups)
        self.assertNotIn("llm", groups)

    def test_default_topics_keep_agent_benchmark_out_of_llm(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = {
            topic["id"]: topic.get("search", {}).get("must_include", [])
            for topic in topics
        }
        article = {
            "title": "Coding agent benchmark report",
            "snippet": "A coding agent benchmark for repository workflows.",
            "topics": ["llm", "ai-agent"],
        }

        groups = merge_mod.group_by_topics(
            [article],
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertNotIn("llm", groups)
        self.assertIn("ai-agent", groups)

    def test_default_topics_keep_non_llm_model_release_out_of_llm(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = {
            topic["id"]: topic.get("search", {}).get("must_include", [])
            for topic in topics
        }
        article = {
            "title": "AlphaFold model release improves structure prediction",
            "snippet": "A biotech model release for protein structure prediction.",
            "topics": ["llm", "frontier-tech"],
        }

        groups = merge_mod.group_by_topics(
            [article],
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertNotIn("llm", groups)
        self.assertIn("frontier-tech", groups)

    def test_default_topics_keep_gpt_story_in_llm(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = merge_mod.topic_keyword_map(topics)
        article = {
            "title": "OpenAI introduces GPT-5",
            "snippet": "The technology update improves model capability.",
            "topics": ["llm", "frontier-tech"],
        }

        groups = merge_mod.group_by_topics(
            [article],
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertIn("llm", groups)
        self.assertNotIn("frontier-tech", groups)

    def test_default_topics_keep_openai_governance_story_in_industry(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = merge_mod.topic_keyword_map(topics)
        article = {
            "title": "OpenAI changes nonprofit governance structure",
            "snippet": "The company updated its governance structure after industry scrutiny.",
            "topics": ["llm", "frontier-tech"],
        }

        groups = merge_mod.group_by_topics(
            [article],
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertNotIn("llm", groups)
        self.assertIn("frontier-tech", groups)

    def test_default_topics_keep_model_evidence_in_llm_over_industry_terms(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = merge_mod.topic_keyword_map(topics)
        article = {
            "title": "Claude model release adds open source security controls",
            "snippet": "The release improves model behavior for enterprise teams.",
            "topics": ["llm", "frontier-tech"],
        }

        groups = merge_mod.group_by_topics(
            [article],
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertIn("llm", groups)
        self.assertNotIn("frontier-tech", groups)

    def test_default_topics_route_hacker_news_to_hackernews_only(self):
        topics = render_mod.load_topic_definitions(TOPICS_FILE)
        topic_priority = {topic["id"]: index for index, topic in enumerate(topics)}
        topic_keywords = merge_mod.topic_keyword_map(topics)
        article = {
            "title": "Show HN: Useful Tool",
            "link": "https://example.com/tool",
            "hn_url": "https://news.ycombinator.com/item?id=42",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "topics": ["hackernews"],
            "score": 234,
            "num_comments": 56,
            "quality_score": 10,
        }

        groups = merge_mod.group_by_topics(
            [article],
            allowed_topics={topic["id"] for topic in topics},
            topic_priority=topic_priority,
            topic_keywords=topic_keywords,
        )

        self.assertIn("hackernews", groups)
        self.assertNotIn("frontier-tech", groups)
        self.assertEqual(groups["hackernews"][0]["primary_topic"], "hackernews")

    def test_chat_intro_keeps_decimal_version_in_highlight(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "Claude 4.5 improves coding workflows",
                            "link": "https://example.com/claude-4-5",
                            "quality_score": 12,
                            "source_type": "rss",
                            "chat_summary": "Claude 4.5 improves coding workflows. The release focuses on repository tasks.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "llm", "emoji": "🧠", "label": "LLM / 大模型"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("• Claude 4.5 improves coding workflows.", text)
        self.assertNotIn("\n• Claude 4.\n", text)

    def test_chat_intro_keeps_abbreviation_in_highlight(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "frontier-tech": {
                    "articles": [
                        {
                            "title": "U.S. agency backs open-source AI policy",
                            "link": "https://example.com/us-policy",
                            "quality_score": 12,
                            "source_type": "rss",
                            "chat_summary": "U.S. agency backs open-source AI policy. The update affects public-sector technology teams.",
                        }
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "frontier-tech", "emoji": "🔬", "label": "Tech Industry / 产业动态"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("• U.S. agency backs open-source AI policy.", text)
        self.assertNotIn("\n• U.\n", text)

    def test_chat_intro_keeps_titlecase_abbreviation_in_highlight(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "OpenAI Inc. ships new model",
                            "link": "https://example.com/openai-inc-model",
                            "quality_score": 12,
                            "source_type": "rss",
                            "chat_summary": "OpenAI Inc. ships new model. The release targets coding workflows.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "llm", "emoji": "🧠", "label": "LLM / 大模型"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("• OpenAI Inc. ships new model.", text)
        self.assertNotIn("\n• OpenAI Inc.\n", text)

    def test_chat_intro_stops_at_terminal_company_abbreviation(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "OpenAI Inc. update",
                            "link": "https://example.com/openai-inc-update",
                            "quality_score": 12,
                            "source_type": "rss",
                            "chat_summary": "OpenAI Inc. It released a model.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "llm", "emoji": "🧠", "label": "LLM / 大模型"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-05-18",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("• OpenAI Inc.", text)
        self.assertNotIn("• OpenAI Inc. It released a model.", text)

    def test_github_fetch_preserves_prerelease_flag(self):
        class FakeResponse:
            headers = {"ETag": "etag"}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(
                    [
                        {
                            "draft": False,
                            "prerelease": True,
                            "published_at": "2026-05-18T00:00:00Z",
                            "tag_name": "v1.0.0",
                            "html_url": "https://github.com/example/tool/releases/tag/v1.0.0",
                            "body": "Stable-looking prerelease.",
                        }
                    ]
                ).encode("utf-8")

        source = {
            "id": "example-github",
            "name": "Example Tool",
            "repo": "example/tool",
            "priority": False,
            "topics": ["ai-agent"],
        }
        cutoff = fetch_github_mod.parse_github_date("2026-05-17T00:00:00Z")

        with patch.object(fetch_github_mod, "urlopen", return_value=FakeResponse()):
            result = fetch_github_mod.fetch_releases_with_retry(
                source,
                cutoff,
                no_cache=True,
            )

        self.assertEqual(result["articles"][0]["tag_name"], "v1.0.0")
        self.assertTrue(result["articles"][0]["prerelease"])

    def test_chat_non_github_summaries_keep_stable_evidence_phrases(self):
        text = render_daily_chat_digest()

        expected_phrases = [
            "结构化评测",
            "LangGraph 新增 checkpoint",
            "prompt injection",
            "product taste",
            "SWE-bench 分享了一份",
        ]

        for phrase in expected_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_digest_prompt_documents_non_github_summary_contract(self):
        prompt = (ROOT_DIR / "references" / "digest-prompt.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("### Non-GitHub Summary Quality Contract", prompt)
        self.assertIn("references/summarize-tweets.md", prompt)
        self.assertIn("references/summarize-podcast.md", prompt)
        self.assertIn("references/translate.md", prompt)
        self.assertIn("It does not apply to GitHub Releases or GitHub Trending.", prompt)
        self.assertIn("Use a tendency-based structure", prompt)
        self.assertIn("full_text > summary > snippet > title", prompt)
        self.assertIn("Lower-priority fields may provide supplemental context", prompt)
        self.assertIn("do not render engagement metrics", prompt)
        self.assertIn("Metrics may remain in merged JSON for internal ranking", prompt)
        self.assertIn("Discord and email length limits take precedence over sentence-count targets.", prompt)

    def test_templates_document_non_github_summary_contract(self):
        template_paths = [
            ROOT_DIR / "references" / "templates" / "chat.md",
            ROOT_DIR / "references" / "templates" / "discord.md",
            ROOT_DIR / "references" / "templates" / "email.md",
        ]

        for template_path in template_paths:
            with self.subTest(template=template_path.name):
                text = template_path.read_text(encoding="utf-8")
                self.assertIn("Non-GitHub Summary Quality", text)
                self.assertIn("references/summarize-tweets.md", text)
                self.assertIn("references/summarize-podcast.md", text)
                self.assertIn("references/translate.md", text)
                self.assertIn("GitHub Releases and GitHub Trending keep their existing concise style.", text)
                self.assertIn("Use a tendency-based structure", text)
                self.assertIn("full_text > summary > snippet > title", text)
                self.assertIn("Lower-priority fields may provide supplemental context", text)
                self.assertIn("length limits take precedence over sentence-count targets", text)

    def test_chat_digest_filters_linkless_items_and_empty_topics(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "No link item",
                            "quality_score": 18,
                            "source_type": "rss",
                            "chat_summary": "This item must not render because it has no link.",
                        }
                    ]
                },
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Visible agent item",
                            "link": "https://example.com/agent",
                            "quality_score": 10,
                            "source_type": "rss",
                            "chat_summary": "This item remains visible and uses fallback scoring.",
                        }
                    ]
                },
            },
        }
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 🧠 LLM / Large Models", text)
        self.assertNotIn("No link item", text)
        self.assertIn("## 🤖 AI Agent", text)
        self.assertIn(f"1. {render_mod.bold_chat_title_text('Visible agent item')}", text)
        self.assertIn("🔗 https://example.com/agent", text)

    def test_chat_digest_invalid_score_does_not_render_score_prefix(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Invalid score item",
                            "link": "https://example.com/invalid-score",
                            "quality_score": "NaN",
                            "source_type": "rss",
                            "chat_summary": "This item remains visible with fallback scoring.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertIn(f"1. {render_mod.bold_chat_title_text('Invalid score item')}", text)
        self.assertNotRegex(text, r"(?m)^[0-9]+\. \[[0-9]+(?:\.[0-9]+)?/10\] ")

    def test_default_discord_digest_filters_invalid_score_items(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Invalid score should not render in Discord",
                            "link": "https://example.com/invalid-discord",
                            "quality_score": "NaN",
                            "source_type": "rss",
                            "summary": "This item must not render in Discord.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="discord",
        )

        self.assertNotIn("Invalid score should not render in Discord", text)
        self.assertNotIn("https://example.com/invalid-discord", text)

    def test_chat_digest_skips_missing_null_and_empty_scores(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 3},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Missing score item",
                            "link": "https://example.com/missing-score",
                            "source_type": "rss",
                            "chat_summary": "This item must not render.",
                        },
                        {
                            "title": "Null score item",
                            "link": "https://example.com/null-score",
                            "quality_score": None,
                            "source_type": "rss",
                            "chat_summary": "This item must not render.",
                        },
                        {
                            "title": "Empty score item",
                            "link": "https://example.com/empty-score",
                            "quality_score": "",
                            "source_type": "rss",
                            "chat_summary": "This item must not render.",
                        },
                    ]
                }
            },
        }
        topic_defs = [{"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertNotIn("## 🤖 AI Agent", text)
        self.assertNotIn("Missing score item", text)
        self.assertNotIn("Null score item", text)
        self.assertNotIn("Empty score item", text)

    def test_chat_summary_uses_available_material_without_extra_facts(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "llm": {
                    "articles": [
                        {
                            "title": "Snippet-only model note",
                            "link": "https://example.com/snippet",
                            "quality_score": 10,
                            "source_type": "web",
                            "snippet": "Only this snippet is available.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )
        summary = extract_chat_summary(
            text,
            f"1. {render_mod.bold_chat_title_text('Snippet-only model note')}",
        )

        self.assertEqual(summary, "Only this snippet is available.")
        self.assertNotIn("OpenAI", summary)
        self.assertNotIn("Anthropic", summary)
        self.assertNotIn("2026", summary)
        self.assertNotIn("CEO", summary)

    def test_chat_summary_prefers_full_text_over_lower_priority_fields(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "builder": {
                    "articles": [
                        {
                            "title": "Title-level fallback only",
                            "link": "https://example.com/priority",
                            "quality_score": 10,
                            "source_type": "rss",
                            "full_text": "Full text evidence should win.",
                            "summary": "Summary evidence should not win.",
                            "snippet": "Snippet evidence should not win.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "builder", "emoji": "🏗️", "label": "Builder"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )
        summary = extract_chat_summary(
            text,
            f"1. {render_mod.bold_chat_title_text('Title-level fallback only')}",
        )

        self.assertEqual(summary, "Full text evidence should win.")

    def test_chat_podcast_without_transcript_does_not_create_transcript_insight(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "podcast": {
                    "articles": [
                        {
                            "title": "Agent taste preview",
                            "link": "https://example.com/podcast",
                            "quality_score": 12,
                            "source_type": "podcast",
                            "show_name": "Training Data",
                            "transcript_status": "missing",
                            "snippet": "A short preview for an upcoming episode.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "podcast", "emoji": "🎧", "label": "Podcast"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("A short preview for an upcoming episode.", text)

    def test_chat_twitter_metrics_are_not_rendered_without_summary_support(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Agent benchmark post",
                            "link": "https://x.com/example/status/1",
                            "quality_score": 11,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "Example Lab shared a benchmark note.",
                            "metrics": {
                                "impression_count": 12500,
                                "reply_count": 45,
                                "retweet_count": 230,
                                "like_count": 1800,
                            },
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("Example Lab shared a benchmark note.", text)
        topic_text = text.split("## 📢 KOL Updates", 1)[0]
        self.assertNotIn("12.5K", topic_text)
        self.assertNotIn("views", topic_text.lower())

    def test_chat_kol_updates_do_not_render_metrics(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Sparse KOL post",
                            "link": "https://x.com/example/status/2",
                            "quality_score": 11,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "Example Lab shared a sparse benchmark note.",
                            "metrics": {
                                "impression_count": None,
                                "reply_count": "",
                                "retweet_count": "not-a-number",
                                "like_count": 0,
                            },
                        }
                    ]
                }
            },
        }
        topic_defs = []

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        kol_text = text.split("## 📢 KOL Updates", 1)[1]
        self.assertIn("Example Lab shared a sparse benchmark note.", kol_text)
        self.assertNotIn("👁", kol_text)
        self.assertNotIn("💬", kol_text)
        self.assertNotIn("🔁", kol_text)
        self.assertNotIn("❤️", kol_text)
        self.assertNotIn("not-a-number", kol_text)

    def test_discord_kol_updates_do_not_render_metrics(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Invalid metrics container",
                            "link": "https://x.com/example/status/3",
                            "quality_score": 11,
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "Example Lab shared another benchmark note.",
                            "metrics": None,
                        }
                    ]
                }
            },
        }
        topic_defs = []

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
        )

        kol_text = text.split("## 📢 KOL Updates", 1)[1]
        self.assertIn(
            "• **Example Lab** (@example) — Example Lab shared another benchmark note.",
            kol_text,
        )
        self.assertNotIn("👁", kol_text)
        self.assertNotIn("💬", kol_text)
        self.assertNotIn("🔁", kol_text)
        self.assertNotIn("❤️", kol_text)

    def test_chat_kol_updates_skips_empty_section(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "builder": {
                    "articles": [
                        {
                            "title": "Builder article",
                            "link": "https://example.com/builder",
                            "quality_score": 10,
                            "source_type": "rss",
                            "chat_summary": "Builder evidence remains visible.",
                        }
                    ]
                }
            },
        }
        topic_defs = [{"id": "builder", "emoji": "🏗️", "label": "Builder"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 🏗️ Builder", text)
        self.assertNotIn("## 📢 KOL Updates", text)

    def test_daily_digest_structure_contract(self):
        text = render_daily_digest()
        lines = text.splitlines()

        self.assertTrue(text.startswith("# 🚀 Tech Digest - 2026-02-27\n"))
        self.assertIn("## 🧠 LLM / 大模型", text)
        self.assertIn("---\n", text)
        self.assertIn("Powered by OpenClaw", text)

        self.assertNotIn("🔥", text)
        article_lines = [
            line
            for line in lines
            if line.startswith("• ") and not line.startswith("• **")
        ]
        self.assertGreater(len(article_lines), 0)
        for index, line in enumerate(lines):
            if not line.startswith("• "):
                continue
            self.assertNotRegex(line, r"^• 🔥[0-9]+(?:\.[0-9]+)? \| ")
            self.assertLess(index + 1, len(lines))
            self.assertRegex(lines[index + 1], r"^  🔗 https?://.+$")

    def test_update_golden_requires_explicit_environment_flag(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            expected_path = Path(tmp_dir) / "golden.md"
            expected_path.write_text("old\n", encoding="utf-8")

            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(AssertionError):
                    assert_or_update_golden(self, expected_path, "new\n")
                self.assertEqual(expected_path.read_text(encoding="utf-8"), "old\n")

            with patch.dict(os.environ, {"UPDATE_GOLDEN": "1"}, clear=True):
                assert_or_update_golden(self, expected_path, "new\n")
                self.assertEqual(expected_path.read_text(encoding="utf-8"), "new\n")

    def test_render_digest_uses_current_discord_structure(self):
        data = load_acceptance_fixture()
        topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
        )

        self.assertIn("# 🚀 Tech Digest - 2026-02-27", text)
        self.assertIn("## 🧠 LLM / 大模型", text)
        self.assertIn("• OpenAI ships structured agent evaluation suite", text)
        self.assertNotRegex(text, r"(?m)^• 🔥[0-9]+(?:\.[0-9]+)? \| ")
        self.assertIn("  🔗 https://openai.com/research/agent-evals", text)
        self.assertIn("  *[3 sources]*", text)
        self.assertNotIn("Low scoring model rumor should not render", text)
        self.assertNotIn("## 📢 KOL Updates", text)
        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("## 🐙 GitHub Trending", text)
        self.assertNotIn("## 📝 Blog Picks", text)
        self.assertNotIn("## 🎙️ Podcast Remix", text)
        self.assertIn(
            "📊 Data Sources: RSS 3 | Twitter 1 | Reddit 1 | Web 1 | GitHub 1 releases + 1 trending | Podcast 1 episodes | Dedup: 9 articles",
            text,
        )
        self.assertTrue(text.endswith("\n"))

    def test_discord_fixed_sections_render_unseen_items(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 5},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Unseen KOL update",
                            "link": "https://x.com/example/status/unseen",
                            "source_type": "twitter",
                            "display_name": "Example Lab",
                            "handle": "example",
                            "summary": "Example Lab shared an unseen update.",
                            "metrics": {
                                "impression_count": 1200,
                                "reply_count": 3,
                                "retweet_count": 4,
                                "like_count": 50,
                            },
                        },
                        {
                            "title": "Example Tool v1.0.0",
                            "link": "https://github.com/example/tool/releases/tag/v1.0.0",
                            "source_type": "github",
                            "repo": "example/tool",
                            "tag_name": "v1.0.0",
                            "summary": "The release ships a stable API.",
                        },
                        {
                            "title": "example/trending-tool",
                            "link": "https://github.com/example/trending-tool",
                            "source_type": "github_trending",
                            "repo": "example/trending-tool",
                            "stars": 2500,
                            "daily_stars_est": 125,
                            "language": "TypeScript",
                            "description": "A trending tool for builders.",
                        },
                        {
                            "title": "Unseen blog pick",
                            "link": "https://example.com/unseen-blog",
                            "source_type": "rss",
                            "is_blog_pick": True,
                            "author": "Example Author",
                            "full_text": "A detailed unseen blog post.",
                        },
                        {
                            "title": "Unseen podcast episode",
                            "link": "https://www.youtube.com/watch?v=unseenpodcast",
                            "source_type": "podcast",
                            "transcript_status": "ok",
                            "transcript": "Host | 00:00 - 00:05 This is an unseen podcast.",
                            "show_name": "Example Show",
                            "snippet": "An unseen podcast episode.",
                        },
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertIn("## 📢 KOL Updates", text)
        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("## 🐙 GitHub Trending", text)
        self.assertIn("## 📝 Blog Picks", text)
        self.assertIn("## 🎙️ Podcast Remix", text)
        self.assertEqual(text.count("https://x.com/example/status/unseen"), 1)
        self.assertEqual(
            text.count("https://github.com/example/tool/releases/tag/v1.0.0"),
            1,
        )
        self.assertEqual(text.count("https://github.com/example/trending-tool"), 1)
        self.assertEqual(text.count("https://example.com/unseen-blog"), 1)
        self.assertEqual(
            text.count("https://www.youtube.com/watch?v=unseenpodcast"),
            1,
        )

    def test_discord_podcast_remix_renders_metadata_only_episode(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Agent taste preview",
                            "link": "https://example.com/podcast",
                            "source_type": "podcast",
                            "show_name": "Training Data",
                            "transcript_status": "missing",
                            "snippet": "A short preview for an upcoming episode about agent product taste.",
                            "quality_score": 12,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("## 🎙️ Podcast Remix", text)
        self.assertIn("• **Agent taste preview** — Training Data", text)
        self.assertIn(
            "A short preview for an upcoming episode about agent product taste.",
            text,
        )
        self.assertNotIn("Quote:", text)

    def test_discord_podcast_remix_renders_clean_transcript_quote(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Why agents need product taste",
                            "link": "https://example.com/podcast-transcript",
                            "source_type": "podcast",
                            "show_name": "Training Data",
                            "transcript_status": "ok",
                            "transcript": "Host | 00:00 - 00:05 Taste is the difference between a demo and a daily tool.",
                            "summary": "The episode explains why product taste, evaluation loops, and reliability decide whether agent tools become daily workflow infrastructure.",
                            "quality_score": 12,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("• **Why agents need product taste** — Training Data", text)
        self.assertIn(
            "The episode explains why product taste, evaluation loops, and reliability decide whether agent tools become daily workflow infrastructure.",
            text,
        )
        self.assertIn(
            'Quote: "Taste is the difference between a demo and a daily tool."',
            text,
        )
        self.assertNotIn("Host | 00:00", text)

    def test_podcast_remix_uses_description_metadata_fallback(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Metadata-only episode",
                            "link": "https://example.com/podcast-description",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "missing",
                            "description": "Description-only context should remain visible.",
                            "quality_score": 12,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("Description-only context should remain visible.", text)
        self.assertNotIn("has no available transcript", text)

    def test_discord_podcast_remix_prefers_standard_summary_over_chat_summary(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Localized summary episode",
                            "link": "https://example.com/podcast-localized",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "missing",
                            "chat_summary": "这是一段只适合 chat 的摘要。",
                            "summary": "This summary is intended for default digest output.",
                            "quality_score": 12,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("This summary is intended for default digest output.", text)
        self.assertNotIn("这是一段只适合 chat 的摘要", text)

    def test_podcast_quote_skips_empty_cleaned_transcript_lines(self):
        article = {
            "transcript_status": "ok",
            "transcript": (
                "Host | 00:00 - 00:05\n"
                "Guest | 00:05 - 00:10 Evaluation loops create product taste."
            ),
        }

        self.assertEqual(
            render_mod.podcast_quote(article),
            "Evaluation loops create product taste.",
        )

    def test_chat_podcast_remix_renders_transcript_quote(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Transcript-only episode",
                            "link": "https://example.com/podcast-chat-quote",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "ok",
                            "transcript": "Host | 00:00 - 00:05 Concrete evidence matters.",
                            "quality_score": 12,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
            template="chat",
        )

        self.assertIn('Quote: "Concrete evidence matters."', text)

    def test_podcast_remix_prioritizes_transcript_backed_episodes(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 4},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": f"Metadata episode {index}",
                            "link": f"https://example.com/metadata-podcast-{index}",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "missing",
                            "summary": f"Metadata summary {index}.",
                            "quality_score": 100 - index,
                        }
                        for index in range(3)
                    ]
                    + [
                        {
                            "title": "Transcript episode",
                            "link": "https://example.com/transcript-podcast",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "ok",
                            "transcript": "Guest | 00:00 - 00:05 Transcript evidence.",
                            "quality_score": 1,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("**Transcript episode**", text)
        self.assertIn('Quote: "Transcript evidence."', text)
        self.assertNotIn("**Metadata episode 2**", text)

    def test_podcast_remix_backfills_after_dedupe(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 5},
            "topics": {
                "ai-agent": {
                    "articles": [
                        {
                            "title": "Topic already used this podcast URL",
                            "link": "https://example.com/podcast-0",
                            "summary": "Topic summary.",
                            "quality_score": 20,
                        }
                    ]
                },
                "supplemental": {
                    "articles": [
                        {
                            "title": f"Podcast {index}",
                            "link": f"https://example.com/podcast-{index}",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "missing",
                            "summary": f"Podcast summary {index}.",
                            "quality_score": 10 - index,
                        }
                        for index in range(4)
                    ]
                },
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[{"id": "ai-agent", "label": "AI Agent", "emoji": "🤖"}],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("**Podcast 1**", text)
        self.assertIn("**Podcast 2**", text)
        self.assertIn("**Podcast 3**", text)
        self.assertNotIn("**Podcast 0**", text)

    def test_podcast_alias_candidates_include_full_remix_candidate_graph(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 4},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": f"Podcast {index}",
                            "link": f"https://example.com/podcast-{index}",
                            "source_type": "podcast",
                            "show_name": "Example Show",
                            "transcript_status": "missing",
                            "summary": f"Podcast summary {index}.",
                            "quality_score": 10 - index,
                        }
                        for index in range(4)
                    ]
                }
            },
        }

        candidates = render_mod.visible_alias_candidates(
            data,
            topic_defs=[],
            template="chat",
        )

        podcast_links = [
            article["link"]
            for article in candidates
            if article.get("source_type") == "podcast"
        ]
        self.assertEqual(
            podcast_links,
            [
                "https://example.com/podcast-0",
                "https://example.com/podcast-1",
                "https://example.com/podcast-2",
                "https://example.com/podcast-3",
            ],
        )

    def test_hacker_news_top_renders_top_ten_plus_ai_related_top_twenty(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 12},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": f"HN story {index}",
                            "link": f"https://example.com/story-{index}",
                            "hn_url": f"https://news.ycombinator.com/item?id={index}",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": index,
                            "score": 100 - index,
                            "num_comments": index,
                            "summary": f"Summary {index}.",
                            "quality_score": 10,
                        }
                        for index in range(1, 12)
                    ]
                    + [
                        {
                            "title": "LLM inference systems story",
                            "link": "https://example.com/llm-inference",
                            "hn_url": "https://news.ycombinator.com/item?id=18",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 18,
                            "score": 25,
                            "num_comments": 7,
                            "summary": "A detailed look at LLM inference systems.",
                            "quality_score": 10,
                        }
                    ],
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("## 📰 Hacker News Top", text)
        self.assertIn("1. **HN story 1** — 99↑ · 1 comments", text)
        self.assertIn("**HN story 10**", text)
        self.assertNotIn("**HN story 11**", text)
        self.assertIn("**LLM inference systems story**", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=18", text)
        self.assertIn("↗ https://example.com/llm-inference", text)

    def test_hacker_news_top_selects_default_items_by_score_not_rank(self):
        articles = [
            {
                "title": "High score later HN story",
                "link": "https://example.com/high-score",
                "hn_url": "https://news.ycombinator.com/item?id=999",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": 19,
                "score": 500,
                "num_comments": 12,
                "summary": "A high scoring story outside the old rank gate.",
                "quality_score": 10,
            },
            {
                "title": "Low score frontpage HN story",
                "link": "https://example.com/low-score",
                "hn_url": "https://news.ycombinator.com/item?id=1",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": 1,
                "score": 1,
                "num_comments": 1,
                "summary": "A low scoring story with an early feed position.",
                "quality_score": 10,
            },
        ]
        articles.extend(
            {
                "title": f"Scored HN story {index}",
                "link": f"https://example.com/scored-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(2, 11)
        )
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"supplemental": {"articles": articles}},
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("**High score later HN story**", text)
        self.assertNotIn("**Low score frontpage HN story**", text)

    def test_hacker_news_ai_related_extra_uses_token_boundaries(self):
        articles = [
            {
                "title": f"Top HN story {index}",
                "link": f"https://example.com/top-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "score": 1000 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 11)
        ]
        articles.extend(
            [
                {
                    "title": "Paid XML email tooling",
                    "link": "https://example.com/false-positive",
                    "hn_url": "https://news.ycombinator.com/item?id=101",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 18,
                    "score": 900,
                    "num_comments": 11,
                    "summary": "Text that should not match short tokens.",
                    "quality_score": 10,
                },
                {
                    "title": "LLM inference systems story",
                    "link": "https://example.com/llm-extra",
                    "hn_url": "https://news.ycombinator.com/item?id=102",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 19,
                    "score": 899,
                    "num_comments": 12,
                    "summary": "A real AI systems discussion.",
                    "quality_score": 10,
                },
            ]
        )
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"supplemental": {"articles": articles}},
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertNotIn("**Paid XML email tooling**", text)
        self.assertIn("**LLM inference systems story**", text)

    def test_hacker_news_ai_related_extra_matches_hyphenated_phrases(self):
        article = {"title": "Machine-learning inference systems"}

        self.assertTrue(render_mod.is_ai_related_hacker_news_article(article))

    def test_hacker_news_ai_related_extra_uses_title_only_keywords(self):
        articles = [
            {
                "title": f"Top HN story {index}",
                "link": f"https://example.com/top-title-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={200 + index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "score": 1000 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 11)
        ]
        articles.extend(
            [
                {
                    "title": "Distributed queue incident report",
                    "link": "https://example.com/non-ai-summary",
                    "hn_url": "https://news.ycombinator.com/item?id=301",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 18,
                    "score": 900,
                    "num_comments": 11,
                    "summary": "The post mentions an AI model in background context.",
                    "quality_score": 10,
                },
                {
                    "title": "Machine learning inference systems",
                    "link": "https://example.com/title-ai-extra",
                    "hn_url": "https://news.ycombinator.com/item?id=302",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 19,
                    "score": 899,
                    "num_comments": 12,
                    "summary": "A systems discussion.",
                    "quality_score": 10,
                },
            ]
        )
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"supplemental": {"articles": articles}},
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertNotIn("**Distributed queue incident report**", text)
        self.assertIn("**Machine learning inference systems**", text)

    def test_hacker_news_ai_related_extra_requires_rank_eleven_to_twenty(self):
        articles = [
            {
                "title": f"Top HN story {index}",
                "link": f"https://example.com/ranked-top-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={400 + index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 1000 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 11)
        ]
        articles.extend(
            [
                {
                    "title": "AI story with rank ten",
                    "link": "https://example.com/ai-rank-10",
                    "hn_url": "https://news.ycombinator.com/item?id=501",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 10,
                    "score": 10,
                    "num_comments": 10,
                    "summary": "Below the score top ten but not an extra rank.",
                    "quality_score": 10,
                },
                {
                    "title": "AI story with rank eighteen",
                    "link": "https://example.com/ai-rank-18",
                    "hn_url": "https://news.ycombinator.com/item?id=502",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 18,
                    "score": 9,
                    "num_comments": 9,
                    "summary": "This qualifies for the title keyword exception.",
                    "quality_score": 10,
                },
                {
                    "title": "AI story with rank twenty one",
                    "link": "https://example.com/ai-rank-21",
                    "hn_url": "https://news.ycombinator.com/item?id=503",
                    "source_type": "rss",
                    "source_name": "Hacker News Frontpage",
                    "source_id": "hn-rss",
                    "hn_rank": 21,
                    "score": 8,
                    "num_comments": 8,
                    "summary": "This is outside the exception rank window.",
                    "quality_score": 10,
                },
            ]
        )
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"supplemental": {"articles": articles}},
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertNotIn("**AI story with rank ten**", text)
        self.assertIn("**AI story with rank eighteen**", text)
        self.assertNotIn("**AI story with rank twenty one**", text)

    def test_hacker_news_top_excludes_merged_story_without_hn_metadata(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Merged HN story",
                            "link": "https://example.com/merged-hn",
                            "source_type": "article",
                            "source_name": "Example",
                            "all_sources": ["Example", "Hacker News Frontpage"],
                            "score": 120,
                            "num_comments": 18,
                            "summary": "A merged story retained from Hacker News.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertNotIn("## 📰 Hacker News Top", text)
        self.assertNotIn("**Merged HN story**", text)

    def test_hacker_news_top_excludes_direct_story_without_metrics(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "HN story without metrics",
                            "link": "https://example.com/no-metrics",
                            "hn_url": "https://news.ycombinator.com/item?id=601",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "summary": "Missing score and comments metadata.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertNotIn("## 📰 Hacker News Top", text)
        self.assertNotIn("0↑ · 0 comments", text)

    def test_hacker_news_top_includes_merged_story_with_hn_metadata(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Merged HN story",
                            "link": "https://example.com/merged-hn",
                            "source_type": "article",
                            "source_name": "Example",
                            "all_sources": ["Example", "Hacker News Frontpage"],
                            "score": 1,
                            "num_comments": 2,
                            "hn_score": 120,
                            "hn_comments": 18,
                            "summary": "A merged story retained from Hacker News.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("## 📰 Hacker News Top", text)
        self.assertIn("**Merged HN story** — 120↑ · 18 comments", text)
        self.assertEqual(text.count("https://example.com/merged-hn"), 1)

    def test_chat_hacker_news_top_uses_fixed_numbered_shape(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "Show HN: Useful Tool",
                            "link": "https://example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "A tool builders are discussing.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
            template="chat",
        )

        self.assertIn("## 📰 Hacker News Top / 热榜", text)
        self.assertIn(
            f"1. {render_mod.bold_chat_title_text('Show HN: Useful Tool')}",
            text,
        )
        self.assertIn("234↑ · 56 comments · A tool builders are discussing.", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=42", text)
        self.assertIn("↗ https://example.com/tool", text)

    def test_chat_legacy_hacker_news_fallback_skips_generic_topic(self):
        hn_title = "Legacy HN Infrastructure Story"
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "frontier-tech": {
                    "articles": [
                        {
                            "title": "Regular Frontier Tech Story",
                            "link": "https://example.com/frontier-tech",
                            "summary": "A regular topic story.",
                            "quality_score": 10,
                        },
                        {
                            "title": hn_title,
                            "link": "https://example.com/legacy-hn",
                            "hn_url": "https://news.ycombinator.com/item?id=4242",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 321,
                            "num_comments": 45,
                            "summary": "Legacy HN story from an old merged topic.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "frontier-tech", "emoji": "🏭", "label": "Tech Industry / 产业动态"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.0",
            template="chat",
        )

        topic_section = text.split("## 🏭 Tech Industry / 产业动态", 1)[1].split(
            "## 📰 Hacker News Top / 热榜",
            1,
        )[0]

        self.assertIn("## 🏭 Tech Industry / 产业动态", text)
        self.assertIn("https://example.com/frontier-tech", topic_section)
        self.assertNotIn(render_mod.bold_chat_title_text(hn_title), topic_section)
        self.assertIn("## 📰 Hacker News Top / 热榜", text)
        self.assertIn(f"1. {render_mod.bold_chat_title_text(hn_title)}", text)
        self.assertIn(
            "321↑ · 45 comments · Legacy HN story from an old merged topic.",
            text,
        )
        self.assertIn("🔗 https://news.ycombinator.com/item?id=4242", text)
        self.assertIn("↗ https://example.com/legacy-hn", text)

    def test_chat_hackernews_topic_renders_hn_metadata_and_links(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "Show HN: Useful Tool",
                            "link": "https://example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "A tool builders are discussing.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertIn(
            f"1. {render_mod.bold_chat_title_text('Show HN: Useful Tool')}",
            text,
        )
        self.assertIn("234↑ · 56 comments · A tool builders are discussing.", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=42", text)
        self.assertIn("↗ https://example.com/tool", text)
        self.assertNotIn("## 📰 Hacker News Top / 热榜", text)

    def test_chat_hackernews_topic_requires_hn_discussion_url(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "HN metadata without discussion URL",
                            "link": "https://example.com/story",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "HN discussion URL is missing.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertNotIn("## 📰 Hacker News / 热榜", text)
        self.assertIn("## 📰 Hacker News Top / 热榜", text)
        self.assertIn("🔗 https://example.com/story", text)

    def test_chat_hackernews_topic_skips_malformed_articles(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 4},
            "topics": {
                "hackernews": {
                    "articles": [
                        None,
                        "malformed",
                        ["malformed"],
                        {
                            "title": "Show HN: Useful Tool",
                            "link": "https://example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "A tool builders are discussing.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=42", text)
        self.assertNotIn("malformed", text)

    def test_chat_hackernews_topic_suppresses_fixed_section_with_matching_id(self):
        articles = [
            {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 12)
        ]
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"HackerNews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "HackerNews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertIn(
            f"10. {render_mod.bold_chat_title_text('HN ranked story 10')}",
            text,
        )
        self.assertNotIn("## 📰 Hacker News Top / 热榜", text)
        self.assertNotIn("HN ranked story 11", text)

    def test_chat_intro_uses_hackernews_topic_filtering(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "Ghost HN highlight",
                            "link": "https://example.com/ghost",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 999,
                            "num_comments": 100,
                            "summary": "Ghost story should not appear.",
                            "quality_score": 100,
                        },
                        {
                            "title": "Renderable HN story",
                            "link": "https://example.com/renderable",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 2,
                            "score": 10,
                            "num_comments": 5,
                            "summary": "Renderable discussion appears.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("今日看点", text)
        self.assertIn("Renderable discussion appears.", text)
        self.assertNotIn("Ghost story should not appear.", text)
        self.assertNotIn("Ghost HN highlight", text)

    def test_chat_keeps_non_hn_primary_article_with_hn_all_source(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "frontier-tech": {
                    "articles": [
                        {
                            "title": "Primary source story also discussed on HN",
                            "link": "https://example.com/primary",
                            "source_type": "rss",
                            "source_name": "Example Primary Source",
                            "all_sources": [
                                "Example Primary Source",
                                "Hacker News Frontpage",
                            ],
                            "summary": "The primary source should remain visible.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }
        topic_defs = [
            {
                "id": "frontier-tech",
                "emoji": "🔬",
                "label": "Tech Industry / 产业动态",
            },
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"},
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("## 🔬 Tech Industry / 产业动态", text)
        self.assertIn(
            render_mod.bold_chat_title_text(
                "Primary source story also discussed on HN"
            ),
            text,
        )
        self.assertIn("🔗 https://example.com/primary", text)
        self.assertNotIn("## 📰 Hacker News / 热榜", text)
        self.assertNotIn("## 📰 Hacker News Top / 热榜", text)

    def test_chat_hackernews_topic_renders_ranked_top_ten_without_duplicates(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 12)
        }
        duplicate_story = {
            "title": "HN ranked story 3",
            "link": "https://mirror.example.com/story-3",
            "hn_url": "https://news.ycombinator.com/item?id=3",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "hn_rank": 3,
            "score": 3,
            "num_comments": 3,
            "summary": "Duplicate story.",
            "quality_score": 10,
        }
        articles = [
            ranked_articles[index]
            for index in [5, 1, 3, 2, 4, 6, 7, 8, 9]
        ]
        articles.extend([duplicate_story, ranked_articles[10], ranked_articles[11]])
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"hackernews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        story_1_line = f"1. {render_mod.bold_chat_title_text('HN ranked story 1')}"
        story_2_line = f"2. {render_mod.bold_chat_title_text('HN ranked story 2')}"
        story_3_line = f"3. {render_mod.bold_chat_title_text('HN ranked story 3')}"
        story_10_line = f"10. {render_mod.bold_chat_title_text('HN ranked story 10')}"
        story_11_line = f"11. {render_mod.bold_chat_title_text('HN ranked story 11')}"

        self.assertIn(story_1_line, text)
        self.assertIn(story_10_line, text)
        self.assertNotIn(story_11_line, text)
        self.assertLess(text.find(story_1_line), text.find(story_2_line))
        self.assertLess(text.find(story_2_line), text.find(story_3_line))
        self.assertEqual(text.count(story_3_line), 1)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("https://mirror.example.com/story-3", text)

    def test_chat_hackernews_topic_sorts_unranked_after_ranked_by_score_title(self):
        articles = [
            {
                "title": "Unranked lower score",
                "link": "https://example.com/unranked-lower",
                "hn_url": "https://news.ycombinator.com/item?id=101",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "score": 20,
                "num_comments": 2,
                "summary": "Lower score unranked story.",
                "quality_score": 10,
            },
            {
                "title": "Ranked lower score",
                "link": "https://example.com/ranked",
                "hn_url": "https://news.ycombinator.com/item?id=102",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": 1,
                "score": 1,
                "num_comments": 1,
                "summary": "Ranked story.",
                "quality_score": 10,
            },
            {
                "title": "Unranked higher score",
                "link": "https://example.com/unranked-higher",
                "hn_url": "https://news.ycombinator.com/item?id=103",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "score": 99,
                "num_comments": 3,
                "summary": "Higher score unranked story.",
                "quality_score": 10,
            },
        ]
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"hackernews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        ranked_line = f"1. {render_mod.bold_chat_title_text('Ranked lower score')}"
        unranked_high_line = (
            f"2. {render_mod.bold_chat_title_text('Unranked higher score')}"
        )
        unranked_low_line = (
            f"3. {render_mod.bold_chat_title_text('Unranked lower score')}"
        )

        self.assertIn(ranked_line, text)
        self.assertIn(unranked_high_line, text)
        self.assertIn(unranked_low_line, text)
        self.assertLess(text.find(ranked_line), text.find(unranked_high_line))
        self.assertLess(text.find(unranked_high_line), text.find(unranked_low_line))

    def test_chat_hackernews_topic_dedupes_by_hn_url_before_limiting(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in list(range(1, 10)) + [11]
        }
        duplicate_story = {
            "title": "Different coverage of story 3",
            "link": "https://mirror.example.com/different-story-3",
            "hn_url": "https://news.ycombinator.com/item?id=3",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "hn_rank": 3,
            "score": 96,
            "num_comments": 3,
            "summary": "Duplicate story with a different title.",
            "quality_score": 10,
        }
        articles = [
            ranked_articles[index]
            for index in [5, 1, 3, 2, 4, 6, 7, 8, 9]
        ]
        articles.extend([duplicate_story, ranked_articles[11]])
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"hackernews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        story_11_line = f"10. {render_mod.bold_chat_title_text('HN ranked story 11')}"

        self.assertIn(story_11_line, text)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("Different coverage of story 3", text)
        self.assertNotIn("https://mirror.example.com/different-story-3", text)

    def test_chat_hackernews_topic_suppresses_fixed_hn_section(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "HN ranked story 1",
                            "link": "https://example.com/story-1",
                            "hn_url": "https://news.ycombinator.com/item?id=1",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 100,
                            "num_comments": 10,
                            "summary": "Top story.",
                            "quality_score": 10,
                        },
                        {
                            "title": "HN ranked story 11",
                            "link": "https://example.com/story-11",
                            "hn_url": "https://news.ycombinator.com/item?id=11",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 11,
                            "score": 90,
                            "num_comments": 5,
                            "summary": "Fixed fallback candidate.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
            template="chat",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertNotIn("## 📰 Hacker News Top / 热榜", text)

    def test_discord_hackernews_topic_suppresses_fixed_hn_duplicate_by_hn_url(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "Show HN: Useful Tool",
                            "link": "https://example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "A tool builders are discussing.",
                            "quality_score": 10,
                        }
                    ]
                },
                "supplemental": {
                    "articles": [
                        {
                            "title": "Different mirror coverage",
                            "link": "https://mirror.example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 233,
                            "num_comments": 56,
                            "summary": "Same discussion via another link.",
                            "quality_score": 10,
                        }
                    ]
                },
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        self.assertIn("• Show HN: Useful Tool — 234↑ · 56 comments", text)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=42"), 1)
        self.assertNotIn("Different mirror coverage", text)
        self.assertNotIn("https://mirror.example.com/tool", text)
        self.assertNotIn("## 📰 Hacker News Top", text)

    def test_discord_hackernews_topic_suppresses_fixed_hn_section(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "HN ranked story 1",
                            "link": "https://example.com/story-1",
                            "hn_url": "https://news.ycombinator.com/item?id=1",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 100,
                            "num_comments": 10,
                            "summary": "Top story.",
                            "quality_score": 10,
                        },
                        {
                            "title": "HN ranked story 11",
                            "link": "https://example.com/story-11",
                            "hn_url": "https://news.ycombinator.com/item?id=11",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 11,
                            "score": 90,
                            "num_comments": 5,
                            "summary": "Fixed fallback candidate.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertNotIn("## 📰 Hacker News Top", text)

    def test_discord_hackernews_topic_ignores_generic_hn_duplicate_by_hn_url(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 12)
        }
        prior_visible_duplicate = {
            "title": "Prior coverage of story 3",
            "link": "https://supplemental.example.com/story-3",
            "hn_url": "https://news.ycombinator.com/item?id=3",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "hn_rank": 3,
            "score": 97,
            "num_comments": 3,
            "summary": "Already visible elsewhere.",
            "quality_score": 100,
        }
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 12},
            "topics": {
                "supplemental": {"articles": [prior_visible_duplicate]},
                "hackernews": {
                    "articles": [
                        ranked_articles[index]
                        for index in [5, 1, 3, 2, 4, 6, 7, 8, 9, 10, 11]
                    ]
                },
            },
        }
        topic_defs = [
            {"id": "supplemental", "emoji": "🧩", "label": "Supplemental"},
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"},
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        story_10_line = "• HN ranked story 10 — 90↑ · 10 comments"
        story_3_line = "• HN ranked story 3 — 97↑ · 3 comments"
        story_11_line = "• HN ranked story 11 — 89↑ · 11 comments"

        self.assertNotIn("• Prior coverage of story 3", text)
        self.assertNotIn("https://supplemental.example.com/story-3", text)
        self.assertIn(story_3_line, text)
        self.assertIn(story_10_line, text)
        self.assertNotIn(story_11_line, text)
        self.assertIn("https://example.com/story-3", text)

    def test_discord_hackernews_topic_survives_filtered_alias_chain(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 3},
            "topics": {
                "frontier-tech": {
                    "articles": [
                        {
                            "title": "Shared launch coverage",
                            "link": "https://example.com/non-hn",
                            "summary": "Ordinary coverage should remain visible.",
                            "quality_score": 100,
                        },
                        {
                            "title": "Shared launch coverage",
                            "link": "https://example.com/legacy-hn",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "Filtered legacy HN coverage.",
                            "quality_score": 99,
                        },
                    ]
                },
                "hackernews": {
                    "articles": [
                        {
                            "title": "Show HN: Shared Launch",
                            "link": "https://example.com/hn-topic",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "The real HN topic story should render.",
                            "quality_score": 10,
                        }
                    ]
                },
            },
        }
        topic_defs = [
            {"id": "frontier-tech", "emoji": "🏭", "label": "Tech Industry"},
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"},
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        self.assertIn("• Shared launch coverage", text)
        self.assertNotIn("Filtered legacy HN coverage.", text)
        self.assertIn("• Show HN: Shared Launch — 234↑ · 56 comments", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=42", text)
        self.assertIn("↗ https://example.com/hn-topic", text)

    def test_discord_hackernews_topic_backfills_when_prior_link_is_hn_url(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 12)
        }
        prior_visible_discussion = {
            "title": "Prior discussion link for story 3",
            "link": "https://news.ycombinator.com/item?id=3",
            "source_type": "web",
            "summary": "Already visible as an ordinary link.",
            "quality_score": 100,
        }
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 12},
            "topics": {
                "supplemental": {"articles": [prior_visible_discussion]},
                "hackernews": {
                    "articles": [
                        ranked_articles[index]
                        for index in [5, 1, 3, 2, 4, 6, 7, 8, 9, 10, 11]
                    ]
                },
            },
        }
        topic_defs = [
            {"id": "supplemental", "emoji": "🧩", "label": "Supplemental"},
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"},
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        story_10_line = "• HN ranked story 10 — 90↑ · 10 comments"
        story_11_line = "• HN ranked story 11 — 89↑ · 11 comments"

        self.assertIn("• Prior discussion link for story 3", text)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("• HN ranked story 3 — 97↑ · 3 comments", text)
        self.assertIn(story_10_line, text)
        self.assertIn(story_11_line, text)
        self.assertNotIn("https://example.com/story-3", text)

    def test_discord_hackernews_topic_renders_hn_metadata_and_links(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "hackernews": {
                    "articles": [
                        {
                            "title": "Show HN: Useful Tool",
                            "link": "https://example.com/tool",
                            "hn_url": "https://news.ycombinator.com/item?id=42",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 234,
                            "num_comments": 56,
                            "summary": "A tool builders are discussing.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        self.assertIn("## 📰 Hacker News / 热榜", text)
        self.assertIn("• Show HN: Useful Tool — 234↑ · 56 comments", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=42", text)
        self.assertIn("↗ https://example.com/tool", text)
        self.assertNotIn("## 📰 Hacker News Top", text)

    def test_discord_legacy_hacker_news_fallback_skips_generic_topic(self):
        hn_title = "Legacy HN Infrastructure Story"
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 2},
            "topics": {
                "frontier-tech": {
                    "articles": [
                        {
                            "title": "Regular Frontier Tech Story",
                            "link": "https://example.com/frontier-tech",
                            "summary": "A regular topic story.",
                            "quality_score": 10,
                        },
                        {
                            "title": hn_title,
                            "link": "https://example.com/legacy-hn",
                            "hn_url": "https://news.ycombinator.com/item?id=4242",
                            "source_type": "rss",
                            "source_name": "Hacker News Frontpage",
                            "source_id": "hn-rss",
                            "hn_rank": 1,
                            "score": 321,
                            "num_comments": 45,
                            "summary": "Legacy HN story from an old merged topic.",
                            "quality_score": 10,
                        },
                    ]
                }
            },
        }
        topic_defs = [
            {"id": "frontier-tech", "emoji": "🏭", "label": "Tech Industry / 产业动态"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.0",
        )

        topic_section = text.split("## 🏭 Tech Industry / 产业动态", 1)[1].split(
            "## 📰 Hacker News Top",
            1,
        )[0]

        self.assertIn("## 🏭 Tech Industry / 产业动态", text)
        self.assertIn("Regular Frontier Tech Story", topic_section)
        self.assertNotIn(hn_title, topic_section)
        self.assertIn("## 📰 Hacker News Top", text)
        self.assertIn(f"1. **{hn_title}** — 321↑ · 45 comments", text)
        self.assertIn("Legacy HN story from an old merged topic.", text)
        self.assertIn("🔗 https://news.ycombinator.com/item?id=4242", text)
        self.assertIn("↗ https://example.com/legacy-hn", text)

    def test_discord_hackernews_topic_renders_ranked_top_ten_without_duplicates(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in range(1, 12)
        }
        duplicate_story = {
            "title": "HN ranked story 3",
            "link": "https://mirror.example.com/story-3",
            "hn_url": "https://news.ycombinator.com/item?id=3",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "hn_rank": 3,
            "score": 97,
            "num_comments": 3,
            "summary": "Duplicate story.",
            "quality_score": 10,
        }
        articles = [
            ranked_articles[index]
            for index in [5, 1, 3, 2, 4, 6, 7, 8, 9]
        ]
        articles.extend([duplicate_story, ranked_articles[10], ranked_articles[11]])
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"hackernews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        story_1_line = "• HN ranked story 1 — 99↑ · 1 comments"
        story_2_line = "• HN ranked story 2 — 98↑ · 2 comments"
        story_3_line = "• HN ranked story 3 — 97↑ · 3 comments"
        story_10_line = "• HN ranked story 10 — 90↑ · 10 comments"
        story_11_line = "• HN ranked story 11 — 89↑ · 11 comments"

        self.assertIn(story_1_line, text)
        self.assertIn(story_10_line, text)
        self.assertNotIn(story_11_line, text)
        self.assertLess(text.find(story_1_line), text.find(story_2_line))
        self.assertLess(text.find(story_2_line), text.find(story_3_line))
        self.assertEqual(text.count(story_3_line), 1)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("https://mirror.example.com/story-3", text)

    def test_discord_hackernews_topic_dedupes_by_hn_url_before_limiting(self):
        ranked_articles = {
            index: {
                "title": f"HN ranked story {index}",
                "link": f"https://example.com/story-{index}",
                "hn_url": f"https://news.ycombinator.com/item?id={index}",
                "source_type": "rss",
                "source_name": "Hacker News Frontpage",
                "source_id": "hn-rss",
                "hn_rank": index,
                "score": 100 - index,
                "num_comments": index,
                "summary": f"Summary {index}.",
                "quality_score": 10,
            }
            for index in list(range(1, 10)) + [11]
        }
        duplicate_story = {
            "title": "Different coverage of story 3",
            "link": "https://mirror.example.com/different-story-3",
            "hn_url": "https://news.ycombinator.com/item?id=3",
            "source_type": "rss",
            "source_name": "Hacker News Frontpage",
            "source_id": "hn-rss",
            "hn_rank": 3,
            "score": 96,
            "num_comments": 3,
            "summary": "Duplicate story with a different title.",
            "quality_score": 10,
        }
        articles = [
            ranked_articles[index]
            for index in [5, 1, 3, 2, 4, 6, 7, 8, 9]
        ]
        articles.extend([duplicate_story, ranked_articles[11]])
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": len(articles)},
            "topics": {"hackernews": {"articles": articles}},
        }
        topic_defs = [
            {"id": "hackernews", "emoji": "📰", "label": "Hacker News / 热榜"}
        ]

        text = render_mod.render_digest(
            data,
            topic_defs=topic_defs,
            report_date="2026-05-22",
            version="3.17.5",
        )

        story_11_line = "• HN ranked story 11 — 89↑ · 11 comments"

        self.assertIn(story_11_line, text)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("Different coverage of story 3", text)
        self.assertNotIn("https://mirror.example.com/different-story-3", text)

    def test_hnrss_metadata_is_parsed_from_description(self):
        description = """
        <p>Article URL: <a href="https://example.com/article">https://example.com/article</a></p>
        <p>Comments URL: <a href="https://news.ycombinator.com/item?id=123">https://news.ycombinator.com/item?id=123</a></p>
        <p>Points: 234</p>
        <p># Comments: 56</p>
        """

        metadata = fetch_rss_mod.parse_hnrss_metadata(description)

        self.assertEqual(metadata["external_url"], "https://example.com/article")
        self.assertEqual(
            metadata["hn_url"],
            "https://news.ycombinator.com/item?id=123",
        )
        self.assertEqual(metadata["score"], 234)
        self.assertEqual(metadata["num_comments"], 56)

    def test_hnrss_regex_parser_preserves_feed_rank_for_ai_exceptions(self):
        content = """
        <rss><channel>
          <item>
            <title>Machine-learning systems</title>
            <link>https://example.com/story</link>
            <pubDate>Fri, 22 May 2026 12:00:00 +0000</pubDate>
            <description><![CDATA[
              <p>Article URL: <a href="https://example.com/story">https://example.com/story</a></p>
              <p>Comments URL: <a href="https://news.ycombinator.com/item?id=789">https://news.ycombinator.com/item?id=789</a></p>
              <p>Points: 345</p>
              <p># Comments: 67</p>
            ]]></description>
          </item>
        </channel></rss>
        """

        articles = fetch_rss_mod.parse_feed_regex(
            content,
            cutoff=datetime(2026, 5, 22, tzinfo=timezone.utc),
            feed_url="https://hnrss.org/frontpage",
        )

        self.assertEqual(articles[0]["hn_rank"], 1)

    def test_hnrss_atom_fallback_parses_metadata_from_summary(self):
        content = """
        <feed>
          <entry>
            <title>Atom HN story</title>
            <link href="https://example.com/atom-story" />
            <updated>2026-05-22T12:00:00Z</updated>
            <summary><![CDATA[
              <p>Article URL: <a href="https://example.com/atom-article">https://example.com/atom-article</a></p>
              <p>Comments URL: <a href="https://news.ycombinator.com/item?id=789">https://news.ycombinator.com/item?id=789</a></p>
              <p>Points: 345</p>
              <p># Comments: 67</p>
            ]]></summary>
          </entry>
        </feed>
        """

        articles = fetch_rss_mod.parse_feed_regex(
            content,
            cutoff=datetime(2026, 5, 22, tzinfo=timezone.utc),
            feed_url="https://hnrss.org/frontpage.atom",
        )

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["external_url"], "https://example.com/atom-article")
        self.assertEqual(
            articles[0]["hn_url"],
            "https://news.ycombinator.com/item?id=789",
        )
        self.assertEqual(articles[0]["score"], 345)
        self.assertEqual(articles[0]["num_comments"], 67)
        self.assertEqual(articles[0]["hn_rank"], 1)

    def test_hnrss_feedparser_path_parses_atom_summary_metadata(self):
        if not fetch_rss_mod.HAS_FEEDPARSER:
            self.skipTest("feedparser is not installed")

        content = """
        <feed>
          <entry>
            <title>Atom HN story</title>
            <link href="https://example.com/atom-story" />
            <updated>2026-05-22T12:00:00Z</updated>
            <summary><![CDATA[
              <p>Article URL: <a href="https://example.com/atom-article">https://example.com/atom-article</a></p>
              <p>Comments URL: <a href="https://news.ycombinator.com/item?id=790">https://news.ycombinator.com/item?id=790</a></p>
              <p>Points: 456</p>
              <p># Comments: 78</p>
            ]]></summary>
          </entry>
        </feed>
        """

        articles = fetch_rss_mod.parse_feed_feedparser(
            content,
            cutoff=datetime(2026, 5, 22, tzinfo=timezone.utc),
            feed_url="https://hnrss.org/frontpage.atom",
        )

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["external_url"], "https://example.com/atom-article")
        self.assertEqual(
            articles[0]["hn_url"],
            "https://news.ycombinator.com/item?id=790",
        )
        self.assertEqual(articles[0]["score"], 456)
        self.assertEqual(articles[0]["num_comments"], 78)
        self.assertEqual(articles[0]["hn_rank"], 1)

    def test_github_trending_fixed_sections_limit_to_top_five_repos(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 7},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": f"example/trending-{index}",
                            "link": f"https://github.com/example/trending-{index}",
                            "source_type": "github_trending",
                            "repo": f"example/trending-{index}",
                            "stars": 1000 + index,
                            "daily_stars_est": 100 - index,
                            "language": "TypeScript",
                            "description": f"Trending repo {index}.",
                            "quality_score": 10,
                        }
                        for index in range(7)
                    ]
                }
            },
        }

        discord_text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )
        chat_text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
            template="chat",
        )

        for text in (discord_text, chat_text):
            self.assertIn("example/trending-0", text)
            self.assertIn("example/trending-4", text)
            self.assertNotIn("example/trending-5", text)
            self.assertNotIn("example/trending-6", text)

    def test_discord_github_trending_does_not_render_daily_star_estimate(self):
        data = {
            "input_sources": {},
            "output_stats": {"total_articles": 1},
            "topics": {
                "supplemental": {
                    "articles": [
                        {
                            "title": "example/trending-tool",
                            "link": "https://github.com/example/trending-tool",
                            "source_type": "github_trending",
                            "repo": "example/trending-tool",
                            "stars": 1234,
                            "daily_stars_est": 56,
                            "language": "Python",
                            "description": "A trending tool.",
                            "quality_score": 10,
                        }
                    ]
                }
            },
        }

        text = render_mod.render_digest(
            data,
            topic_defs=[],
            report_date="2026-05-22",
            version="3.17.0",
        )

        self.assertIn("• **example/trending-tool** ⭐ 1.2K | Python — A trending tool.", text)
        self.assertNotIn("(+56/day)", text)
        self.assertNotIn("/day", text)

    def test_footer_uses_current_github_trending_count_key(self):
        data = {
            "input_sources": {
                "rss_articles": 0,
                "twitter_articles": 0,
                "web_articles": 0,
                "github_articles": 0,
                "github_trending": 2,
                "reddit_posts": 0,
                "podcast_episodes": 0,
            },
            "output_stats": {"total_articles": 0},
            "topics": {},
        }

        footer = render_mod.render_footer(data, version="3.17.0")

        self.assertIn("GitHub 0 releases + 2 trending", footer)

    def test_discord_visible_dedupe_resolves_cross_fixed_late_bridge(self):
        text = render_mod.render_digest(
            cross_fixed_bridge_fixture(),
            topic_defs=[],
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertEqual(text.count("https://x.com/example/status/a"), 1)
        self.assertNotIn(
            "https://github.com/example/bridge/releases/tag/v1.0.0",
            text,
        )
        self.assertIn("## 📢 KOL Updates", text)
        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("## 📝 Blog Picks", text)

    def test_chat_visible_dedupe_resolves_cross_fixed_late_bridge(self):
        text = render_mod.render_digest(
            cross_fixed_bridge_fixture(),
            topic_defs=[],
            report_date="2026-05-17",
            version="3.17.0",
            template="chat",
        )

        self.assertEqual(text.count("https://x.com/example/status/a"), 1)
        self.assertNotIn(
            "https://github.com/example/bridge/releases/tag/v1.0.0",
            text,
        )
        self.assertIn("## 📢 KOL Updates", text)
        self.assertNotIn("## 📦 GitHub Releases", text)
        self.assertNotIn("## 📝 Blog Picks", text)

    def test_discord_visible_dedupe_keeps_topic_sections_over_fixed_sections(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            duplicate_visible_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertEqual(text.count("https://example.com/blog/agent-evals?utm_source=rss"), 1)
        self.assertEqual(text.count("https://www.youtube.com/watch?v=abc123&utm_source=rss"), 1)
        self.assertEqual(text.count("https://x.com/example/status/1?utm_source=rss"), 1)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("## 🤖 AI Agent", text)
        self.assertNotIn("## 📢 KOL Updates", text)
        self.assertNotIn("## 📝 Blog Picks", text)
        self.assertNotIn("## 🎙️ Podcast Remix", text)

    def test_discord_visible_dedupe_skips_duplicate_topic_sections(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            topic_topic_duplicate_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertEqual(text.count("https://example.com/shared/agent-evals"), 1)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertNotIn("## 🤖 AI Agent", text)

    def test_discord_visible_dedupe_skips_same_title_different_url_topic(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            same_title_duplicate_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
        )

        self.assertEqual(text.count("https://example.com/a"), 1)
        self.assertNotIn("https://other.example/b", text)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertNotIn("## 🤖 AI Agent", text)

    def test_chat_visible_dedupe_keeps_topic_sections_over_fixed_sections(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            duplicate_visible_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
            template="chat",
        )

        self.assertEqual(text.count("https://example.com/blog/agent-evals?utm_source=rss"), 1)
        self.assertEqual(text.count("https://www.youtube.com/watch?v=abc123&utm_source=rss"), 1)
        self.assertEqual(text.count("https://x.com/example/status/1?utm_source=rss"), 1)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("## 🤖 AI Agent", text)
        self.assertNotIn("## 📢 KOL Updates", text)
        self.assertNotIn("## 📝 Blog Picks", text)
        self.assertNotIn("## 🎙️ Podcast Remix", text)

    def test_chat_visible_dedupe_skips_duplicate_topic_sections(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            topic_topic_duplicate_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
            template="chat",
        )

        self.assertEqual(text.count("https://example.com/shared/agent-evals"), 1)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertNotIn("## 🤖 AI Agent", text)

    def test_chat_visible_dedupe_skips_same_title_different_url_topic(self):
        topic_defs = [
            {"id": "llm", "emoji": "🧠", "label": "LLM / Large Models"},
            {"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"},
        ]

        text = render_mod.render_digest(
            same_title_duplicate_fixture(),
            topic_defs,
            report_date="2026-05-17",
            version="3.17.0",
            template="chat",
        )

        self.assertEqual(text.count("https://example.com/a"), 1)
        self.assertNotIn("https://other.example/b", text)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertNotIn("## 🤖 AI Agent", text)

    def test_prepare_manual_codex_context(self):
        data = load_acceptance_fixture()
        topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)
        source_fixture = ACCEPTANCE_FIXTURE

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)

            render_mod.prepare_codex_acceptance_context(
                data,
                topic_defs,
                source_fixture,
                output_dir,
                report_date="2026-02-27",
                version="3.17.0",
            )

            self.assertEqual(
                {path.name for path in output_dir.iterdir()},
                {"merged.json", "summarized.txt", "prompt.md", "expected.md"},
            )
            self.assertIn(
                "Do not run the network pipeline.",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Save the generated report as `actual.md` in this directory.",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "diff -u expected.md actual.md",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "references/digest-prompt.md",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "references/templates/discord.md",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "expected.md as a deterministic comparison sample",
                (output_dir / "prompt.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "# 🚀 Tech Digest - 2026-02-27",
                (output_dir / "expected.md").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Total articles: 9",
                (output_dir / "summarized.txt").read_text(encoding="utf-8"),
            )

    def test_cli_prepare_codex_context_does_not_require_output(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)

            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPTS_DIR / "render-acceptance-digest.py"),
                    "--input",
                    str(ACCEPTANCE_FIXTURE),
                    "--topics",
                    str(TOPICS_FILE),
                    "--date",
                    "2026-02-27",
                    "--version",
                    "3.17.0",
                    "--prepare-codex-context",
                    str(output_dir),
                ],
                cwd=ROOT_DIR,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                {path.name for path in output_dir.iterdir()},
                {"merged.json", "summarized.txt", "prompt.md", "expected.md"},
            )

    def test_cli_can_render_chat_template(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "daily-chat.md"

            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPTS_DIR / "render-acceptance-digest.py"),
                    "--input",
                    str(ACCEPTANCE_FIXTURE),
                    "--topics",
                    str(TOPICS_FILE),
                    "--date",
                    "2026-02-27",
                    "--version",
                    "3.17.0",
                    "--template",
                    "chat",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT_DIR,
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            text = output_path.read_text(encoding="utf-8")
            self.assertIn(
                f"1. {render_mod.bold_chat_title_text('OpenAI ships structured agent evaluation suite')}",
                text,
            )
            self.assertNotRegex(text, r"(?m)^[0-9]+\. \[[0-9]+(?:\.[0-9]+)?/10\] ")
            self.assertIn("🔗 https://openai.com/research/agent-evals", text)
            self.assertNotIn("<https://", text)


if __name__ == "__main__":
    unittest.main()
