# Non-GitHub Summary Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Strengthen non-GitHub digest summary rules across prompt, chat, Discord, and email templates while preserving GitHub Releases and GitHub Trending behavior.

**Architecture:** Keep the data pipeline unchanged. Treat `references/digest-prompt.md` and `references/templates/*.md` as the behavioral contract, then add focused acceptance tests that lock field-based summary evidence, KOL metric normalization, and GitHub exclusion boundaries. The renderer changes are limited to small pure helper coverage if the current branch does not already normalize KOL metrics.

**Tech Stack:** Python 3.8 standard library, `unittest`, Markdown prompt/template files, existing `scripts/render-acceptance-digest.py` acceptance renderer.

---

## File Structure

- Modify: `references/digest-prompt.md`
  - Owns the global report-generation contract and source-specific fixed-section rules.
  - Add a "Non-GitHub Summary Quality Contract" that explicitly excludes `source_type == "github"` and `source_type == "github_trending"`.
- Modify: `references/templates/chat.md`
  - Owns IM/chat item structure and source-specific summary rules.
  - Add the evidence priority and platform-length precedence rules for non-GitHub items.
- Modify: `references/templates/discord.md`
  - Owns Discord-specific layout and length constraints.
  - Add the same summary-quality contract in Discord terms without changing the GitHub examples.
- Modify: `references/templates/email.md`
  - Owns HTML email structure and email-specific rendering guidance.
  - Add the same summary-quality contract in email terms.
- Modify: `tests/test_acceptance_digest.py`
  - Add text-contract tests for prompt/templates.
  - Add regression tests for KOL metric zero fallback and stable non-GitHub summary material.
- Modify only if tests fail: `scripts/render-acceptance-digest.py`
  - Keep any implementation minimal and pure.
  - Do not touch fetchers, merge logic, scoring, ordering, source configs, or GitHub renderers.

