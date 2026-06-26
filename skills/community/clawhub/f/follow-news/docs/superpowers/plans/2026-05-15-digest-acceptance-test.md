# Digest Acceptance Test Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic Markdown/Discord digest acceptance test plus a manual Codex acceptance context for the current `follow-news` output format.

**Architecture:** Add a test-only renderer that converts a fixed merged JSON fixture into the current Markdown/Discord digest contract. Unit tests compare that output to a golden file and gate golden updates behind `UPDATE_GOLDEN=1`; a separate manual context command writes the fixture, expected output, summarized input, and prompt under `/tmp/follow-news-acceptance/`.

**Tech Stack:** Python 3.8 standard library, `unittest`, JSON fixtures, golden-file diffing with `difflib`, existing `config/defaults/topics.json`, existing `scripts/summarize-merged.py`.

---

## File Structure

- Create: `tests/fixtures/acceptance-merged.json`
  - Dedicated small merged-output fixture for final digest acceptance.
  - Covers topic articles, multi-source indicators, KOL metrics, GitHub releases, GitHub Trending, Blog Picks, Podcast Remix, and footer counts.

- Create: `scripts/render-acceptance-digest.py`
  - Test-only deterministic renderer.
  - Exposes pure functions for tests and a CLI for humans.
  - Does not call network, LLMs, delivery tools, or archive writers.

- Create: `tests/test_acceptance_digest.py`
  - Imports the hyphenated renderer via `importlib.util`.
  - Checks fixture shape, renderer structure, golden diff, `UPDATE_GOLDEN=1` behavior, and manual context creation.

- Create: `tests/golden/daily-discord.md`
  - Product acceptance sample for current Markdown/Discord output format.

- Modify: `README.md`
  - Add a short acceptance test command section.

- Modify: `README_CN.md`
  - Add the same command section in Chinese prose with English commands.

## Task 1: Add Acceptance Fixture and Fixture Shape Test

**Files:**
- Create: `tests/fixtures/acceptance-merged.json`
- Create: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Create the dedicated acceptance fixture**

Create `tests/fixtures/acceptance-merged.json` with this exact content:

