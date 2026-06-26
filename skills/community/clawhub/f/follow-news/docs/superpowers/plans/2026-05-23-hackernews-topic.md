# Hacker News Topic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a first-class `hackernews` topic so Hacker News stories render only in a dedicated Hacker News section.

**Architecture:** Keep topic routing config-driven by adding `hackernews` to default topics and moving the `hn-rss` source from `frontier-tech` to `hackernews`. Extend the digest renderer with a topic-specific presentation path for `hackernews` that shows the Hacker News frontpage Top 10 by `hn_rank`, including HN score, comments, discussion link, and external article link while preserving the existing fixed Hacker News fallback for legacy merged inputs.

**Tech Stack:** Python 3 standard library, `unittest`, JSON config files, Markdown docs.

---

## File Structure

- Modify `config/defaults/topics.json`: add the `hackernews` topic before `frontier-tech`.
- Modify `config/defaults/sources.json`: change `hn-rss.topics` to `["hackernews"]`.
- Modify `scripts/render-acceptance-digest.py`: add HN topic-specific Top 10 selection and rendering in both Discord and chat topic sections.
- Modify `tests/test_config.py`: require `hackernews` and assert HN source routing.
- Modify `tests/test_acceptance_digest.py`: assert default grouping, no duplicate output, Top 10 limit, and HN topic rendering contracts.
- Modify `README.md`, `README_CN.md`, `SKILL.md`, and `scripts/test-pipeline.sh`: update default topic count/list references.
- Modify `tests/golden/daily-discord.md` and `tests/golden/daily-chat.md` only if the golden fixture output changes after running acceptance tests.

## Task 1: Add Failing Config And Routing Tests

**Files:**
- Modify: `tests/test_config.py`
- Modify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Update required topic tests**

In `tests/test_config.py`, change:

```python
REQUIRED_TOPICS = {"llm", "ai-agent", "kol", "frontier-tech", "podcast"}
```

to:

```python
REQUIRED_TOPICS = {
    "llm",
    "ai-agent",
    "kol",
    "hackernews",
    "frontier-tech",
    "podcast",
}
```

- [ ] **Step 2: Add source routing test**

Add this method to `TestLoadTopics` in `tests/test_config.py`, near the other source/topic validation tests:

```python
    def test_hacker_news_source_uses_hackernews_topic_only(self):
        sources = load_merged_sources(DEFAULTS_DIR)
        hn_sources = [source for source in sources if source.get("id") == "hn-rss"]

        self.assertEqual(len(hn_sources), 1)
        self.assertEqual(hn_sources[0].get("topics"), ["hackernews"])
```

- [ ] **Step 3: Add default grouping test**

Add this method to `TestAcceptanceRenderer` in `tests/test_acceptance_digest.py`, near the existing default topic grouping tests:

```python
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
```

- [ ] **Step 4: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_config.TestLoadTopics.test_hacker_news_source_uses_hackernews_topic_only tests.test_acceptance_digest.TestAcceptanceRenderer.test_default_topics_route_hacker_news_to_hackernews_only -v
```

Expected: at least `test_hacker_news_source_uses_hackernews_topic_only` fails because `hn-rss` still uses `["frontier-tech"]`. The grouping test may fail because `hackernews` is not in default topics yet.

- [ ] **Step 5: Commit failing tests**

```bash
git add tests/test_config.py tests/test_acceptance_digest.py
git commit -m "test: cover Hacker News topic routing"
```

## Task 2: Add Default `hackernews` Topic And Route HN Source

**Files:**
- Modify: `config/defaults/topics.json`
- Modify: `config/defaults/sources.json`
- Modify: `README.md`
- Modify: `README_CN.md`
- Modify: `SKILL.md`
- Modify: `scripts/test-pipeline.sh`

- [ ] **Step 1: Add topic definition**

In `config/defaults/topics.json`, insert this object after `kol` and before `frontier-tech`:

```json
    {
      "id": "hackernews",
      "emoji": "📰",
      "label": "Hacker News / 热榜",
      "description": "Top stories from Hacker News frontpage with HN score, comments, and discussion links",
      "search": {
        "queries": [],
        "twitter_queries": [],
        "must_include": [],
        "exclude": []
      },
      "display": {
        "max_items": 10,
        "style": "compact"
      }
    },