## Task 1: Add Prompt Contract Test

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add the failing prompt contract test**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_daily_chat_digest_structure_contract`:

```python
    def test_digest_prompt_documents_non_github_summary_contract(self):
        prompt = (ROOT_DIR / "references" / "digest-prompt.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("### Non-GitHub Summary Quality Contract", prompt)
        self.assertIn("This contract applies to KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast items.", prompt)
        self.assertIn("It does not apply to GitHub Releases or GitHub Trending.", prompt)
        self.assertIn("full_text > summary > snippet > title", prompt)
        self.assertIn("Lower-priority fields may provide supplemental context", prompt)
        self.assertIn("metrics.impression_count", prompt)
        self.assertIn("metrics.reply_count", prompt)
        self.assertIn("metrics.retweet_count", prompt)
        self.assertIn("metrics.like_count", prompt)
        self.assertIn("Missing, null, empty, or unparsable metric values render as 0.", prompt)
        self.assertIn("Discord and email length limits take precedence over sentence-count targets.", prompt)
```

- [ ] **Step 2: Run the specific test and verify it fails**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_digest_prompt_documents_non_github_summary_contract -v
```

Expected: `FAIL` with an assertion that `"### Non-GitHub Summary Quality Contract"` is not found.

- [ ] **Step 3: Update `references/digest-prompt.md`**

Insert this section after the paragraph that starts with `Select articles **purely by quality_score` and before `For non-chat templates`:

```markdown
### Non-GitHub Summary Quality Contract

This contract applies to KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast items. It does not apply to GitHub Releases or GitHub Trending.

Use a tendency-based structure, not a mandatory checklist: explain what happened, what object it happened to, and why it matters only when the available evidence supports those points. If evidence is thin, keep the summary shorter and preserve the most concrete fact instead of adding unsupported context.

Use this evidence priority as weight, not exclusivity: `full_text > summary > snippet > title`. Prefer the highest-quality field as the main fact source. Lower-priority fields may provide supplemental context such as object names, source titles, or short background, but they must not override or contradict higher-priority fields.

Non-GitHub summaries normally use 2-4 sentences. Chat can keep this target when space permits. Discord and email length limits take precedence over sentence-count targets; when space is tight, compress to 1-2 sentences while preserving the most specific evidence-backed fact.

For KOL/Twitter fixed sections, always render the four metrics from `metrics.impression_count`, `metrics.reply_count`, `metrics.retweet_count`, and `metrics.like_count` in that order. Missing, null, empty, or unparsable metric values render as 0. A real value of 0 also renders as 0. Metrics are context for reach and discussion, not proof that a claim is true.
```

- [ ] **Step 4: Run the prompt contract test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_digest_prompt_documents_non_github_summary_contract -v
```

Expected: `OK`.

- [ ] **Step 5: Commit Task 1**

Run:

```bash
git add tests/test_acceptance_digest.py references/digest-prompt.md
git commit -m "docs: define non-github summary contract"
```

Expected: commit succeeds.

## Task 2: Update Template Contracts

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Modify: `references/templates/chat.md`
- Modify: `references/templates/discord.md`
- Modify: `references/templates/email.md`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add the failing template contract test**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_digest_prompt_documents_non_github_summary_contract`:

```python
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
                self.assertIn("KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast", text)
                self.assertIn("GitHub Releases and GitHub Trending keep their existing concise style.", text)
                self.assertIn("full_text > summary > snippet > title", text)
                self.assertIn("Lower-priority fields may provide supplemental context", text)
                self.assertIn("length limits take precedence over sentence-count targets", text)
```

- [ ] **Step 2: Run the specific test and verify it fails**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_templates_document_non_github_summary_contract -v
```

Expected: `FAIL` with an assertion that `"Non-GitHub Summary Quality"` is not found.

- [ ] **Step 3: Update `references/templates/chat.md`**

Insert this section after `## Evidence Rules` and before `## Source Rules`:

```markdown
## Non-GitHub Summary Quality

This applies to KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast items. GitHub Releases and GitHub Trending keep their existing concise style.

Use a tendency-based structure: what happened, what object changed, and why it matters when the evidence supports it. Do not force all three points into every item.

Use `full_text > summary > snippet > title` as evidence weight. Lower-priority fields may provide supplemental context such as names or short background, but they must not override higher-priority facts.

Chat summaries normally use 2-4 sentences in one compact paragraph. Platform length limits take precedence over sentence-count targets when the output is sent through constrained channels.
```

- [ ] **Step 4: Update `references/templates/discord.md`**

Insert this section after `## Discord-Specific Features` and before `## Example Output`:

```markdown
## Non-GitHub Summary Quality

This applies to KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast items. GitHub Releases and GitHub Trending keep their existing concise style.

Use a tendency-based structure: what happened, what object changed, and why it matters when the evidence supports it. Do not force all three points into every item.

Use `full_text > summary > snippet > title` as evidence weight. Lower-priority fields may provide supplemental context such as names or short background, but they must not override higher-priority facts.

Discord length limits take precedence over sentence-count targets. When space is tight, compress non-GitHub summaries to 1-2 evidence-backed sentences.
```

- [ ] **Step 5: Update `references/templates/email.md`**

Insert this section after `## Style Guidelines` and before `## Example Output`:

```markdown
## Non-GitHub Summary Quality

This applies to KOL, non-GitHub topic, Blog Picks, Reddit, and Podcast items. GitHub Releases and GitHub Trending keep their existing concise style.

Use a tendency-based structure: what happened, what object changed, and why it matters when the evidence supports it. Do not force all three points into every item.

Use `full_text > summary > snippet > title` as evidence weight. Lower-priority fields may provide supplemental context such as names or short background, but they must not override higher-priority facts.

Email length limits take precedence over sentence-count targets. When space is tight, compress non-GitHub summaries to 1-2 evidence-backed sentences.
```

- [ ] **Step 6: Run the template contract test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_templates_document_non_github_summary_contract -v
```

Expected: `OK`.

- [ ] **Step 7: Commit Task 2**

Run:

```bash
git add tests/test_acceptance_digest.py references/templates/chat.md references/templates/discord.md references/templates/email.md
git commit -m "docs: align summary quality templates"
```

Expected: commit succeeds.

## Task 3: Lock KOL Metric Normalization

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Modify if needed: `scripts/render-acceptance-digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add the KOL missing-metric regression test**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_chat_twitter_metrics_are_not_rendered_without_summary_support`:

```python
    def test_chat_kol_metrics_render_zero_for_missing_values(self):
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
        topic_defs = [{"id": "ai-agent", "emoji": "🤖", "label": "AI Agent"}]

        text = render_mod.render_digest(
            data,
            topic_defs,
            report_date="2026-02-27",
            version="3.17.0",
            template="chat",
        )

        kol_text = text.split("## 📢 KOL Updates", 1)[1]
        self.assertIn("`👁 0 | 💬 0 | 🔁 0 | ❤️ 0`", kol_text)
```

- [ ] **Step 2: Run the specific test**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_kol_metrics_render_zero_for_missing_values -v
```

Expected on a clean pre-change branch: `FAIL` because fixed chat KOL metric rendering is absent. Expected on the current working tree after the earlier KOL normalization change: `OK`.

- [ ] **Step 3: Add the renderer helper if the test fails**

If `scripts/render-acceptance-digest.py` does not already have `format_kol_metric_text`, add this function after `render_kol_updates`:

```python
def format_kol_metric_text(article: Dict[str, Any]) -> str:
    metrics = article.get("metrics", {})
    return (
        f"👁 {format_count(metrics.get('impression_count'))} | "
        f"💬 {format_count(metrics.get('reply_count'))} | "
        f"🔁 {format_count(metrics.get('retweet_count'))} | "
        f"❤️ {format_count(metrics.get('like_count'))}"
    )
```

- [ ] **Step 4: Use the helper in Discord KOL rendering if needed**

If `render_kol_updates` still builds metric text inline, replace that inline block with:

```python
        metric_text = format_kol_metric_text(article)
```

- [ ] **Step 5: Use the helper in chat KOL rendering if needed**

If `render_chat_kol_updates` still delegates to `render_chat_article_section`, replace the function body with:

```python
def render_chat_kol_updates(data: Dict[str, Any]) -> Optional[str]:
    tweets = [
        article
        for article in unique_articles(iter_articles(data), "twitter")
        if article_link(article)
    ]
    tweets = sorted(tweets, key=quality_score, reverse=True)
    lines = ["## 📢 KOL Updates", ""]
    for index, article in enumerate(tweets, 1):
        metric_text = format_kol_metric_text(article)
        lines.append(chat_title_line(article, index, "📢"))
        lines.append("")
        lines.append(f"{chat_summary(article)} `{metric_text}`")
        lines.append("")
        lines.append(f"🔗 {article_link(article)}")
        lines.append("")
    return "\n".join(lines).rstrip()
```

- [ ] **Step 6: Run the KOL metric test and verify it passes**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_kol_metrics_render_zero_for_missing_values -v
```

Expected: `OK`.

- [ ] **Step 7: Commit Task 3**

Run:

```bash
git add tests/test_acceptance_digest.py scripts/render-acceptance-digest.py
git commit -m "test: lock kol metric normalization"
```

Expected: commit succeeds.

## Task 4: Lock Non-GitHub Summary Evidence Boundaries

**Files:**
- Modify: `tests/test_acceptance_digest.py`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Add a helper for extracting chat item summaries**

Insert this helper after `render_daily_chat_digest()`:

```python
def extract_chat_summary(text, title_line):
    lines = text.splitlines()
    index = lines.index(title_line)
    return lines[index + 2]
```

- [ ] **Step 2: Add stable phrase checks for non-GitHub fixture summaries**

Insert this method inside `class TestAcceptanceRenderer(unittest.TestCase):` after `test_daily_chat_digest_structure_contract`:

```python
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
```

- [ ] **Step 3: Strengthen snippet-only anti-fabrication coverage**

Replace the body of `test_chat_summary_uses_available_material_without_extra_facts` with this exact body:

```python
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
            "1. 🧠 [5/10] Snippet-only model note",
        )

        self.assertEqual(summary, "Only this snippet is available.")
        self.assertNotIn("OpenAI", summary)
        self.assertNotIn("Anthropic", summary)
        self.assertNotIn("2026", summary)
        self.assertNotIn("CEO", summary)