```json
{
  "generated": "2026-02-27T12:04:12+00:00",
  "input_sources": {
    "rss_articles": 3,
    "twitter_articles": 1,
    "web_articles": 1,
    "github_articles": 1,
    "trending_repositories": 1,
    "reddit_posts": 1,
    "podcast_episodes": 1,
    "total_input": 9
  },
  "processing": {
    "deduplication_applied": true,
    "multi_source_merging": true,
    "previous_digest_penalty": false,
    "quality_scoring": true
  },
  "output_stats": {
    "total_articles": 9,
    "topics_count": 4,
    "topic_distribution": {
      "llm": 3,
      "ai-agent": 2,
      "builder": 1,
      "podcast": 1
    }
  },
  "topics": {
    "llm": {
      "count": 3,
      "articles": [
        {
          "title": "OpenAI ships structured agent evaluation suite",
          "link": "https://openai.com/research/agent-evals",
          "date": "2026-02-27T08:00:00+00:00",
          "topics": ["llm", "ai-agent"],
          "source_type": "rss",
          "source_name": "OpenAI Blog",
          "source_id": "openai-rss",
          "quality_score": 18,
          "multi_source": true,
          "source_count": 3,
          "all_sources": ["OpenAI Blog", "Hacker News", "r/OpenAI"],
          "primary_topic": "llm",
          "snippet": "OpenAI published a new suite for evaluating agent reliability across tool use and long-horizon tasks."
        },
        {
          "title": "Claude Code adds repository-wide planning mode",
          "link": "https://www.anthropic.com/news/claude-code-planning",
          "date": "2026-02-27T07:30:00+00:00",
          "topics": ["llm"],
          "source_type": "web",
          "source_name": "Anthropic News",
          "source_id": "web-anthropic",
          "quality_score": 12,
          "multi_source": false,
          "primary_topic": "llm",
          "snippet": "The new mode helps developers review multi-file plans before code changes."
        },
        {
          "title": "Low scoring model rumor should not render",
          "link": "https://example.com/low-score",
          "date": "2026-02-27T06:00:00+00:00",
          "topics": ["llm"],
          "source_type": "web",
          "source_name": "Example",
          "source_id": "example-low",
          "quality_score": 4,
          "multi_source": false,
          "primary_topic": "llm",
          "snippet": "This item is below the minimum score threshold."
        }
      ]
    },
    "ai-agent": {
      "count": 2,
      "articles": [
        {
          "title": "LangGraph releases durable multi-agent workflows",
          "link": "https://blog.langchain.dev/durable-multi-agent-workflows",
          "date": "2026-02-27T05:45:00+00:00",
          "topics": ["ai-agent"],
          "source_type": "rss",
          "source_name": "LangChain Blog",
          "source_id": "langchain-blog",
          "quality_score": 14,
          "multi_source": false,
          "primary_topic": "ai-agent",
          "snippet": "LangGraph adds checkpoints and resumable orchestration for production agents."
        },
        {
          "title": "SWE-agent benchmark report",
          "link": "https://x.com/swebench/status/1234567890",
          "date": "2026-02-27T05:00:00+00:00",
          "topics": ["ai-agent", "kol"],
          "source_type": "twitter",
          "source_name": "SWE-bench",
          "source_id": "twitter-swebench",
          "quality_score": 11,
          "multi_source": false,
          "primary_topic": "ai-agent",
          "display_name": "SWE-bench",
          "handle": "swebench",
          "metrics": {
            "impression_count": 12500,
            "reply_count": 45,
            "retweet_count": 230,
            "like_count": 1800
          },
          "summary": "Shared a benchmark report on repository-level coding agents."
        }
      ]
    },
    "builder": {
      "count": 1,
      "articles": [
        {
          "title": "Simon Willison explains practical prompt injection defenses",
          "link": "https://simonwillison.net/2026/Feb/27/prompt-injection-defenses/",
          "date": "2026-02-27T04:00:00+00:00",
          "topics": ["builder"],
          "source_type": "rss",
          "source_name": "Simon Willison",
          "source_id": "simonwillison-rss",
          "quality_score": 13,
          "multi_source": false,
          "primary_topic": "builder",
          "author": "Simon Willison",
          "is_blog_pick": true,
          "full_text": "Prompt injection defenses work best when systems minimize authority in retrieved content, isolate tool execution, and expose clear audit trails for users."
        }
      ]
    },
    "podcast": {
      "count": 1,
      "articles": [
        {
          "title": "Why agents need product taste",
          "link": "https://www.youtube.com/watch?v=agenttaste",
          "date": "2026-02-27T03:00:00+00:00",
          "topics": ["podcast"],
          "source_type": "podcast",
          "source_name": "Training Data",
          "source_id": "training-data-podcast",
          "quality_score": 15,
          "multi_source": false,
          "primary_topic": "podcast",
          "show_name": "Training Data",
          "transcript_status": "ok",
          "transcript": "Host | 00:00 - 00:05 Taste is the difference between a tool that demos well and a tool that gets used every morning.",
          "snippet": "A conversation about product taste, evaluation loops, and agent reliability."
        }
      ]
    },
    "frontier-tech": {
      "count": 2,
      "articles": [
        {
          "title": "vLLM ships v1.0 scheduler improvements",
          "link": "https://github.com/vllm-project/vllm/releases/tag/v1.0.0",
          "date": "2026-02-27T02:00:00+00:00",
          "topics": ["frontier-tech"],
          "source_type": "github",
          "source_name": "vllm-project/vllm",
          "source_id": "github-vllm",
          "quality_score": 10,
          "multi_source": false,
          "primary_topic": "frontier-tech",
          "repo": "vllm-project/vllm",
          "tag_name": "v1.0.0",
          "summary": "The release improves scheduler fairness and production serving stability."
        },
        {
          "title": "browser-use/web-ui",
          "link": "https://github.com/browser-use/web-ui",
          "date": "2026-02-27T01:00:00+00:00",
          "topics": ["frontier-tech"],
          "source_type": "github_trending",
          "source_name": "GitHub Trending",
          "source_id": "github-trending",
          "quality_score": 9,
          "multi_source": false,
          "primary_topic": "frontier-tech",
          "repo": "browser-use/web-ui",
          "stars": 1234,
          "daily_stars_est": 76,
          "language": "TypeScript",
          "description": "Run browser agents from a local web UI."
        }
      ]
    }
  }
}
```

- [ ] **Step 2: Add a fixture shape test**

Create `tests/test_acceptance_digest.py` with this exact initial content:

```python
#!/usr/bin/env python3
"""Acceptance tests for final Markdown/Discord digest output."""

import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"
ACCEPTANCE_FIXTURE = FIXTURES_DIR / "acceptance-merged.json"


def load_acceptance_fixture():
    with open(ACCEPTANCE_FIXTURE, "r") as f:
        return json.load(f)


class TestAcceptanceFixture(unittest.TestCase):
    def test_fixture_covers_acceptance_sections(self):
        data = load_acceptance_fixture()
        self.assertEqual(data["output_stats"]["total_articles"], 9)

        articles = [
            article
            for topic in data["topics"].values()
            for article in topic.get("articles", [])
        ]
        source_types = {article.get("source_type") for article in articles}

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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the fixture shape test**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS with one test.

- [ ] **Step 4: Commit the fixture and shape test**

```bash
git add tests/fixtures/acceptance-merged.json tests/test_acceptance_digest.py
git commit -m "test: add digest acceptance fixture"
```

## Task 2: Add Deterministic Renderer Core

**Files:**
- Create: `scripts/render-acceptance-digest.py`
- Modify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add failing renderer tests**

Replace `tests/test_acceptance_digest.py` with:

```python
#!/usr/bin/env python3
"""Acceptance tests for final Markdown/Discord digest output."""

import importlib.util
import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"
TOPICS_FILE = ROOT_DIR / "config" / "defaults" / "topics.json"
ACCEPTANCE_FIXTURE = FIXTURES_DIR / "acceptance-merged.json"

