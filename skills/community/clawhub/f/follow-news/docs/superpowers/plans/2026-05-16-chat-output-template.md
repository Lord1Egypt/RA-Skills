# Chat Output Template Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a stable `chat` output template for Telegram, Feishu, WeChat, and similar IM channels, using title, compact summary, and `🔗 URL` per news item.

**Architecture:** Keep existing Discord rendering as the default path and add `chat` as an explicit template mode in the acceptance renderer. The `chat` path shares topic filtering, ordering, footer stats, and fixture loading with Discord, but owns its own item layout and summary selection helpers. Prompt and template docs make `chat` available to the LLM-based report generation path without introducing platform-specific Telegram, Feishu, or WeChat variants.

**Tech Stack:** Python standard library, `unittest`, Markdown reference templates, JSON acceptance fixture, golden-file tests.

---

## Current Worktree Note

The current worktree already contains uncommitted edits that change Discord links from `<URL>` to `🔗 URL`. Those edits are outside this plan's main goal. Before executing this plan, either commit those edits as a separate change or keep them unstaged and stage only files touched by each task.

This plan assumes implementation happens in:

```bash
cd /Users/tangwz/workspace/git/tech-news/.worktrees/codex-output-content-enrichment
```

## File Structure

- Create: `references/templates/chat.md`
  - Defines the user-facing `chat` template contract, fixed item shape, summary rules, link format, and examples.
- Modify: `references/digest-prompt.md`
  - Adds `chat` to `<TEMPLATE>` values and points chat output to `references/templates/chat.md`.
- Modify: `scripts/render-acceptance-digest.py`
  - Adds `--template discord|chat`.
  - Keeps `discord` as default.
  - Adds `render_chat_digest()` and small pure helpers for chat score formatting, summary material selection, and fixed-section rendering.
- Modify: `tests/fixtures/acceptance-merged.json`
  - Adds deterministic `chat_summary` fields for the acceptance sample so golden output can be stable while still representing Chinese summaries.
- Modify: `tests/test_acceptance_digest.py`
  - Adds chat rendering helper, golden test, structure contract test, filtering tests, source-boundary tests, CLI coverage, and invalid-score coverage.
- Create: `tests/golden/daily-chat.md`
  - Locks the expected chat layout.
- Keep: `tests/golden/daily-discord.md`
  - Existing Discord golden remains covered by existing tests. If the separate direct-link Discord change is kept, update and commit it separately.

## Task 1: Add Failing Chat Acceptance Tests

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add chat golden path and render helper**

Insert after `DAILY_GOLDEN = GOLDEN_DIR / "daily-discord.md"`:

```python
DAILY_CHAT_GOLDEN = GOLDEN_DIR / "daily-chat.md"
```

Insert after `render_daily_digest()`:

```python
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
```

- [ ] **Step 2: Add chat golden and structure tests**

Insert inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_daily_digest_matches_golden`:

```python
    def test_daily_chat_digest_matches_golden(self):
        assert_or_update_golden(self, DAILY_CHAT_GOLDEN, render_daily_chat_digest())

    def test_daily_chat_digest_structure_contract(self):
        text = render_daily_chat_digest()
        lines = text.splitlines()

        self.assertTrue(text.startswith("# 🚀 Tech Digest - 2026-02-27\n"))
        self.assertIn("## 🧠 LLM / Large Models", text)
        self.assertIn("1. 🧠 [9/10] OpenAI ships structured agent evaluation suite", text)
        self.assertIn("🔗 https://openai.com/research/agent-evals", text)
        self.assertIn("## 📦 GitHub Releases", text)
        self.assertIn("## 🐙 GitHub Trending", text)
        self.assertNotIn("<https://", text)
        self.assertNotIn("Low scoring model rumor should not render", text)

        title_lines = [
            line
            for line in lines
            if re.match(r"^[0-9]+\. .+ \[[0-9]+(?:\.[0-9]+)?/10\] .+", line)
        ]
        self.assertGreater(len(title_lines), 0)

        for index, line in enumerate(lines):
            if not re.match(r"^[0-9]+\. .+ \[[0-9]+(?:\.[0-9]+)?/10\] .+", line):
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
                r"(?m)^[0-9]+\. .+ \[[0-9]+(?:\.[0-9]+)?/10\] .+",
                lines[start],
            )