```

- [ ] **Step 4: Run the non-GitHub summary tests**

Run:

```bash
python3 -m unittest \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_non_github_summaries_keep_stable_evidence_phrases \
  tests.test_acceptance_digest.TestAcceptanceRenderer.test_chat_summary_uses_available_material_without_extra_facts \
  -v
```

Expected: `OK`.

- [ ] **Step 5: Commit Task 4**

Run:

```bash
git add tests/test_acceptance_digest.py
git commit -m "test: cover non-github summary evidence"
```

Expected: commit succeeds.

## Task 5: Refresh Chat Golden Only If Renderer Output Changed

**Files:**
- Modify if needed: `tests/golden/daily-chat.md`
- Test: `tests/test_acceptance_digest.py`

- [ ] **Step 1: Run the chat golden test**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_chat_digest_matches_golden -v
```

Expected if Task 3 changed rendered output: `FAIL` with a golden diff. Expected if current KOL metric rendering was already present: `OK`.

- [ ] **Step 2: Regenerate the chat golden only if Step 1 failed**

Run:

```bash
UPDATE_GOLDEN=1 python3 -m unittest tests.test_acceptance_digest.TestAcceptanceRenderer.test_daily_chat_digest_matches_golden -v
```

Expected: `OK` and output includes `golden updated:`.