spec = importlib.util.spec_from_file_location(
    "render_acceptance_digest",
    SCRIPTS_DIR / "render-acceptance-digest.py",
)
render_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mod)


def load_acceptance_fixture():
    with open(ACCEPTANCE_FIXTURE, "r") as f:
        return json.load(f)


class TestAcceptanceFixture(unittest.TestCase):
    def test_fixture_covers_acceptance_sections(self):
        data = load_acceptance_fixture()
        self.assertEqual(data["output_stats"]["total_articles"], 9)

        articles = [
            article
            for topic in data["topics"].values()
            for article in topic.get("articles", [])
        ]
        source_types = {article.get("source_type") for article in articles}

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


class TestAcceptanceRenderer(unittest.TestCase):
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
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("• 🔥18 | OpenAI ships structured agent evaluation suite", text)
        self.assertIn("  <https://openai.com/research/agent-evals>", text)
        self.assertIn("  *[3 sources]*", text)
        self.assertNotIn("Low scoring model rumor should not render", text)
        self.assertIn("## 📢 KOL Updates", text)
        self.assertIn("`👁 12.5K | 💬 45 | 🔁 230 | ❤️ 1.8K`", text)
        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("## 🐙 GitHub Trending", text)
        self.assertIn("## 📝 Blog Picks", text)
        self.assertIn("## 🎙️ Podcast Remix", text)
        self.assertIn(
            "📊 Data Sources: RSS 3 | Twitter 1 | Reddit 1 | Web 1 | GitHub 1 releases + 1 trending | Podcast 1 episodes | Dedup: 9 articles",
            text,
        )
        self.assertTrue(text.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run renderer tests and verify failure**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: FAIL during import with a missing `scripts/render-acceptance-digest.py` file.

- [ ] **Step 3: Implement the renderer core**

Create `scripts/render-acceptance-digest.py` with:

```python
#!/usr/bin/env python3
"""Render deterministic Markdown/Discord digest output for acceptance tests."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


MIN_QUALITY_SCORE = 5


def load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r") as f:
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


def quality_score(article: Dict[str, Any]) -> float:
    value = article.get("quality_score", 0)
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def format_score(value: float) -> str:
    if value.is_integer():
        return str(int(value))
    return f"{value:.1f}".rstrip("0").rstrip(".")


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


def iter_articles(data: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    for topic in data.get("topics", {}).values():
        if not isinstance(topic, dict):
            continue
        for article in topic.get("articles", []):
            if isinstance(article, dict):
                yield article


def unique_articles(
    articles: Iterable[Dict[str, Any]],
    source_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for article in articles:
        if source_type and article.get("source_type") != source_type:
            continue
        key = article_link(article) or article.get("title") or id(article)
        if key in seen:
            continue
        seen.add(key)
        result.append(article)
    return result


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
) -> List[str]:
    sections = []
    topics = data.get("topics", {})

    for topic_def in topic_defs:
        topic_id = topic_def.get("id")
        topic_data = topics.get(topic_id)
        if not isinstance(topic_data, dict):
            continue

        articles = sorted_topic_articles(topic_data)
        if not articles:
            continue

        lines = [f"## {topic_def.get('emoji', '')} {topic_def.get('label', topic_id)}".rstrip(), ""]
        for article in articles:
            score = format_score(quality_score(article))
            lines.append(f"• 🔥{score} | {article.get('title', '?')}")
            lines.append(f"  <{article_link(article)}>")
            if article.get("multi_source"):
                lines.append(f"  *[{article.get('source_count', 2)} sources]*")
            lines.append("")
        sections.append("\n".join(lines).rstrip())

    return sections


def render_kol_updates(data: Dict[str, Any]) -> Optional[str]:
    tweets = [
        article
        for article in unique_articles(iter_articles(data), "twitter")
        if article_link(article)
    ]
    if not tweets:
        return None

    tweets = sorted(tweets, key=quality_score, reverse=True)
    lines = ["## 📢 KOL Updates", ""]
    for article in tweets:
        metrics = article.get("metrics", {})
        metric_text = (
            f"👁 {format_count(metrics.get('impression_count'))} | "
            f"💬 {format_count(metrics.get('reply_count'))} | "
            f"🔁 {format_count(metrics.get('retweet_count'))} | "
            f"❤️ {format_count(metrics.get('like_count'))}"
        )
        display_name = article.get("display_name") or article.get("source_name") or "Unknown"
        handle = article.get("handle") or article.get("source_id") or "unknown"
        summary = article.get("summary") or article.get("snippet") or article.get("title", "")
        lines.append(f"• **{display_name}** (@{handle}) — {summary} `{metric_text}`")
        lines.append(f"  <{article_link(article)}>")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_github_releases(data: Dict[str, Any]) -> Optional[str]:
    releases = [
        article
        for article in unique_articles(iter_articles(data), "github")
        if article_link(article)
    ]
    if not releases:
        return None

    releases = sorted(releases, key=quality_score, reverse=True)
    lines = ["## 📦 GitHub Releases", ""]
    for article in releases:
        repo = article.get("repo") or article.get("source_name") or article.get("title", "?")
        tag = article.get("tag_name") or article.get("version") or "release"
        summary = article.get("summary") or article.get("snippet") or article.get("title", "")
        lines.append(f"• **{repo}** `{tag}` — {summary}")
        lines.append(f"  <{article_link(article)}>")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_github_trending(data: Dict[str, Any]) -> Optional[str]:
    repos = [
        article
        for article in unique_articles(iter_articles(data), "github_trending")
        if article_link(article)
    ]
    if not repos:
        return None

    repos = sorted(repos, key=lambda article: article.get("daily_stars_est", 0), reverse=True)
    lines = ["## 🐙 GitHub Trending", ""]
    for article in repos:
        repo = article.get("repo") or article.get("title", "?")
        stars = format_count(article.get("stars"))
        daily_stars = format_count(article.get("daily_stars_est"))
        language = article.get("language") or "Unknown"
        description = article.get("description") or article.get("snippet") or ""
        lines.append(f"• **{repo}** ⭐ {stars} (+{daily_stars}/day) | {language} — {description}")
        lines.append(f"  <{article_link(article)}>")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_blog_picks(data: Dict[str, Any]) -> Optional[str]:
    picks = [
        article
        for article in unique_articles(iter_articles(data))
        if article.get("is_blog_pick") and article_link(article)
    ]
    if not picks:
        return None

    picks = sorted(picks, key=quality_score, reverse=True)
    lines = ["## 📝 Blog Picks", ""]
    for article in picks:
        author = article.get("author") or article.get("source_name") or "Unknown"
        summary = article.get("full_text") or article.get("snippet") or article.get("summary") or ""
        lines.append(f"• **{article.get('title', '?')}** — {author} | {summary}")
        lines.append(f"  <{article_link(article)}>")
        lines.append("")

    return "\n".join(lines).rstrip()


def render_podcast_remix(data: Dict[str, Any]) -> Optional[str]:
    episodes = [
        article
        for article in unique_articles(iter_articles(data), "podcast")
        if article.get("transcript_status") == "ok"
        and article.get("transcript")
        and article_link(article)
    ]
    if not episodes:
        return None

    episodes = sorted(episodes, key=quality_score, reverse=True)
    lines = ["## 🎙️ Podcast Remix", ""]
    for article in episodes:
        show_name = article.get("show_name") or article.get("source_name") or "Unknown"
        summary = article.get("snippet") or article.get("summary") or ""
        quote = str(article.get("transcript", "")).strip().splitlines()[0]
        lines.append(
            f"• **{article.get('title', '?')}** — {show_name} | {summary} Quote: \"{quote}\""
        )
        lines.append(f"  <{article_link(article)}>")
        lines.append("")

    return "\n".join(lines).rstrip()


def source_count(data: Dict[str, Any], key: str) -> int:
    input_sources = data.get("input_sources", {})
    value = input_sources.get(key, 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def render_footer(data: Dict[str, Any], version: str) -> str:
    stats = data.get("output_stats", {})
    merged = stats.get("total_articles", 0)
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
                f"{source_count(data, 'trending_repositories')} trending | "
                f"Podcast {source_count(data, 'podcast_episodes')} episodes | "
                f"Dedup: {merged} articles"
            ),
            (
                f"🤖 Generated by follow-news v{version} | "
                "<https://github.com/tangwz/follow-news> | Powered by OpenClaw"
            ),
        ]
    )


def render_digest(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    report_date: str,
    version: str,
) -> str:
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_topic_sections(data, topic_defs))

    for renderer in (
        render_kol_updates,
        render_github_releases,
        render_github_trending,
        render_blog_picks,
        render_podcast_remix,
    ):
        section = renderer(data)
        if section:
            sections.append(section)

    sections.append(render_footer(data, version))
    return "\n\n".join(sections).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render deterministic Markdown/Discord digest acceptance output."
    )
    parser.add_argument("--input", type=Path, required=True, help="Merged JSON input")
    parser.add_argument("--topics", type=Path, required=True, help="Topics JSON file")
    parser.add_argument("--date", required=True, help="Report date in YYYY-MM-DD format")
    parser.add_argument("--version", required=True, help="follow-news version string")
    parser.add_argument("--output", type=Path, required=True, help="Markdown output path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data = load_json(args.input)
    topic_defs = load_topic_definitions(args.topics)
    output = render_digest(data, topic_defs, args.date, args.version)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run renderer tests and verify pass**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS with two tests.

- [ ] **Step 5: Run renderer CLI smoke test**

Run:

```bash
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output /tmp/follow-news-acceptance-smoke.md
```

Expected: exit code 0 and `/tmp/follow-news-acceptance-smoke.md` exists.

- [ ] **Step 6: Commit renderer core**

```bash
git add scripts/render-acceptance-digest.py tests/test_acceptance_digest.py
git commit -m "test: render deterministic digest acceptance output"
```

## Task 3: Add Golden File Diff Test

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Create: `tests/golden/daily-discord.md`

- [ ] **Step 1: Generate the initial golden file**

Run:

```bash
mkdir -p tests/golden
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output tests/golden/daily-discord.md
```

Expected: `tests/golden/daily-discord.md` is created.

- [ ] **Step 2: Verify the golden content**

Run:

```bash
sed -n '1,220p' tests/golden/daily-discord.md
```

Expected output should start with this exact content:

```markdown
# 🚀 Tech Digest - 2026-02-27

## 🧠 LLM / Large Models

• 🔥18 | OpenAI ships structured agent evaluation suite
  <https://openai.com/research/agent-evals>
  *[3 sources]*

• 🔥12 | Claude Code adds repository-wide planning mode
  <https://www.anthropic.com/news/claude-code-planning>
```

- [ ] **Step 3: Add the golden diff test**

Replace `tests/test_acceptance_digest.py` with:

```python
#!/usr/bin/env python3
"""Acceptance tests for final Markdown/Discord digest output."""

import difflib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"
GOLDEN_DIR = ROOT_DIR / "tests" / "golden"
TOPICS_FILE = ROOT_DIR / "config" / "defaults" / "topics.json"
ACCEPTANCE_FIXTURE = FIXTURES_DIR / "acceptance-merged.json"
DAILY_GOLDEN = GOLDEN_DIR / "daily-discord.md"

spec = importlib.util.spec_from_file_location(
    "render_acceptance_digest",
    SCRIPTS_DIR / "render-acceptance-digest.py",
)
render_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mod)