```

- [ ] **Step 3: Add filtering, source-boundary, and invalid-score tests**

Insert inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_daily_chat_digest_structure_contract`:

```python
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
                            "quality_score": "NaN",
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
        self.assertIn("1. 🤖 [0/10] Visible agent item", text)
        self.assertIn("🔗 https://example.com/agent", text)

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

        self.assertIn("Only this snippet is available.", text)
        self.assertNotIn("announced", text.lower())
        self.assertNotIn("released", text.lower())

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
        self.assertNotIn("Quote:", text)
        self.assertNotIn("guest", text.lower())
        self.assertNotIn("argues", text.lower())

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
        self.assertNotIn("12.5K", text)
        self.assertNotIn("views", text.lower())
```

- [ ] **Step 4: Add CLI chat template test**

Insert inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_cli_prepare_codex_context_does_not_require_output`:

```python
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
            self.assertIn("1. 🧠 [9/10] OpenAI ships structured agent evaluation suite", text)
            self.assertIn("🔗 https://openai.com/research/agent-evals", text)
            self.assertNotIn("<https://", text)
```

- [ ] **Step 5: Run tests to verify failure**

Run:

```bash
python3 -m unittest tests/test_acceptance_digest.py -v
```

Expected: FAIL because `render_digest()` does not yet accept `template="chat"` and `tests/golden/daily-chat.md` does not exist.

- [ ] **Step 6: Commit failing tests**

```bash
git add tests/test_acceptance_digest.py
git commit -m "test: cover chat digest output contract"
```

## Task 2: Add Deterministic Chat Fixture Summaries

**Files:**
- Modify: `tests/fixtures/acceptance-merged.json`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add deterministic chat summaries to the fixture**

For each visible article in `tests/fixtures/acceptance-merged.json`, add a `chat_summary` field next to the existing `snippet`, `summary`, `full_text`, or `description` field. Use these exact values:

```json
"chat_summary": "OpenAI 发布了一套面向 Agent 可靠性的结构化评测，用来覆盖工具调用和长周期任务等场景。这个条目同时来自 OpenAI Blog、Hacker News 和 r/OpenAI，说明它既有官方信息源，也引发了开发者社区关注。"
```

```json
"chat_summary": "Anthropic 为 Claude Code 增加了仓库级 planning mode，让开发者在真正改代码前先审阅跨文件计划。这个变化更偏向工程工作流治理，适合需要控制大规模代码修改风险的团队关注。"
```

```json
"chat_summary": "LangGraph 新增 checkpoint 和可恢复编排能力，目标是让多 Agent 工作流更适合生产环境。它解决的是长任务中断、恢复和状态管理问题，属于 Agent 工程化基础设施的一部分。"
```

```json
"chat_summary": "SWE-bench 分享了一份关于仓库级 coding agent 的 benchmark report，重点是评估 Agent 在真实代码库中的修复能力。该条目只基于账号名称、原始摘要和链接，不额外推断账号背景或行业地位。"
```

```json
"chat_summary": "Simon Willison 讨论了 prompt injection 的实际防护策略，核心是降低检索内容权限、隔离工具执行，并向用户暴露清晰审计线索。文章适合正在构建 RAG、Agent 或工具调用系统的开发者参考。"
```

```json
"chat_summary": "这期 Training Data 播客围绕 product taste、evaluation loops 和 Agent reliability 展开。Transcript 中提到，taste 是一个工具从 demo 好看走向每天被使用的关键差异。"
```

```json
"chat_summary": "vLLM v1.0.0 改进了 scheduler fairness 和生产 serving 稳定性。对依赖 vLLM 部署推理服务的团队来说，这类调度层变化会直接影响吞吐、公平性和线上可靠性。"
```

```json
"chat_summary": "browser-use/web-ui 是一个 TypeScript 项目，用本地 Web UI 运行 browser agents。它在 GitHub Trending 中增长到 1.2K stars，并估算有 76 stars/day 的新增速度。"
```

- [ ] **Step 2: Verify fixture JSON still parses**

Run:

```bash
python3 -m json.tool tests/fixtures/acceptance-merged.json >/tmp/acceptance-merged.pretty.json
```

Expected: command exits with status 0.

- [ ] **Step 3: Commit fixture summaries**

```bash
git add tests/fixtures/acceptance-merged.json
git commit -m "test: add chat digest summary fixture"
```

## Task 3: Implement Chat Rendering in Acceptance Renderer

**Files:**
- Modify: `scripts/render-acceptance-digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Import `math`**

