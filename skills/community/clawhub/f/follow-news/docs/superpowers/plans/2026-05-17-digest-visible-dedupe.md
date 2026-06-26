# Digest Visible Dedupe Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ensure each article is visible at most once in a generated digest, with topic sections taking precedence over fixed sections.

**Architecture:** Add a digest-scoped visible article registry inside the deterministic acceptance renderer. Topic renderers mark articles only after they actually render them; fixed-section renderers filter and mark unseen articles before rendering. Keep merge output, scoring, ordering, and source collection unchanged.

**Tech Stack:** Python 3.8 standard library, `unittest`, existing `scripts/render-acceptance-digest.py`, existing `tests/test_acceptance_digest.py`.

---

## File Structure

- Modify: `scripts/render-acceptance-digest.py`
  - Owns deterministic acceptance rendering for Discord and chat outputs.
  - Add stable visible dedupe keys, URL/title normalization helpers, and a small registry.
  - Thread the registry through topic and fixed-section renderers.

- Modify: `tests/test_acceptance_digest.py`
  - Add regression tests for stable key generation.
  - Add final-output tests proving topic sections win over KOL, Blog Picks, and Podcast Remix fixed sections.
  - Cover both Discord and chat render paths.

- No changes: `scripts/merge-sources.py`
  - Existing merge-level dedupe remains unchanged.

- No changes: `references/digest-prompt.md` or templates
  - This task enforces the renderer behavior already captured in the approved design.

## Task 1: Add Visible Dedupe Regression Tests

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add a shared duplicate fixture helper**

Insert this helper after `render_daily_chat_digest()`:

```python
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
```

- [ ] **Step 2: Add stable key tests**

Insert this test class after `class TestAcceptanceFixture(unittest.TestCase):`:

```python
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

    def test_article_dedupe_key_falls_back_to_normalized_title(self):
        first = {"title": "RT @user: OpenAI releases GPT-5!"}
        second = {"title": "OpenAI releases GPT-5"}

        self.assertEqual(
            render_mod.article_dedupe_key(first),
            render_mod.article_dedupe_key(second),
        )

    def test_article_dedupe_key_returns_none_without_url_or_title(self):
        self.assertIsNone(render_mod.article_dedupe_key({"source_type": "rss"}))
```

- [ ] **Step 3: Add Discord final-output dedupe test**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_render_digest_uses_current_discord_structure`:

```python
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
```

- [ ] **Step 4: Add chat final-output dedupe test**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after the Discord dedupe test:

```python
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
```

- [ ] **Step 5: Run the new tests and verify they fail for the expected reason**

Run:

```bash
python3 -m unittest \
  tests.test_acceptance_digest.TestVisibleArticleDedupe \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_visible_dedupe_keeps_topic_sections_over_fixed_sections \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_visible_dedupe_keeps_topic_sections_over_fixed_sections \
  -v
```

Expected: `ERROR` for missing `render_mod.article_dedupe_key`, or `FAIL` showing duplicate fixed-section links still render. Both outcomes confirm the tests cover missing behavior.

- [ ] **Step 6: Commit the failing tests**

Run:

```bash
git add tests/test_acceptance_digest.py
git commit -m "test: cover digest visible dedupe"
```

Expected: commit succeeds.

## Task 2: Add Stable Visible Dedupe Helpers

**Files:**
- Modify: `scripts/render-acceptance-digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Update imports**

Change the imports at the top of `scripts/render-acceptance-digest.py` from:

```python
import argparse
import json
import math
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence
```

to:

```python
import argparse
import json
import math
import re
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence
from urllib.parse import parse_qs, urlparse
```

- [ ] **Step 2: Add URL/title normalization and registry helpers**

Insert this block after `article_link()`:

```python
def normalize_visible_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.rstrip("/")

        if domain in {"youtube.com", "m.youtube.com"} and path == "/watch":
            video_id = parse_qs(parsed.query).get("v", [""])[0]
            if video_id:
                return f"url:youtube:{video_id}"

        if domain == "youtu.be" and path:
            video_id = path.lstrip("/")
            if video_id:
                return f"url:youtube:{video_id}"

        if domain or path:
            return f"url:{domain}{path}"
    except Exception:
        pass

    compact = " ".join(str(url).split())
    return f"url:{compact}" if compact else ""


def normalize_visible_title(title: Any) -> str:
    if not title:
        return ""

    value = str(title)
    value = re.sub(r"^(RT\s+@\w+:\s*)", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*[|\-–]\s*[^|]*$", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"[^\w\s]", "", value.lower())
    return value


def article_dedupe_key(article: Dict[str, Any]) -> Optional[str]:
    url = article_link(article)
    if url:
        normalized_url = normalize_visible_url(url)
        if normalized_url:
            return normalized_url

    normalized_title = normalize_visible_title(article.get("title"))
    if normalized_title:
        return f"title:{normalized_title}"

    return None


class VisibleArticleRegistry:
    def __init__(self) -> None:
        self.seen_keys = set()

    def is_seen(self, article: Dict[str, Any]) -> bool:
        key = article_dedupe_key(article)
        return bool(key and key in self.seen_keys)

    def mark(self, article: Dict[str, Any]) -> None:
        key = article_dedupe_key(article)
        if key:
            self.seen_keys.add(key)

    def filter_unseen(self, articles: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        visible = []
        for article in articles:
            if self.is_seen(article):
                continue
            self.mark(article)
            visible.append(article)
        return visible
```

- [ ] **Step 3: Run stable key tests and verify they pass**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestVisibleArticleDedupe -v
```

Expected: `OK`.

- [ ] **Step 4: Run final-output dedupe tests and verify they still fail**

Run:

```bash
python3 -m unittest \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_visible_dedupe_keeps_topic_sections_over_fixed_sections \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_visible_dedupe_keeps_topic_sections_over_fixed_sections \
  -v
```

Expected: `FAIL` because topic and fixed renderers do not use the registry yet.

- [ ] **Step 5: Commit helper implementation**

Run:

```bash
git add scripts/render-acceptance-digest.py
git commit -m "feat: add visible article dedupe keys"
```

Expected: commit succeeds.

## Task 3: Wire Visible Dedupe Through Discord Rendering

**Files:**
- Modify: `scripts/render-acceptance-digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Update Discord topic renderer signature and marking**

Change `render_topic_sections` signature from:

```python
def render_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
) -> List[str]:
```

to:

```python
def render_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    visible_registry: VisibleArticleRegistry,
) -> List[str]:
```

Inside the `for article in articles:` loop, add `visible_registry.mark(article)` after the link line and optional multi-source line are appended:

```python
        for article in articles:
            score = format_score(quality_score(article))
            lines.append(f"• 🔥{score} | {article.get('title', '?')}")
            lines.append(render_link(article_link(article)))
            if article.get("multi_source"):
                lines.append(f"  *[{article.get('source_count', 2)} sources]*")
            visible_registry.mark(article)
            lines.append("")
```

- [ ] **Step 2: Update Discord fixed renderers to accept and apply the registry**

For each fixed renderer, add a `visible_registry: VisibleArticleRegistry` parameter and call `visible_registry.filter_unseen(...)` after sorting.

Use these exact function headers:

```python
def render_kol_updates(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_github_releases(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_github_trending(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_blog_picks(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_podcast_remix(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

In `render_kol_updates`, replace:

```python
    tweets = sorted(tweets, key=quality_score, reverse=True)
```

with:

```python
    tweets = sorted(tweets, key=quality_score, reverse=True)
    tweets = visible_registry.filter_unseen(tweets)
    if not tweets:
        return None
```

In `render_github_releases`, replace:

```python
    releases = sorted(releases, key=quality_score, reverse=True)