def load_acceptance_fixture():
    with open(ACCEPTANCE_FIXTURE, "r") as f:
        return json.load(f)


def render_daily_digest():
    data = load_acceptance_fixture()
    topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)
    return render_mod.render_digest(
        data,
        topic_defs,
        report_date="2026-02-27",
        version="3.17.0",
    )


class TestAcceptanceFixture(unittest.TestCase):
    def test_fixture_covers_acceptance_sections(self):
        data = load_acceptance_fixture()
        self.assertEqual(data["output_stats"]["total_articles"], 9)

        articles = [
            article
            for topic in data["topics"].values()
            for article in topic.get("articles", [])
        ]
        source_types = {article.get("source_type") for article in articles}

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


class TestAcceptanceRenderer(unittest.TestCase):
    def test_render_digest_uses_current_discord_structure(self):
        text = render_daily_digest()

        self.assertIn("# 🚀 Tech Digest - 2026-02-27", text)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("• 🔥18 | OpenAI ships structured agent evaluation suite", text)
        self.assertIn("  <https://openai.com/research/agent-evals>", text)
        self.assertIn("  *[3 sources]*", text)
        self.assertNotIn("Low scoring model rumor should not render", text)
        self.assertIn("## 📢 KOL Updates", text)
        self.assertIn("`👁 12.5K | 💬 45 | 🔁 230 | ❤️ 1.8K`", text)
        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("## 🐙 GitHub Trending", text)
        self.assertIn("## 📝 Blog Picks", text)
        self.assertIn("## 🎙️ Podcast Remix", text)
        self.assertIn(
            "📊 Data Sources: RSS 3 | Twitter 1 | Reddit 1 | Web 1 | GitHub 1 releases + 1 trending | Podcast 1 episodes | Dedup: 9 articles",
            text,
        )
        self.assertTrue(text.endswith("\n"))

    def test_daily_digest_matches_golden(self):
        actual = render_daily_digest()
        expected = DAILY_GOLDEN.read_text()

        if actual != expected:
            diff = "\n".join(
                difflib.unified_diff(
                    expected.splitlines(),
                    actual.splitlines(),
                    fromfile=str(DAILY_GOLDEN),
                    tofile="rendered daily digest",
                    lineterm="",
                )
            )
            self.fail("Daily digest golden mismatch:\n" + diff)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 4: Run the golden test**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS with three tests.