Add this import after `import json`:

```python
import math
```

- [ ] **Step 2: Make score parsing finite-safe**

Replace the existing `quality_score()` with:

```python
def quality_score(article: Dict[str, Any]) -> float:
    value = article.get("quality_score", 0)
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0

    if not math.isfinite(number):
        return 0.0
    return number
```

- [ ] **Step 3: Add chat helper functions**

Insert after `format_count()`:

```python
def format_chat_score(article: Dict[str, Any]) -> str:
    score = max(0.0, min(quality_score(article), 20.0)) / 2
    return format_score(score)


def compact_text(value: Any) -> str:
    return " ".join(str(value).split()) if value else ""


def chat_summary(article: Dict[str, Any]) -> str:
    for field in (
        "chat_summary",
        "summary",
        "snippet",
        "full_text",
        "description",
        "transcript",
        "title",
    ):
        text = compact_text(article.get(field))
        if text:
            return text
    return "No summary material is available."


def chat_title_line(
    article: Dict[str, Any],
    index: int,
    emoji: str,
) -> str:
    title = article.get("title") or article.get("repo") or "Untitled"
    return f"{index}. {emoji} [{format_chat_score(article)}/10] {title}"


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
```

- [ ] **Step 4: Add chat topic renderer**

Insert after `render_topic_sections()`:

```python
def render_chat_topic_sections(
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

        emoji = topic_def.get("emoji", "")
        lines = [
            f"## {emoji} {topic_def.get('label', topic_id)}".rstrip(),
            "",
        ]
        for index, article in enumerate(articles, 1):
            lines.append(render_chat_item(article, index, emoji))
            lines.append("")
        sections.append("\n".join(lines).rstrip())

    return sections
```

- [ ] **Step 5: Add chat fixed-section renderers**

Insert after `render_podcast_remix()`:

```python
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


def render_chat_kol_updates(data: Dict[str, Any]) -> Optional[str]:
    tweets = [
        article
        for article in unique_articles(iter_articles(data), "twitter")
        if article_link(article)
    ]
    tweets = sorted(tweets, key=quality_score, reverse=True)
    return render_chat_article_section("## 📢 KOL Updates", "📢", tweets)


def render_chat_github_releases(data: Dict[str, Any]) -> Optional[str]:
    releases = [
        article
        for article in unique_articles(iter_articles(data), "github")
        if article_link(article)
    ]
    releases = sorted(releases, key=quality_score, reverse=True)
    return render_chat_article_section("## 📦 GitHub Releases", "📦", releases)


def render_chat_github_trending(data: Dict[str, Any]) -> Optional[str]:
    repos = [
        article
        for article in unique_articles(iter_articles(data), "github_trending")
        if article_link(article)
    ]
    repos = sorted(
        repos,
        key=lambda article: article.get("daily_stars_est", 0),
        reverse=True,
    )
    return render_chat_article_section("## 🐙 GitHub Trending", "🐙", repos)


def render_chat_blog_picks(data: Dict[str, Any]) -> Optional[str]:
    picks = [
        article
        for article in unique_articles(iter_articles(data))
        if article.get("is_blog_pick") and article_link(article)
    ]
    picks = sorted(picks, key=quality_score, reverse=True)
    return render_chat_article_section("## 📝 Blog Picks", "📝", picks)


def render_chat_podcast_remix(data: Dict[str, Any]) -> Optional[str]:
    episodes = [
        article
        for article in unique_articles(iter_articles(data), "podcast")
        if article.get("transcript_status") == "ok"
        and article.get("transcript")
        and article_link(article)
    ]
    episodes = sorted(episodes, key=quality_score, reverse=True)
    return render_chat_article_section("## 🎙️ Podcast Remix", "🎙️", episodes)
```

