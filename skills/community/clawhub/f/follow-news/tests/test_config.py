#!/usr/bin/env python3
"""Tests for config_loader.py."""

import json
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from config_loader import load_merged_sources, load_merged_topics

DEFAULTS_DIR = Path(__file__).parent.parent / "config" / "defaults"
README_EN = Path(__file__).parent.parent / "README.md"
README_ZH = Path(__file__).parent.parent / "README_CN.md"
SKILL_FILE = Path(__file__).parent.parent / "SKILL.md"
TEST_PIPELINE = Path(__file__).parent.parent / "scripts" / "test-pipeline.sh"
VALIDATE_CONFIG = Path(__file__).parent.parent / "scripts" / "validate-config.py"

REQUIRED_TOPICS = {
    "llm",
    "ai-agent",
    "kol",
    "hackernews",
    "frontier-tech",
    "podcast",
}

validate_config_spec = importlib.util.spec_from_file_location(
    "validate_config", VALIDATE_CONFIG
)
validate_config = importlib.util.module_from_spec(validate_config_spec)
validate_config_spec.loader.exec_module(validate_config)
validate_source_types = validate_config.validate_source_types


def read_skill_frontmatter():
    content = SKILL_FILE.read_text(encoding="utf-8")
    marker = "---"
    parts = content.split(marker, 2)
    if len(parts) < 3:
        raise AssertionError("SKILL.md is missing frontmatter")
    return parts[1].strip().splitlines()


def read_skill_metadata():
    for line in read_skill_frontmatter():
        if line.startswith("metadata:"):
            return json.loads(line.split(":", 1)[1].strip())
    raise AssertionError("SKILL.md frontmatter is missing metadata")


def get_source_counts():
    sources = load_merged_sources(DEFAULTS_DIR)
    topics = load_merged_topics(DEFAULTS_DIR)
    return {
        "total": len(sources),
        "rss": len([s for s in sources if s["type"] == "rss"]),
        "twitter": len([s for s in sources if s["type"] == "twitter"]),
        "github": len([s for s in sources if s["type"] == "github"]),
        "reddit": len([s for s in sources if s["type"] == "reddit"]),
        "podcast": len([s for s in sources if s["type"] == "podcast"]),
        "topics": len(topics),
    }


def group_sources_by_topic(sources):
    grouped = {}
    for source in sources:
        for topic in source.get("topics", []):
            grouped.setdefault(topic, []).append(source)
    return grouped


def get_topic_ids():
    topics = load_merged_topics(DEFAULTS_DIR)
    return [topic["id"] for topic in topics]