- [ ] **Step 5: Commit golden diff coverage**

```bash
git add tests/test_acceptance_digest.py tests/golden/daily-discord.md
git commit -m "test: add digest golden acceptance check"
```

## Task 4: Add Explicit Golden Update Gate and Structure Assertions

**Files:**
- Modify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add update gate and structure assertions**

Replace `tests/test_acceptance_digest.py` with:

```python
#!/usr/bin/env python3
"""Acceptance tests for final Markdown/Discord digest output."""

import difflib
import importlib.util
import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
FIXTURES_DIR = ROOT_DIR / "tests" / "fixtures"
GOLDEN_DIR = ROOT_DIR / "tests" / "golden"
TOPICS_FILE = ROOT_DIR / "config" / "defaults" / "topics.json"
ACCEPTANCE_FIXTURE = FIXTURES_DIR / "acceptance-merged.json"
DAILY_GOLDEN = GOLDEN_DIR / "daily-discord.md"

spec = importlib.util.spec_from_file_location(
    "render_acceptance_digest",
    SCRIPTS_DIR / "render-acceptance-digest.py",
)
render_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mod)


def load_acceptance_fixture():
    with open(ACCEPTANCE_FIXTURE, "r") as f:
        return json.load(f)


def render_daily_digest():
    data = load_acceptance_fixture()
    topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)
    return render_mod.render_digest(
        data,
        topic_defs,
        report_date="2026-02-27",
        version="3.17.0",
    )


def assert_or_update_golden(testcase, expected_path, actual):
    if os.environ.get("UPDATE_GOLDEN") == "1":
        expected_path.parent.mkdir(parents=True, exist_ok=True)
        expected_path.write_text(actual)
        print(f"golden updated: {expected_path}")
        return

    expected = expected_path.read_text()
    if actual != expected:
        diff = "\n".join(
            difflib.unified_diff(
                expected.splitlines(),
                actual.splitlines(),
                fromfile=str(expected_path),
                tofile="rendered daily digest",
                lineterm="",
            )
        )
        testcase.fail("Daily digest golden mismatch:\n" + diff)


class TestAcceptanceFixture(unittest.TestCase):
    def test_fixture_covers_acceptance_sections(self):
        data = load_acceptance_fixture()
        self.assertEqual(data["output_stats"]["total_articles"], 9)

        articles = [
            article
            for topic in data["topics"].values()
            for article in topic.get("articles", [])
        ]
        source_types = {article.get("source_type") for article in articles}

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


class TestAcceptanceRenderer(unittest.TestCase):
    def test_render_digest_uses_current_discord_structure(self):
        text = render_daily_digest()

        self.assertIn("# 🚀 Tech Digest - 2026-02-27", text)
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("• 🔥18 | OpenAI ships structured agent evaluation suite", text)
        self.assertIn("  <https://openai.com/research/agent-evals>", text)
        self.assertIn("  *[3 sources]*", text)
        self.assertNotIn("Low scoring model rumor should not render", text)
        self.assertIn("## 📢 KOL Updates", text)
        self.assertIn("`👁 12.5K | 💬 45 | 🔁 230 | ❤️ 1.8K`", text)
        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("## 🐙 GitHub Trending", text)
        self.assertIn("## 📝 Blog Picks", text)
        self.assertIn("## 🎙️ Podcast Remix", text)
        self.assertIn(
            "📊 Data Sources: RSS 3 | Twitter 1 | Reddit 1 | Web 1 | GitHub 1 releases + 1 trending | Podcast 1 episodes | Dedup: 9 articles",
            text,
        )
        self.assertTrue(text.endswith("\n"))

    def test_daily_digest_structure_contract(self):
        text = render_daily_digest()

        self.assertTrue(text.startswith("# 🚀 Tech Digest - 2026-02-27\n"))
        self.assertIn("\n## 🧠 LLM / Large Models\n", text)
        self.assertIn("\n---\n📊 Data Sources:", text)
        self.assertIn("Powered by OpenClaw", text)

        article_lines = [line for line in text.splitlines() if line.startswith("• 🔥")]
        self.assertGreaterEqual(len(article_lines), 5)
        for line in article_lines:
            self.assertRegex(line, r"^• 🔥[0-9]+(?:\.[0-9]+)? \| .+")

        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("• 🔥"):
                self.assertLess(index + 1, len(lines))
                self.assertRegex(lines[index + 1], r"^  <https?://")

        topic_scores = []
        in_llm_section = False
        for line in lines:
            if line.startswith("## "):
                in_llm_section = line == "## 🧠 LLM / Large Models"
                continue
            if in_llm_section and line.startswith("• 🔥"):
                match = re.match(r"^• 🔥([0-9]+(?:\.[0-9]+)?)", line)
                self.assertIsNotNone(match)
                topic_scores.append(float(match.group(1)))

        self.assertEqual(topic_scores, sorted(topic_scores, reverse=True))

    def test_daily_digest_matches_golden(self):
        assert_or_update_golden(self, DAILY_GOLDEN, render_daily_digest())

    def test_update_golden_requires_explicit_environment_flag(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "daily-discord.md"
            path.write_text("old\n")

            with patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(AssertionError):
                    assert_or_update_golden(self, path, "new\n")
            self.assertEqual(path.read_text(), "old\n")

            with patch.dict(os.environ, {"UPDATE_GOLDEN": "1"}, clear=True):
                assert_or_update_golden(self, path, "new\n")
            self.assertEqual(path.read_text(), "new\n")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run acceptance tests**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS with five tests.

- [ ] **Step 3: Verify explicit golden update path**

Run:

```bash
UPDATE_GOLDEN=1 python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS and output includes `golden updated:`.