```

- [ ] **Step 2: Move `hn-rss` to `hackernews`**

In `config/defaults/sources.json`, change the `hn-rss` source topics from:

```json
      "topics": [
        "frontier-tech"
      ],
```

to:

```json
      "topics": [
        "hackernews"
      ],
```

- [ ] **Step 3: Update README topic counts and lists**

Update `README.md`:

```markdown
> Automated tech news digest — 163 built-in sources, 7-source pipeline, one chat message to install.
```

stays unchanged.

Keep count-derived references at 6 topics after the new topic is added, for example:

```markdown
plus **6 web search topics**
```

Ensure every default topic list includes:

```markdown
`llm`, `ai-agent`, `kol`, `hackernews`, `frontier-tech`, `podcast`
```

Update `README_CN.md` similarly with:

```markdown
`llm`、`ai-agent`、`kol`、`hackernews`、`frontier-tech`、`podcast`
```

- [ ] **Step 4: Update SKILL and test-pipeline topic examples**

Search:

```bash
rg -n "llm|ai-agent|kol|frontier-tech|podcast|topics" SKILL.md scripts/test-pipeline.sh
```

For each default topic list, include `hackernews` in the same order as `topics.json`:

```text
llm, ai-agent, kol, hackernews, frontier-tech, podcast
```

- [ ] **Step 5: Run config tests**

Run:

```bash
python3 -m unittest tests.test_config -v
```

Expected: all config tests pass. If documentation tests fail, update the exact stale documentation strings they report.

- [ ] **Step 6: Run routing tests**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_default_topics_route_hacker_news_to_hackernews_only -v
```

Expected: the routing test passes.

- [ ] **Step 7: Commit config and docs**

```bash
git add config/defaults/topics.json config/defaults/sources.json README.md README_CN.md SKILL.md scripts/test-pipeline.sh tests/test_config.py tests/test_acceptance_digest.py
git commit -m "feat: add Hacker News topic"
```

## Task 3: Add Failing HN Topic Rendering Tests

**Files:**
- Modify: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add chat rendering test**

Add this method near `test_chat_hacker_news_top_uses_fixed_numbered_shape`:

```python
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
```

- [ ] **Step 2: Add chat Top 10 and dedupe test**

Add this method near the chat HN topic rendering test:

```python
    def test_chat_hackernews_topic_renders_ranked_top_ten_without_duplicates(self):
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
        articles.append(
            {
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
        )
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

        self.assertIn(render_mod.bold_chat_title_text("HN ranked story 1"), text)
        self.assertIn(render_mod.bold_chat_title_text("HN ranked story 10"), text)
        self.assertNotIn(render_mod.bold_chat_title_text("HN ranked story 11"), text)
        self.assertEqual(text.count(render_mod.bold_chat_title_text("HN ranked story 3")), 1)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("https://mirror.example.com/story-3", text)
```

The HN discussion URL must appear once, and the duplicate mirror URL must not appear.

- [ ] **Step 3: Add Discord rendering test**

Add this method near the existing Discord HN tests:

```python
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
```

- [ ] **Step 4: Add Discord Top 10 and dedupe test**

Add this method near the Discord HN topic rendering test:

```python
    def test_discord_hackernews_topic_renders_ranked_top_ten_without_duplicates(self):
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
        articles.append(
            {
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
        )
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

        self.assertIn("HN ranked story 1", text)
        self.assertIn("HN ranked story 10", text)
        self.assertNotIn("HN ranked story 11", text)
        self.assertEqual(text.count("HN ranked story 3"), 1)
        self.assertEqual(text.count("https://news.ycombinator.com/item?id=3"), 1)
        self.assertNotIn("https://mirror.example.com/story-3", text)
```