```

with:

```python
    releases = sorted(releases, key=quality_score, reverse=True)
    releases = visible_registry.filter_unseen(releases)
    if not releases:
        return None
```

In `render_github_trending`, replace:

```python
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
```

with:

```python
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    repos = visible_registry.filter_unseen(repos)
    if not repos:
        return None
```

In `render_blog_picks`, replace:

```python
    picks = sorted(picks, key=quality_score, reverse=True)
```

with:

```python
    picks = sorted(picks, key=quality_score, reverse=True)
    picks = visible_registry.filter_unseen(picks)
    if not picks:
        return None
```

In `render_podcast_remix`, replace:

```python
    episodes = sorted(episodes, key=quality_score, reverse=True)
```

with:

```python
    episodes = sorted(episodes, key=quality_score, reverse=True)
    episodes = visible_registry.filter_unseen(episodes)
    if not episodes:
        return None
```

- [ ] **Step 3: Update `render_digest` to create and pass the registry**

In `render_digest`, replace:

```python
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_topic_sections(data, topic_defs))
```

with:

```python
    visible_registry = VisibleArticleRegistry()
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_topic_sections(data, topic_defs, visible_registry))
```

Then replace:

```python
        section = renderer(data)
```

with:

```python
        section = renderer(data, visible_registry)
```

- [ ] **Step 4: Run Discord dedupe test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_visible_dedupe_keeps_topic_sections_over_fixed_sections -v
```

Expected: `OK`.

- [ ] **Step 5: Run existing Discord acceptance tests and verify they pass**

Run:

```bash
python3 -m unittest \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_digest_matches_golden \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_digest_structure_contract \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_render_digest_uses_current_discord_structure \
  -v
```

Expected: `OK`.

- [ ] **Step 6: Commit Discord wiring**

Run:

```bash
git add scripts/render-acceptance-digest.py
git commit -m "feat: dedupe visible discord digest items"
```

Expected: commit succeeds.

## Task 4: Wire Visible Dedupe Through Chat Rendering

**Files:**
- Modify: `scripts/render-acceptance-digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Update chat topic renderer signature and marking**

Change `render_chat_topic_sections` signature from:

```python
def render_chat_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
) -> List[str]:
```

to:

```python
def render_chat_topic_sections(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    visible_registry: VisibleArticleRegistry,
) -> List[str]:
```

Inside the `for index, article in enumerate(articles, 1):` loop, add `visible_registry.mark(article)` immediately after appending the rendered item:

```python
        for index, article in enumerate(articles, 1):
            lines.append(render_chat_item(article, index, emoji))
            visible_registry.mark(article)
            lines.append("")