- [ ] **Step 4: Confirm golden did not change unexpectedly**

Run:

```bash
git diff -- tests/golden/daily-discord.md
```

Expected: no diff.

- [ ] **Step 5: Commit update gate and structure assertions**

```bash
git add tests/test_acceptance_digest.py
git commit -m "test: gate digest golden updates"
```

## Task 5: Add Manual Codex Acceptance Context

**Files:**
- Modify: `scripts/render-acceptance-digest.py`
- Modify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add failing manual context test**

Append this test method inside `TestAcceptanceRenderer` in `tests/test_acceptance_digest.py`:

```python
    def test_prepare_manual_codex_context(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir)
            data = load_acceptance_fixture()
            topic_defs = render_mod.load_topic_definitions(TOPICS_FILE)

            render_mod.prepare_codex_acceptance_context(
                data=data,
                topic_defs=topic_defs,
                source_fixture=ACCEPTANCE_FIXTURE,
                output_dir=output_dir,
                report_date="2026-02-27",
                version="3.17.0",
            )

            expected_files = {
                "merged.json",
                "summarized.txt",
                "prompt.md",
                "expected.md",
            }
            self.assertEqual(
                {path.name for path in output_dir.iterdir()},
                expected_files,
            )
            self.assertIn(
                "Do not run the network pipeline.",
                (output_dir / "prompt.md").read_text(),
            )
            self.assertIn(
                "# 🚀 Tech Digest - 2026-02-27",
                (output_dir / "expected.md").read_text(),
            )
            self.assertIn(
                "Total articles: 9",
                (output_dir / "summarized.txt").read_text(),
            )
```