- [ ] **Step 5: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_hackernews_topic_renders_hn_metadata_and_links tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_hackernews_topic_renders_ranked_top_ten_without_duplicates tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_hackernews_topic_renders_hn_metadata_and_links tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_hackernews_topic_renders_ranked_top_ten_without_duplicates -v
```

Expected: all four tests fail because the generic topic renderer does not yet show HN metadata, does not cap the HN topic to ranked Top 10, and currently links to the external article rather than the HN discussion URL.

- [ ] **Step 6: Commit failing rendering tests**

```bash
git add tests/test_acceptance_digest.py
git commit -m "test: cover Hacker News topic rendering"
```

## Task 4: Implement HN Topic Rendering

**Files:**
- Modify: `scripts/render-acceptance-digest.py`

- [ ] **Step 1: Add topic predicate**

Add this helper near the existing Hacker News helpers:

```python
def is_hackernews_topic(topic_id: Any) -> bool:
    return compact_text(topic_id).lower() == "hackernews"
```

- [ ] **Step 2: Add HN topic Top 10 selector**

Add these helpers near `select_hacker_news_top_articles`:

```python
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
        if is_hacker_news_article(article)
        and has_hacker_news_metadata(article)
        and (hacker_news_url(article) or hacker_news_article_url(article))
    ]
    topic_registry = VisibleArticleRegistry()
    return topic_registry.filter_unseen_limited(
        sorted(eligible, key=hackernews_topic_sort_key),
        HN_DEFAULT_LIMIT,
    )
```

This selector is intentionally separate from `select_hacker_news_top_articles`. The new `hackernews` topic means frontpage Top 10 by `hn_rank`; the old fixed fallback keeps its existing score-first behavior for legacy inputs. The local `VisibleArticleRegistry` ensures duplicates do not consume a Top 10 slot.

- [ ] **Step 3: Add Discord HN topic item renderer**

Add this helper near `render_hacker_news_top`:

```python
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
```

- [ ] **Step 4: Use HN selector and renderer in Discord topic sections**

In `render_topic_sections`, replace:

```python
        articles = sorted_topic_articles(topic_data)
        articles = visible_registry.filter_unseen(articles)
```

with:

```python
        if is_hackernews_topic(topic_id):
            articles = select_hackernews_topic_articles(topic_data.get("articles", []))
        else:
            articles = sorted_topic_articles(topic_data)
        articles = visible_registry.filter_unseen(articles)
```

In `render_topic_sections`, replace the article loop:

```python
        for article in articles:
            lines.append(f"• {article.get('title', '?')}")
            lines.append(render_link(article_link(article)))
            if article.get("multi_source"):
                lines.append(f"  *[{article.get('source_count', 2)} sources]*")
            lines.append("")
```

with:

```python
        for article in articles:
            if is_hackernews_topic(topic_id) and is_hacker_news_article(article):
                lines.extend(render_hackernews_topic_item(article))
            else:
                lines.append(f"• {article.get('title', '?')}")
                lines.append(render_link(article_link(article)))
                if article.get("multi_source"):
                    lines.append(f"  *[{article.get('source_count', 2)} sources]*")
            lines.append("")
```

- [ ] **Step 5: Add chat HN topic item renderer**

Add this helper near `render_chat_hacker_news_top`:

```python
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
```

- [ ] **Step 6: Use HN selector and renderer in chat topic sections**

In `render_chat_topic_sections`, replace:

```python
        articles = chat_topic_articles(topic_data)
        articles = visible_registry.filter_unseen(articles)
```

with:

```python
        if is_hackernews_topic(topic_id):
            articles = select_hackernews_topic_articles(topic_data.get("articles", []))
        else:
            articles = chat_topic_articles(topic_data)
        articles = visible_registry.filter_unseen(articles)
```

In `render_chat_topic_sections`, replace:

```python
        for index, article in enumerate(articles, 1):
            lines.append(render_chat_item(article, index, emoji))
            lines.append("")