- [ ] **Step 3: Verify the regenerated golden contains KOL metrics**

Run:

```bash
rg -n "👁 12.5K \\| 💬 45 \\| 🔁 230 \\| ❤️ 1.8K" tests/golden/daily-chat.md
```

Expected: one matching line in the KOL section.

- [ ] **Step 4: Commit Task 5 if the golden changed**

Run:

```bash
git add tests/golden/daily-chat.md
git commit -m "test: update chat golden summary output"
```

Expected: commit succeeds if the golden changed. If the golden did not change, skip this commit.

## Task 6: Full Verification

**Files:**
- Verify: `references/digest-prompt.md`
- Verify: `references/templates/chat.md`
- Verify: `references/templates/discord.md`
- Verify: `references/templates/email.md`
- Verify: `scripts/render-acceptance-digest.py`
- Verify: `tests/test_acceptance_digest.py`
- Verify: `tests/golden/daily-chat.md`

- [ ] **Step 1: Run the acceptance test module**

Run:

```bash
python3 -m unittest tests.test_acceptance_digest -v
```

Expected: `OK`.

- [ ] **Step 2: Run the summarizer tests to catch fixture/output regressions**

Run:

```bash
python3 -m unittest tests.test_summarize_merged -v
```

Expected: `OK`.

- [ ] **Step 3: Scan the changed docs for forbidden vague markers**

Run:

```bash
rg -n "TB[D]|TO""DO|implement[ ]later|fill[ ]in[ ]details|add[ ]appropriate|similar[ ]to[ ]Task" \
  references/digest-prompt.md \
  references/templates/chat.md \
  references/templates/discord.md \
  references/templates/email.md \
  docs/superpowers/plans/2026-05-17-non-github-summary-quality.md
```

Expected: no matches.

- [ ] **Step 4: Confirm GitHub section wording remains scoped**

Run:

```bash
rg -n "GitHub Releases|GitHub Trending|existing concise style|source_type == \"github\"|github_trending" \
  references/digest-prompt.md \
  references/templates/chat.md \
  references/templates/discord.md \
  references/templates/email.md
```

Expected: output shows GitHub-specific rules still present and the non-GitHub summary contract explicitly excludes GitHub Releases and GitHub Trending.

- [ ] **Step 5: Commit final verification notes if any files changed in Task 6**

Run:

```bash
git status --short
```

Expected: no unstaged changes from verification commands. If files changed because of a deliberate correction, stage and commit them with:

```bash
git add references/digest-prompt.md references/templates/chat.md references/templates/discord.md references/templates/email.md tests/test_acceptance_digest.py tests/golden/daily-chat.md
git commit -m "chore: finalize summary quality contract"
```

## Self-Review

- Spec coverage: The plan covers non-GitHub KOL, topic, Blog Picks, Reddit, and Podcast summary quality; KOL metric field names and zero fallback; field priority as evidence weight; platform length precedence; test strategy that avoids brittle semantic assertions; GitHub Releases and GitHub Trending exclusions.
- Placeholder scan: The plan contains no incomplete markers or deferred implementation language.
- Type consistency: Test names, file paths, renderer function names, and metric field names are consistent across tasks.
- Scope check: The plan modifies prompt/template contracts, tests, and only the small acceptance renderer surface if needed. It does not touch fetchers, merge logic, scoring, source configs, or GitHub renderer behavior.