class TestLoadSources(unittest.TestCase):
    def test_loads_defaults(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        self.assertGreater(len(sources), 100)

    def test_all_sources_have_required_fields(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        for s in sources:
            self.assertIn("id", s, f"Source missing id: {s}")
            self.assertIn("type", s, f"Source missing type: {s}")
            self.assertIn("enabled", s, f"Source missing enabled: {s}")

    def test_source_types(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        types = set(s["type"] for s in sources)
        self.assertIn("rss", types)
        self.assertIn("twitter", types)
        self.assertIn("github", types)
        self.assertIn("reddit", types)

    def test_user_overlay_merges(self):
        """User overlay should override matching IDs and add new ones."""
        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {"id": "test-new-source", "type": "rss", "enabled": True, "url": "https://test.com/feed"},
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            sources = load_merged_sources(DEFAULTS_DIR, Path(tmpdir))
            ids = [s["id"] for s in sources]
            self.assertIn("test-new-source", ids)

    def test_user_overlay_disables(self):
        """User overlay with enabled=false should disable a default source."""
        defaults = load_merged_sources(DEFAULTS_DIR)
        first_id = defaults[0]["id"]

        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {"id": first_id, "type": defaults[0]["type"], "enabled": False},
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            sources = load_merged_sources(DEFAULTS_DIR, Path(tmpdir))
            matched = [s for s in sources if s["id"] == first_id]
            self.assertEqual(len(matched), 1)
            self.assertFalse(matched[0]["enabled"])

    def test_no_overlay_dir(self):
        """Should work fine with no user config dir."""
        sources = load_merged_sources(DEFAULTS_DIR, None)
        self.assertGreater(len(sources), 100)

    def test_user_overlay_accepts_podcast_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {
                        "id": "training-data-podcast",
                        "type": "podcast",
                        "name": "Training Data",
                        "enabled": True,
                        "priority": True,
                        "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
                        "platform": "youtube",
                        "topics": ["llm", "ai-agent"],
                        "transcript": {
                            "enabled": True,
                            "backend": "auto",
                            "languages": ["en", "zh", "zh-Hans"],
                        },
                    }
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            sources = load_merged_sources(DEFAULTS_DIR, Path(tmpdir))
            podcast = [s for s in sources if s["id"] == "training-data-podcast"]

            self.assertEqual(len(podcast), 1)
            self.assertEqual(podcast[0]["type"], "podcast")
            self.assertEqual(podcast[0]["platform"], "youtube")

    def test_source_types_include_podcast_when_user_adds_one(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {
                        "id": "test-podcast",
                        "type": "podcast",
                        "name": "Test Podcast",
                        "enabled": True,
                        "priority": False,
                        "url": "https://example.com/feed.xml",
                        "platform": "rss",
                        "topics": ["frontier-tech"],
                    }
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            sources = load_merged_sources(DEFAULTS_DIR, Path(tmpdir))
            types = {s["type"] for s in sources}

            self.assertIn("podcast", types)


class TestLoadTopics(unittest.TestCase):
    def test_loads_defaults(self):
        topics = load_merged_topics(DEFAULTS_DIR)
        self.assertGreater(len(topics), 0)

    def test_topics_have_required_fields(self):
        topics = load_merged_topics(DEFAULTS_DIR)
        for t in topics:
            self.assertIn("id", t, f"Topic missing id: {t}")
            self.assertIn("label", t, f"Topic missing label: {t}")

    def test_topic_ids(self):
        topics = load_merged_topics(DEFAULTS_DIR)
        ids = {t["id"] for t in topics}
        for expected in REQUIRED_TOPICS:
            self.assertIn(expected, ids)

    def test_kol_topic_has_representative_sources(self):
        topics = load_merged_topics(DEFAULTS_DIR)
        topic_ids = {t["id"] for t in topics}
        self.assertIn("kol", topic_ids)
        self.assertNotIn("builder", topic_ids)

        sources = load_merged_sources(DEFAULTS_DIR)
        topic_sources = group_sources_by_topic(sources)

        sources_for_topic = topic_sources.get("kol", [])
        self.assertGreater(len(sources_for_topic), 0)

        enabled_source_ids = {
            source["id"]
            for source in sources_for_topic
            if source.get("enabled", True)
        }
        self.assertGreater(len(enabled_source_ids), 0)
        self.assertIn("twitter", {source["type"] for source in sources_for_topic})

    def test_crypto_default_set_is_not_reintroduced(self):
        topics = load_merged_topics(DEFAULTS_DIR)
        topic_ids = {t["id"] for t in topics}
        self.assertNotIn("crypto", topic_ids)

        sources = load_merged_sources(DEFAULTS_DIR)
        source_topics = {
            topic for source in sources for topic in source.get("topics", [])
        }
        self.assertNotIn("crypto", source_topics)

    def test_kol_topic_has_stable_representative_sources(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        topic_sources = group_sources_by_topic(sources)

        sources_for_topic = topic_sources.get("kol", [])
        enabled_for_topic = [
            source for source in sources_for_topic if source.get("enabled", True)
        ]
        self.assertGreater(len(enabled_for_topic), 0)

        self.assertGreater(
            len(
                [
                    source
                    for source in enabled_for_topic
                    if source.get("type") == "twitter"
                ]
            ),
            0,
        )

    def test_hacker_news_source_uses_hackernews_topic_only(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        hn_sources = [source for source in sources if source.get("id") == "hn-rss"]

        self.assertEqual(len(hn_sources), 1)
        self.assertEqual(hn_sources[0].get("topics"), ["hackernews"])


class TestPodcastConfigValidation(unittest.TestCase):
    def podcast_source(self, **overrides):
        source = {
            "id": "test-podcast",
            "type": "podcast",
            "url": "https://example.com/feed.xml",
            "platform": "rss",
        }
        source.update(overrides)
        return source

    def test_validate_source_types_rejects_invalid_podcast_url(self):
        sources_data = {
            "sources": [
                self.podcast_source(url="not a url"),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_accepts_valid_podcast_urls(self):
        sources_data = {
            "sources": [
                self.podcast_source(id="rss-podcast", url="http://example.com/feed.xml"),
                self.podcast_source(
                    id="youtube-podcast",
                    url="https://www.youtube.com/playlist?list=abc",
                    platform="youtube",
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))

    def test_validate_source_types_accepts_xiaoyuzhou_platform(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    id="whynottv-podcast",
                    url="https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
                    platform="xiaoyuzhou",
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))

    def test_validate_source_types_accepts_xiaoyuzhou_url_with_query_and_fragment(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    id="whynottv-podcast",
                    url="https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940?foo=bar#section",
                    platform="xiaoyuzhou",
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))

    def test_validate_source_types_rejects_invalid_xiaoyuzhou_url_shape(self):
        invalid_urls = [
            "https://www.xiaoyuzhoufm.com/episode/69f441cd5390b7cc928acdcc",
            "https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940/extra",
            "https://www.xiaoyuzhoufm.com/podcast/",
            "https://example.com/podcast/686a1832222ae2de21fea940",
            "ftp://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
        ]

        for url in invalid_urls:
            with self.subTest(url=url):
                sources_data = {
                    "sources": [
                        self.podcast_source(url=url, platform="xiaoyuzhou"),
                    ]
                }

                self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_accepts_opencli_transcript_backend(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    url="https://www.xiaoyuzhoufm.com/podcast/686a1832222ae2de21fea940",
                    platform="xiaoyuzhou",
                    transcript={
                        "enabled": True,
                        "backend": "opencli",
                    },
                ),
            ]
        }

        self.assertTrue(validate_source_types(sources_data))

    def test_validate_source_types_rejects_opencli_backend_for_non_xiaoyuzhou_platform(self):
        sources_data = {
            "sources": [
                self.podcast_source(
                    url="https://www.youtube.com/playlist?list=abc",
                    platform="youtube",
                    transcript={
                        "enabled": True,
                        "backend": "opencli",
                    },
                ),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_podcast_url_with_whitespace_host(self):
        sources_data = {
            "sources": [
                self.podcast_source(url="https://exa mple.com/feed.xml"),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_podcast_url_with_malformed_ipv6(self):
        sources_data = {
            "sources": [
                self.podcast_source(url="https://[::1/feed.xml"),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_invalid_podcast_platform(self):
        sources_data = {
            "sources": [
                self.podcast_source(platform="vimeo"),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_non_object_transcript(self):
        sources_data = {
            "sources": [
                self.podcast_source(transcript=[]),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_invalid_transcript_backend(self):
        sources_data = {
            "sources": [
                self.podcast_source(transcript={"backend": "manual"}),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_invalid_transcript_enabled(self):
        sources_data = {
            "sources": [
                self.podcast_source(transcript={"enabled": "yes"}),
            ]
        }

        self.assertFalse(validate_source_types(sources_data))

    def test_validate_source_types_rejects_invalid_transcript_languages(self):
        for transcript in (
            {"languages": "en"},
            {"languages": ["en", 123]},
        ):
            with self.subTest(transcript=transcript):
                sources_data = {
                    "sources": [
                        self.podcast_source(transcript=transcript),
                    ]
                }

                self.assertFalse(validate_source_types(sources_data))

    def test_validate_config_accepts_podcast_overlay(self):
        import subprocess

        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {
                        "id": "training-data-podcast",
                        "type": "podcast",
                        "name": "Training Data",
                        "enabled": True,
                        "priority": True,
                        "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8",
                        "platform": "youtube",
                        "topics": ["llm", "ai-agent"],
                        "transcript": {
                            "enabled": True,
                            "backend": "auto",
                            "languages": ["en", "zh", "zh-Hans"],
                        },
                    }
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).parent.parent / "scripts" / "validate-config.py"),
                    "--defaults",
                    str(DEFAULTS_DIR),
                    "--config",
                    tmpdir,
                ],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_validate_config_rejects_podcast_without_url(self):
        import subprocess

        with tempfile.TemporaryDirectory() as tmpdir:
            overlay = {
                "sources": [
                    {
                        "id": "broken-podcast",
                        "type": "podcast",
                        "name": "Broken Podcast",
                        "enabled": True,
                        "priority": False,
                        "platform": "youtube",
                        "topics": ["llm"],
                    }
                ]
            }
            overlay_path = Path(tmpdir) / "follow-news-sources.json"
            with open(overlay_path, "w") as f:
                json.dump(overlay, f)

            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).parent.parent / "scripts" / "validate-config.py"),
                    "--defaults",
                    str(DEFAULTS_DIR),
                    "--config",
                    tmpdir,
                ],
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("url", result.stderr + result.stdout)


class TestSourceCounts(unittest.TestCase):
    """Verify source counts match expectations."""

    def test_total_sources(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        enabled = [s for s in sources if s.get("enabled", True)]
        self.assertGreaterEqual(len(enabled), 130)

    def test_twitter_count(self):
        counts = get_source_counts()
        self.assertEqual(counts["twitter"], 61)

    def test_rss_count(self):
        counts = get_source_counts()
        self.assertEqual(counts["rss"], 65)

    def test_github_count(self):
        counts = get_source_counts()
        self.assertEqual(counts["github"], 23)

    def test_reddit_count(self):
        counts = get_source_counts()
        self.assertEqual(counts["reddit"], 8)


class TestDocumentationExamples(unittest.TestCase):
    def test_english_readme_counts_are_current(self):
        counts = get_source_counts()
        content = README_EN.read_text(encoding="utf-8")
        self.assertIn(
            f"Automated tech news digest — {counts['total']} built-in sources, 7-source pipeline, one chat message to install.",
            content,
        )
        self.assertIn(
            f"A deduplicated tech digest built from **{counts['total']} built-in sources** plus **{counts['topics']} default report topics**:",
            content,
        )
        self.assertIn(
            f"| 📡 RSS | {counts['rss']} feeds |",
            content,
        )
        self.assertIn(
            f"| 🐙 GitHub | {counts['github']} repos |",
            content,
        )
        self.assertIn(
            "| 🎙️ Podcast | custom sources |",
            content,
        )
        self.assertIn("GitHub Tr.", content)
        self.assertIn(
            f"`config/defaults/sources.json` — {counts['total']} built-in sources ({counts['rss']} RSS, {counts['twitter']} Twitter, {counts['github']} GitHub, {counts['reddit']} Reddit, {counts['podcast']} Podcast)",
            content,
        )

    def test_chinese_readme_counts_are_current(self):
        counts = get_source_counts()
        content = README_ZH.read_text(encoding="utf-8")
        self.assertIn(
            f"自动化科技资讯汇总 — {counts['total']} 个内置数据源，7 层管道，一句话安装。",
            content,
        )
        self.assertIn(
            f"基于 **{counts['total']} 个内置数据源** + **{counts['topics']} 个默认报告主题** 的去重科技日报：",
            content,
        )
        self.assertIn(
            f"| 📡 RSS | {counts['rss']} 个订阅源 |",
            content,
        )
        self.assertIn(
            f"| 🐙 GitHub | {counts['github']} 个仓库 |",
            content,
        )
        self.assertIn(
            "| 🎙️ Podcast | 自定义源 |",
            content,
        )
        self.assertIn("RSS 播客订阅源、YouTube 播放列表/频道、小宇宙播客，以及可选转录文本", content)
        self.assertIn("GitHub Tr.", content)
        self.assertIn(
            f"`config/defaults/sources.json` — {counts['total']} 个内置数据源（{counts['rss']} RSS、{counts['twitter']} Twitter、{counts['github']} GitHub、{counts['reddit']} Reddit、{counts['podcast']} Podcast）",
            content,
        )
        self.assertIn(
            f"开箱即用，内置 {counts['total']} 个数据源，并支持自定义 podcast 源",
            content,
        )

    def test_podcast_runtime_docs_include_youtube_and_ytdlp(self):
        docs = {
            "README.md": README_EN.read_text(encoding="utf-8"),
            "README_CN.md": README_ZH.read_text(encoding="utf-8"),
            "SKILL.md": SKILL_FILE.read_text(encoding="utf-8"),
        }

        for name, content in docs.items():
            with self.subTest(doc=name):
                lowered = content.lower()
                self.assertIn("podcast", lowered)
                self.assertIn("youtube", lowered)
                self.assertIn("xiaoyuzhou", lowered)
                self.assertIn("yt-dlp", lowered)
                self.assertIn("opencli", lowered)
                self.assertIn("YTDLP_BIN", content)
                self.assertIn("OPENCLI_BIN", content)
                self.assertIn('"type": "podcast"', content)
                self.assertIn('"platform": "youtube"', content)
                self.assertIn('"platform": "xiaoyuzhou"', content)
                self.assertIn('"backend": "yt-dlp"', content)
                self.assertIn('"backend": "opencli"', content)

        skill = docs["SKILL.md"]
        self.assertIn("--trending FILE", skill)

        readme_zh = docs["README_CN.md"]
        self.assertIn("```bash\n# Twitter/X Backend", readme_zh)
        self.assertIn('export BRAVE_PLAN="free"           # Override Brave rate limit: free|pro\n```', readme_zh)
        self.assertIn("YouTube 播客元数据和转录文本抓取需要 `yt-dlp`", readme_zh)
        self.assertIn("对应 YouTube 播客源会标记为失败", readme_zh)
        self.assertNotIn("可选 transcript", readme_zh)
        self.assertNotIn("metadata/transcript enrich", readme_zh)

    def test_twitter_backend_docs_include_opencli(self):
        readme_en = README_EN.read_text(encoding="utf-8")
        readme_zh = README_ZH.read_text(encoding="utf-8")
        skill = SKILL_FILE.read_text(encoding="utf-8")

        for content in (readme_en, readme_zh, skill):
            lowered = content.lower()
            self.assertIn("opencli", lowered)
            self.assertIn("getxapi", lowered)
            self.assertIn("twitterapiio", lowered)
            self.assertIn("official", lowered)

        self.assertIn("OPENCLI_BIN", skill)

    def test_opencli_installation_requirements_are_documented(self):
        readme_en = README_EN.read_text(encoding="utf-8")
        readme_zh = README_ZH.read_text(encoding="utf-8")
        skill = SKILL_FILE.read_text(encoding="utf-8")

        for content in (readme_en, readme_zh, skill):
            lowered = content.lower()
            self.assertIn("jackwener/opencli", lowered)
            self.assertIn("install", lowered)
            self.assertIn("opencli doctor", lowered)

    def test_intro_docs_describe_current_default_topics(self):
        topic_ids = get_topic_ids()
        docs = {
            "README.md": README_EN.read_text(encoding="utf-8"),
            "README_CN.md": README_ZH.read_text(encoding="utf-8"),
            "SKILL.md": SKILL_FILE.read_text(encoding="utf-8"),
            "scripts/test-pipeline.sh": TEST_PIPELINE.read_text(encoding="utf-8"),
        }

        for name, content in docs.items():
            with self.subTest(doc=name):
                for topic_id in topic_ids:
                    self.assertIn(topic_id, content)

        retired_default_examples = (
            "CoinDesk",
            "VitalikButerin",
            "vitalik-twitter",
            "r/CryptoCurrency",
            "crypto news",
            "crypto sources",
            "Crypto, Frontier Tech",
            "--topics crypto",
        )
        for name, content in docs.items():
            with self.subTest(doc=name):
                for example in retired_default_examples:
                    self.assertNotIn(example, content)


class TestSkillFrontmatter(unittest.TestCase):
    def test_frontmatter_keeps_description_unambiguous_for_single_line_parsers(self):
        lines = read_skill_frontmatter()
        descriptions = [line for line in lines if line.lstrip().startswith("description:")]

        self.assertEqual(len(descriptions), 1)
        self.assertTrue(descriptions[0].startswith("description:"))
        self.assertTrue(descriptions[0].split(":", 1)[1].strip())
        self.assertNotIn("\n", descriptions[0])

    def test_frontmatter_uses_single_line_top_level_entries(self):
        lines = read_skill_frontmatter()
        top_level_keys = []

        for line in lines:
            self.assertFalse(line.startswith(" "), f"frontmatter entry is not top-level: {line}")
            self.assertIn(":", line, f"frontmatter entry is missing key separator: {line}")
            key, value = line.split(":", 1)
            self.assertTrue(key, f"frontmatter entry is missing key: {line}")
            self.assertTrue(value.strip(), f"frontmatter entry must be single-line key/value: {line}")
            top_level_keys.append(key)

        self.assertGreaterEqual(set(top_level_keys), {"name", "description", "version", "metadata"})

    def test_metadata_declares_runtime_env_tools_and_files(self):
        metadata = read_skill_metadata()
        openclaw = metadata["openclaw"]

        env_names = {entry["name"] for entry in openclaw["env"]}
        self.assertGreaterEqual(
            env_names,
            {
                "TWITTER_API_BACKEND",
                "OPENCLI_BIN",
                "TAVILY_API_KEY",
                "WEB_SEARCH_BACKEND",
                "BRAVE_API_KEYS",
                "BRAVE_API_KEY",
                "GITHUB_TOKEN",
                "GH_APP_ID",
                "GH_APP_INSTALL_ID",
                "GH_APP_KEY_FILE",
                "YTDLP_BIN",
            },
        )
        self.assertIn("yt-dlp", openclaw["optionalBins"])
        self.assertEqual(openclaw["files"]["read"][0]["path"], "config/defaults/")
        tools_by_bin = {entry["bin"]: entry for entry in openclaw["tools"] if "bin" in entry}
        self.assertTrue(tools_by_bin["python3"]["required"])
        self.assertFalse(tools_by_bin["yt-dlp"]["required"])
        self.assertTrue(
            any(
                entry.get("script") == "scripts/fetch-podcast.py"
                for entry in openclaw["tools"]
            )
        )
        self.assertIn("python3", openclaw["requires"]["bins"])

    def test_skill_web_search_docs_do_not_advertise_unimplemented_backends(self):
        skill = SKILL_FILE.read_text(encoding="utf-8")
        fetch_web_section = skill.split("#### `fetch-web.py` - Web Search Engine", 1)[1].split(
            "#### `fetch-github.py`",
            1,
        )[0]
        web_backend_lines = [line for line in skill.splitlines() if "WEB_SEARCH_BACKEND" in line]

        for line in web_backend_lines:
            self.assertNotIn("browser", line)
        self.assertNotIn("browser-backed", fetch_web_section)
        self.assertIn("auto|brave|tavily", skill)


if __name__ == "__main__":
    unittest.main()