```

with:

```python
        for index, article in enumerate(articles, 1):
            if is_hackernews_topic(topic_id) and is_hacker_news_article(article):
                lines.extend(render_chat_hackernews_topic_item(article, index, emoji))
            else:
                lines.append(render_chat_item(article, index, emoji))
            lines.append("")
```

- [ ] **Step 7: Run rendering tests**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_hackernews_topic_renders_hn_metadata_and_links tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_hackernews_topic_renders_ranked_top_ten_without_duplicates tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_hackernews_topic_renders_hn_metadata_and_links tests.test_acceptance_digest.TestAcceptanceRenderer.test_discord_hackernews_topic_renders_ranked_top_ten_without_duplicates tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_hacker_news_top_uses_fixed_numbered_shape tests.test_acceptance_digest.TestAcceptanceRenderer.test_hacker_news_top_renders_top_ten_plus_ai_related_top_twenty -v
```

Expected: all listed tests pass. The old fixed-section tests must keep passing because they use `topic_defs=[]`, so the fixed fallback still renders legacy HN input.

- [ ] **Step 8: Commit renderer implementation**

```bash
git add scripts/render-acceptance-digest.py tests/test_acceptance_digest.py
git commit -m "feat: render Hacker News topic metadata"
```

## Task 5: Update Goldens And Run Verification

**Files:**
- Modify: `tests/golden/daily-discord.md` if output changes.
- Modify: `tests/golden/daily-chat.md` if output changes.

- [ ] **Step 1: Run acceptance tests**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest -v
```

Expected: if golden tests fail, failures point to `daily-discord.md` or `daily-chat.md` differences. Non-golden behavior tests should pass.

- [ ] **Step 2: Update goldens if required**

If and only if golden tests fail because expected digest structure intentionally changed, run:

```bash
UPDATE_GOLDEN=1 python3 -m unittest tests.test_acceptance_digest -v
```

Expected: tests pass and golden files are rewritten.

- [ ] **Step 3: Review golden diffs**

Run:

```bash
git diff -- tests/golden/daily-discord.md tests/golden/daily-chat.md
```

Expected: diffs show only intended Hacker News topic placement or metadata rendering changes.

- [ ] **Step 4: Run config tests**

Run:

```bash
python3 -m unittest tests.test_config -v
```

Expected: all tests pass, including documentation count checks.

- [ ] **Step 5: Run full test suite**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 6: Generate a local digest smoke sample**

Use the existing merged output from the previous run to smoke-test rendering with current defaults:

```bash
python3 scripts/render-acceptance-digest.py \
  --input workspace/reports/daily-2026-05-23-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-05-23 \
  --version 3.17.5 \
  --template chat \
  --output workspace/reports/daily-2026-05-23-chat-hackernews-topic.md
```

Expected: command exits 0 and writes the smoke sample.

- [ ] **Step 7: Inspect smoke sample**

Run:

```bash
rg -n "Hacker News / 热榜|Tech Industry / 产业动态|Lawmakers Demand Answers|Models.dev" workspace/reports/daily-2026-05-23-chat-hackernews-topic.md
```

Expected:

- `Hacker News / 热榜` appears.
- HN stories such as `Lawmakers Demand Answers` and `Models.dev` appear under the HN section.
- Those HN stories do not appear under `Tech Industry / 产业动态`.

- [ ] **Step 8: Commit goldens and verification-related changes**

```bash
git add tests/golden/daily-discord.md tests/golden/daily-chat.md
git commit -m "test: update digest goldens for Hacker News topic"
```

If no golden files changed, skip this commit.

## Self-Review

- Spec coverage: Tasks cover topic definition, source routing, HN-only grouping, HN-specific metadata rendering, fallback compatibility, docs, and verification.
- Placeholder scan: The plan contains no `TBD`, `TODO`, or undefined follow-up tasks.
- Type consistency: Helper names used in tests and implementation steps are consistent: `is_hackernews_topic`, `render_hackernews_topic_item`, and `render_chat_hackernews_topic_item`.