```

- [ ] **Step 2: Update chat fixed renderers to accept and apply the registry**

For each chat fixed renderer, add a `visible_registry: VisibleArticleRegistry` parameter and call `visible_registry.filter_unseen(...)` after sorting and before rendering.

Use these exact function headers:

```python
def render_chat_kol_updates(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_chat_github_releases(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_chat_github_trending(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_chat_blog_picks(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

```python
def render_chat_podcast_remix(
    data: Dict[str, Any],
    visible_registry: VisibleArticleRegistry,
) -> Optional[str]:
```

In `render_chat_kol_updates`, replace:

```python
    tweets = sorted(tweets, key=quality_score, reverse=True)
```

with:

```python
    tweets = sorted(tweets, key=quality_score, reverse=True)
    tweets = visible_registry.filter_unseen(tweets)
    if not tweets:
        return None
```

In `render_chat_github_releases`, replace:

```python
    releases = sorted(releases, key=quality_score, reverse=True)
    return render_chat_article_section("## 📦 GitHub Releases", "📦", releases)
```

with:

```python
    releases = sorted(releases, key=quality_score, reverse=True)
    releases = visible_registry.filter_unseen(releases)
    return render_chat_article_section("## 📦 GitHub Releases", "📦", releases)
```

In `render_chat_github_trending`, replace:

```python
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    return render_chat_article_section("## 🐙 GitHub Trending", "🐙", repos)
```

with:

```python
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    repos = visible_registry.filter_unseen(repos)
    return render_chat_article_section("## 🐙 GitHub Trending", "🐙", repos)
```

In `render_chat_blog_picks`, replace:

```python
    picks = sorted(picks, key=quality_score, reverse=True)
    return render_chat_article_section("## 📝 Blog Picks", "📝", picks)
```

with:

```python
    picks = sorted(picks, key=quality_score, reverse=True)
    picks = visible_registry.filter_unseen(picks)
    return render_chat_article_section("## 📝 Blog Picks", "📝", picks)
```

In `render_chat_podcast_remix`, replace:

```python
    episodes = sorted(episodes, key=quality_score, reverse=True)
    return render_chat_article_section("## 🎙️ Podcast Remix", "🎙️", episodes)
```

with:

```python
    episodes = sorted(episodes, key=quality_score, reverse=True)
    episodes = visible_registry.filter_unseen(episodes)
    return render_chat_article_section("## 🎙️ Podcast Remix", "🎙️", episodes)
```

- [ ] **Step 3: Update `render_chat_digest` to create and pass the registry**

In `render_chat_digest`, replace:

```python
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_chat_topic_sections(data, topic_defs))
```

with:

```python
    visible_registry = VisibleArticleRegistry()
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_chat_topic_sections(data, topic_defs, visible_registry))
```

Then replace:

```python
        section = renderer(data)
```

with:

```python
        section = renderer(data, visible_registry)
```

- [ ] **Step 4: Run chat dedupe test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_visible_dedupe_keeps_topic_sections_over_fixed_sections -v
```

Expected: `OK`.

- [ ] **Step 5: Run existing chat acceptance tests and verify they pass**

Run:

```bash
python3 -m unittest \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_chat_digest_matches_golden \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_chat_digest_structure_contract \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_cli_can_render_chat_template \
  -v
```

Expected: `OK`.

- [ ] **Step 6: Commit chat wiring**

Run:

```bash
git add scripts/render-acceptance-digest.py
git commit -m "feat: dedupe visible chat digest items"
```

Expected: commit succeeds.

## Task 5: Full Verification

**Files:**
- Verify: `scripts/render-acceptance-digest.py`
- Verify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Run acceptance renderer tests**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest -v
```

Expected: `OK`.

- [ ] **Step 2: Run merge tests to guard shared normalization assumptions**

Run:

```bash
python3 -m unittest tests.test_merge -v
```

Expected: `OK`.

- [ ] **Step 3: Run the full test suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: `OK`.

- [ ] **Step 4: Check final diff**

Run:

```bash
git diff --stat HEAD
git diff -- scripts/render-acceptance-digest.py tests/test_acceptance_digest.py
```

Expected: the diff only contains visible dedupe tests and renderer changes. No fetchers, merge scoring, prompt templates, or unrelated docs are changed.

- [ ] **Step 5: Commit final verification notes if any tracked files changed**

If Task 5 produced no file changes, do not commit. If a small correction was required during verification, run:

```bash
git add scripts/render-acceptance-digest.py tests/test_acceptance_digest.py
git commit -m "test: verify digest visible dedupe"
```

Expected: commit succeeds only when there are actual staged changes.

## Self-Review

- Spec coverage: Task 1 covers stable key and final visible duplicate behavior. Tasks 2-4 implement URL/title keys, topic-first registration, fixed-section filtering, and both Discord/chat paths. Task 5 covers acceptance, merge, and full-suite verification.
- Scope check: The plan does not modify fetchers, merge scoring, topic assignment, prompts, or templates. Event-level semantic dedupe remains outside this first implementation stage.
- Placeholder scan: The plan contains concrete file paths, commands, expected outcomes, and code snippets for every code-changing step.
- Type consistency: The helper names used in tests match the implementation names: `article_dedupe_key`, `VisibleArticleRegistry`, and `filter_unseen`.