- [ ] **Step 2: Run tests and verify failure**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: FAIL with `AttributeError: module 'render_acceptance_digest' has no attribute 'prepare_codex_acceptance_context'`.

- [ ] **Step 3: Add manual context support to the renderer**

In `scripts/render-acceptance-digest.py`, add this import near the top:

```python
import shutil
```

Add these functions after `render_digest`:

```python
def summarize_fixture(data: Dict[str, Any]) -> str:
    lines = ["=== Merged Data Summary ==="]
    stats = data.get("output_stats", {})
    lines.append(f"Total articles: {stats.get('total_articles', '?')}")
    lines.append(f"Topics: {', '.join(data.get('topics', {}).keys())}")
    lines.append("")

    for topic_id, topic_data in data.get("topics", {}).items():
        articles = topic_data.get("articles", [])
        if not isinstance(articles, list):
            continue
        lines.append(f"=== {topic_id} ({len(articles)} articles) ===")
        for index, article in enumerate(sorted_topic_articles(topic_data), 1):
            score = format_score(quality_score(article))
            lines.append(f"  [{index}] ({score}pts) [{article.get('source_type', '?')}] {article.get('title', '?')}")
            lines.append(f"      Source: {article.get('source_name', '?')}")
            link = article_link(article)
            if link:
                lines.append(f"      Link: {link}")
            snippet = article.get("snippet") or article.get("summary") or ""
            if snippet:
                lines.append(f"      Snippet: {snippet}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_codex_prompt(report_date: str, version: str) -> str:
    return f"""# Follow News Manual Acceptance Prompt

Generate a Markdown/Discord daily digest for {report_date} using the files in this directory.

Rules:
- Do not run the network pipeline.
- Use `merged.json` as the only merged data source.
- Use `summarized.txt` only as a reading aid.
- Follow the current Markdown/Discord format from `references/digest-prompt.md` and `references/templates/discord.md`.
- Keep the report date exactly `{report_date}`.
- Keep the version exactly `{version}`.
- Save the generated report as `actual.md` in this directory.

After writing `actual.md`, compare it with `expected.md`:

```bash
diff -u expected.md actual.md
```

The outputs do not need to be word-for-word identical for freeform summaries, but the title, section order, item format, source links, quality scores, fixed sections, and footer must match the acceptance contract.
"""


def prepare_codex_acceptance_context(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    source_fixture: Path,
    output_dir: Path,
    report_date: str,
    version: str,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source_fixture), str(output_dir / "merged.json"))
    (output_dir / "summarized.txt").write_text(summarize_fixture(data))
    (output_dir / "prompt.md").write_text(build_codex_prompt(report_date, version))
    (output_dir / "expected.md").write_text(
        render_digest(data, topic_defs, report_date, version)
    )
```

- [ ] **Step 4: Extend CLI arguments**

In `parse_args`, add this argument before `return parser.parse_args()`:

```python
parser.add_argument(
    "--prepare-codex-context",
    type=Path,
    default=None,
    help="Write merged.json, summarized.txt, prompt.md, and expected.md to this directory",
)
```

Replace `main` with:

```python
def main() -> int:
    args = parse_args()
    data = load_json(args.input)
    topic_defs = load_topic_definitions(args.topics)

    if args.prepare_codex_context:
        prepare_codex_acceptance_context(
            data=data,
            topic_defs=topic_defs,
            source_fixture=args.input,
            output_dir=args.prepare_codex_context,
            report_date=args.date,
            version=args.version,
        )
        return 0

    output = render_digest(data, topic_defs, args.date, args.version)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output)
    return 0
```

- [ ] **Step 5: Confirm the import block**

The final import block should include only imports used by the file:

```python
import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence
```

- [ ] **Step 6: Run manual context test**

Run:

```bash
python -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_prepare_manual_codex_context -v
```

Expected: PASS.

- [ ] **Step 7: Run CLI manual context smoke test**

Run:

```bash
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output /tmp/follow-news-acceptance/expected.md \
  --prepare-codex-context /tmp/follow-news-acceptance
```