- [ ] **Step 6: Add chat digest entrypoint**

Insert after `render_digest()`:

```python
def render_chat_digest(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    report_date: str,
    version: str,
) -> str:
    sections = [f"# 🚀 Tech Digest - {report_date}"]
    sections.extend(render_chat_topic_sections(data, topic_defs))

    for renderer in (
        render_chat_kol_updates,
        render_chat_github_releases,
        render_chat_github_trending,
        render_chat_blog_picks,
        render_chat_podcast_remix,
    ):
        section = renderer(data)
        if section:
            sections.append(section)

    sections.append(render_footer(data, version))
    return "\n\n".join(sections).rstrip() + "\n"
```

- [ ] **Step 7: Route `render_digest()` by template**

Replace the existing `render_digest()` signature and first lines with:

```python
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
```

Keep the rest of the existing Discord body unchanged after this inserted routing block.

- [ ] **Step 8: Add CLI template argument**

In `build_parser()`, insert after the `--version` argument:

```python
    parser.add_argument(
        "--template",
        choices=("discord", "chat"),
        default="discord",
        help="Output template to render",
    )
```

In `main()`, replace:

```python
    output = render_digest(data, topic_defs, args.date, args.version)
```

with:

```python
    output = render_digest(
        data,
        topic_defs,
        args.date,
        args.version,
        template=args.template,
    )
```

- [ ] **Step 9: Pass template through manual context generation**

Change `build_codex_prompt()` signature to:

```python
def build_codex_prompt(report_date: str, version: str, template: str) -> str:
```

Replace the line that mentions `references/templates/discord.md` with:

```python
                f"references/templates/{template}.md as the source-of-truth "
```

Change `prepare_codex_acceptance_context()` signature to include `template: str = "discord"`:

```python
def prepare_codex_acceptance_context(
    data: Dict[str, Any],
    topic_defs: Sequence[Dict[str, Any]],
    source_fixture: Path,
    output_dir: Path,
    report_date: str,
    version: str,
    template: str = "discord",
) -> None:
```

Replace:

```python
        build_codex_prompt(report_date, version),
```

with:

```python
        build_codex_prompt(report_date, version, template),
```

Replace:

```python
        render_digest(data, topic_defs, report_date, version),
```

with:

```python
        render_digest(data, topic_defs, report_date, version, template=template),
```

In `main()`, pass `template=args.template` into `prepare_codex_acceptance_context()`.

- [ ] **Step 10: Run renderer tests to verify implementation**

Run:

```bash
python3 -m unittest tests/test_acceptance_digest.py -v
```

Expected: FAIL only on `test_daily_chat_digest_matches_golden` if `tests/golden/daily-chat.md` has not been generated yet. All non-golden chat behavior tests should pass.

- [ ] **Step 11: Commit renderer implementation**

```bash
git add scripts/render-acceptance-digest.py
git commit -m "feat: render chat digest acceptance output"
```

## Task 4: Add Chat Template and Prompt Documentation

**Files:**
- Create: `references/templates/chat.md`
- Modify: `references/digest-prompt.md`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Create `references/templates/chat.md`**

Create `references/templates/chat.md` with:

````markdown
# Tech Digest Chat Template

Universal IM format for Telegram, Feishu, WeChat, WeCom, and similar chat surfaces.

## Template Structure

```markdown
# 🚀 Tech Digest - {{DATE}}

{{#topics}}
## {{emoji}} {{label}}

{{#articles}}
{{index}}. {{emoji}} [{{score}}/10] {{title}}

{{summary}}

🔗 {{link}}

{{/articles}}
{{/topics}}

---
📊 Data Sources: RSS {{rss_count}} | Twitter {{twitter_count}} | Reddit {{reddit_count}} | Web {{web_count}} | GitHub {{github_count}} releases + {{trending_count}} trending | Podcast {{podcast_count}} episodes | Dedup: {{merged_count}} articles
🤖 Generated by follow-news v{{version}} | 🔗 https://github.com/tangwz/follow-news | Powered by OpenClaw
```

## Format Rules

- Use one fixed item shape: title line, blank line, compact summary, blank line, `🔗 URL`.
- Use bare URLs only. Do not use `<URL>`, Markdown inline links, or HTML links.
- Reset `{{index}}` to `1` inside each section.
- Use the source title unchanged in `{{title}}`.
- Write `{{summary}}` as one compact Chinese paragraph, normally 2-4 sentences.
- Do not force a `理由：` label. Include significance naturally when the evidence supports it.
- Skip items without a usable link.
- Skip sections that have no visible items after filtering.

## Evidence Rules

- Use only fields already present in merged JSON: `title`, `snippet`, `summary`, `full_text`, `transcript`, release notes, repo metadata, and source metadata.
- Do not infer company, person, metrics, publication time, role, or impact from outside knowledge.
- If only thin material is available, write a shorter and more cautious summary.
- If only fetch time exists, do not write it as the news publication time.

## Source Rules

- Twitter/X and KOL: identify display name, handle, or known identity only when present in evidence. Include metrics only when they explain reach, controversy, or importance.
- RSS and Web: prefer concrete product, model, version, company, person, metric, and publication-time details when present.
- Reddit: distinguish the linked item from subreddit discussion. Treat score, comments, and controversy as discussion signals, not factual proof.
- Podcast: use transcript-backed insight only when transcript text is available. Without transcript, summarize only title, show name, snippet, duration, and source metadata.
- GitHub Releases and GitHub Trending: keep summaries short. Prefer repo, version or trending status, language, stars, and core changes. Do not add industry judgment unless release notes or repo metadata support it.
````

- [ ] **Step 2: Update `<TEMPLATE>` placeholder documentation**

In `references/digest-prompt.md`, replace:

```markdown
| `<TEMPLATE>` | `discord` / `email` / `markdown` | |
```

with:

```markdown
| `<TEMPLATE>` | `discord` / `email` / `markdown` / `chat` | |
```

- [ ] **Step 3: Add chat-specific report-generation rules**

In `references/digest-prompt.md`, after:

```markdown
Use this output to select articles — **do NOT write ad-hoc Python to parse the JSON**. Apply the template from `<SKILL_DIR>/references/templates/<TEMPLATE>.md`.
```

insert:

```markdown
When `<TEMPLATE>` is `chat`, follow `references/templates/chat.md` exactly: each visible item uses title line, one compact Chinese summary paragraph, and `🔗 URL`. Keep source titles and URLs unchanged. Do not use `<URL>`, Markdown inline links, or HTML links. Skip linkless items; skip sections that have no visible items after filtering.
```

- [ ] **Step 4: Add chat-specific link rule**

In `references/digest-prompt.md`, replace:

```markdown
- Every item must include a source link (Discord: `<link>`, Email: `<a href>`, Markdown: `[title](link)`)
```

with:

```markdown
- Every item must include a source link (Discord: follow `references/templates/discord.md`, Email: `<a href>`, Markdown: `[title](link)`, Chat: `🔗 URL`)
```