Expected: exit code 0 and these files exist:

```bash
ls /tmp/follow-news-acceptance
```

Expected listing includes:

```text
expected.md
merged.json
prompt.md
summarized.txt
```

- [ ] **Step 8: Run full acceptance tests**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS.

- [ ] **Step 9: Commit manual context support**

```bash
git add scripts/render-acceptance-digest.py tests/test_acceptance_digest.py
git commit -m "test: add manual codex digest acceptance context"
```

## Task 6: Document Acceptance Commands

**Files:**
- Modify: `README.md`
- Modify: `README_CN.md`

- [ ] **Step 1: Add README acceptance section**

In `README.md`, add this section after the existing test command section:

```markdown
### Product Acceptance Test

The Markdown/Discord digest format has a deterministic golden acceptance test:

```bash
python -m unittest tests.test_acceptance_digest -v
```

When the digest format intentionally changes, update the golden file explicitly:

```bash
UPDATE_GOLDEN=1 python -m unittest tests.test_acceptance_digest -v
git diff -- tests/golden/daily-discord.md
```

To prepare a manual Codex acceptance context:

```bash
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output /tmp/follow-news-acceptance/expected.md \
  --prepare-codex-context /tmp/follow-news-acceptance
```
```

- [ ] **Step 2: Add README_CN acceptance section**

In `README_CN.md`, add this section after the existing test command section:

```markdown
### 产品验收测试

Markdown/Discord 日报格式有一个确定性的 golden 验收测试：

```bash
python -m unittest tests.test_acceptance_digest -v
```

当日报格式有意变化时，必须显式更新 golden 文件并 review diff：

```bash
UPDATE_GOLDEN=1 python -m unittest tests.test_acceptance_digest -v
git diff -- tests/golden/daily-discord.md
```

生成手动 Codex 验收上下文：

```bash
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output /tmp/follow-news-acceptance/expected.md \
  --prepare-codex-context /tmp/follow-news-acceptance
```
```

- [ ] **Step 3: Run acceptance tests after docs edit**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS.

- [ ] **Step 4: Commit docs**

```bash
git add README.md README_CN.md
git commit -m "docs: document digest acceptance workflow"
```

## Task 7: Final Verification

**Files:**
- Verify: all files changed in Tasks 1-6

- [ ] **Step 1: Run the targeted acceptance suite**

Run:

```bash
python -m unittest tests.test_acceptance_digest -v
```

Expected: PASS.

- [ ] **Step 2: Run the full test suite**

Run:

```bash
python -m unittest discover -s tests -v
```

Expected: PASS.

- [ ] **Step 3: Run golden update path and inspect diff**

Run:

```bash
UPDATE_GOLDEN=1 python -m unittest tests.test_acceptance_digest -v
git diff -- tests/golden/daily-discord.md
```

Expected: tests PASS and no golden diff if the renderer has not changed.

- [ ] **Step 4: Run manual context smoke test**

Run:

```bash
python scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-02-27 \
  --version 3.17.0 \
  --output /tmp/follow-news-acceptance/expected.md \
  --prepare-codex-context /tmp/follow-news-acceptance
diff -u /tmp/follow-news-acceptance/expected.md /tmp/follow-news-acceptance/expected.md
```

Expected: first command exits 0; second command exits 0 with no diff output.

- [ ] **Step 5: Review changed files**

Run:

```bash
git status --short
git diff --stat HEAD
git diff HEAD -- scripts/render-acceptance-digest.py tests/test_acceptance_digest.py tests/fixtures/acceptance-merged.json tests/golden/daily-discord.md README.md README_CN.md
```

Expected: only intended files are changed.

- [ ] **Step 6: Final commit if Task 7 produced changes**

If Task 7 only verified existing commits, do not create an empty commit. If Task 7 required a correction, commit the correction:

```bash
git add scripts/render-acceptance-digest.py tests/test_acceptance_digest.py tests/fixtures/acceptance-merged.json tests/golden/daily-discord.md README.md README_CN.md
git commit -m "test: finalize digest acceptance workflow"
```

## Self-Review

- Spec coverage:
  - Default deterministic Markdown/Discord acceptance test: Tasks 1-4.
  - Fixed fixture and date: Tasks 1-3.
  - Golden file and explicit update gate: Tasks 3-4.
  - Manual Codex acceptance context: Task 5.
  - Documentation and verification commands: Tasks 6-7.
  - Non-goals preserved: no Email HTML/PDF, no network pipeline, no LLM call in CI, no delivery actions.

- Placeholder scan:
  - The plan contains no deferred implementation markers.
  - Each code-changing step includes exact content or exact replacement snippets.

- Type consistency:
  - `render_digest`, `load_topic_definitions`, and `prepare_codex_acceptance_context` names are consistent across tests, CLI, and renderer steps.
  - Fixture property names match renderer reads: `input_sources`, `output_stats`, `topics`, `quality_score`, `source_type`, `metrics`, `repo`, `tag_name`, `daily_stars_est`, `is_blog_pick`, `transcript_status`, and `transcript`.