- [ ] **Step 5: Run prompt/template smoke checks**

Run:

```bash
rg -n "chat|templates/chat|🔗 URL|<TEMPLATE>" references/digest-prompt.md references/templates/chat.md
```

Expected: output includes the new `<TEMPLATE>` value, `references/templates/chat.md`, and the chat link rule.

- [ ] **Step 6: Commit template and prompt docs**

```bash
git add references/templates/chat.md references/digest-prompt.md
git commit -m "docs: add chat digest template"
```

## Task 5: Final Verification and Output Sample

**Files:**
- Verify: `scripts/render-acceptance-digest.py`
- Verify: `tests/test_acceptance_digest.py`
- Verify: `tests/golden/daily-chat.md`
- Verify: `references/templates/chat.md`
- Verify: `references/digest-prompt.md`

- [ ] **Step 1: Generate the chat golden**

Run:

```bash
UPDATE_GOLDEN=1 python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_chat_digest_matches_golden -v
```

Expected: PASS and `tests/golden/daily-chat.md` is created.

- [ ] **Step 2: Inspect the generated golden manually**

Run:

```bash
sed -n '1,220p' tests/golden/daily-chat.md
```

Expected:

- Output starts with `# 🚀 Tech Digest - 2026-02-27`.
- Each visible item has title line, blank line, summary paragraph, blank line, and `🔗 URL`.
- No line contains `<https://`.
- Low-score fixture item is absent.

- [ ] **Step 3: Commit chat golden**

```bash
git add tests/golden/daily-chat.md
git commit -m "test: add chat digest golden"
```

- [ ] **Step 4: Run full output-related tests**

Run:

```bash
python3 -m unittest tests/test_acceptance_digest.py tests/test_summarize_merged.py -v
```

Expected: all tests pass.

- [ ] **Step 5: Render a chat sample**

Run:

```bash
python3 scripts/render-acceptance-digest.py \
  --input tests/fixtures/acceptance-merged.json \
  --topics config/defaults/topics.json \
  --date 2026-05-16 \
  --version 3.17.0 \
  --template chat \
  --output /tmp/follow-news-chat-sample.md
```

Expected: command exits with status 0.

- [ ] **Step 6: Inspect the sample**

Run:

```bash
sed -n '1,180p' /tmp/follow-news-chat-sample.md
```

Expected:

- Output uses title, summary, `🔗 URL` blocks.
- No line contains `<https://`.
- Topic sections with visible items contain at least one title line.
- Low-score fixture item is absent.

- [ ] **Step 7: Check working tree scope**

Run:

```bash
git status --short
```

Expected: only files intentionally changed for this plan are modified or staged. If the pre-existing Discord direct-link edits are still unstaged, keep them out of chat-template commits unless the user explicitly wants them included.

- [ ] **Step 8: Commit final verification adjustments if needed**

If golden or documentation files changed during verification, commit only those intended files:

```bash
git add tests/golden/daily-chat.md references/templates/chat.md references/digest-prompt.md scripts/render-acceptance-digest.py tests/test_acceptance_digest.py tests/fixtures/acceptance-merged.json
git commit -m "test: verify chat digest output"
```

Expected: either a small verification commit is created, or there are no remaining chat-template changes to commit.

## Self-Review

- Spec coverage: The plan covers `references/templates/chat.md`, `<TEMPLATE>=chat`, acceptance renderer support, golden output, `🔗 URL`, linkless item filtering, source-specific evidence boundaries, and Discord regression protection.
- Placeholder scan: The plan avoids unresolved placeholder markers and vague implementation-only steps.
- Type consistency: `render_digest(..., template="chat")`, `render_chat_digest()`, `render_chat_item()`, `chat_summary()`, and `format_chat_score()` use consistent names across tests and implementation.
- Risk control: The plan explicitly keeps pre-existing Discord link edits separate from the new `chat` implementation.
