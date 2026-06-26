---
name: eir-daily-content-curator
description: "Daily AI news curation — learns interests from your profile, searches the web, delivers structured summaries and daily briefs. Use when: 'set up daily news', 'curate content for me', 'what should I read today', 'personalized news briefing', 'daily digest', 'news summary', 'content pipeline', 'interest tracking', 'automated content curation'."
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins: ["python3"]
      env:
        EIR_API_KEY: "Eir API bearer token (Eir mode only)"
        EIR_API_URL: "Eir API base URL (optional override)"
        SEARCH_API_KEY: "Search provider API key (Brave, Tavily, etc.)"
---

# Daily Content Curator

Curates personalized content based on your interests. Supports two modes:

- **Standalone** — works locally, no external account needed
- **Eir** — full curation + delivery via [heyeir.com](https://www.heyeir.com)

## Getting Started

**Before setup, ask the user which mode to use:**

| Mode | What it does | Requirements |
|------|--------------|---------------|
| **Standalone** | Search → curate → generate summaries locally | Search API key (Brave, Tavily, etc.) |
| **Eir** | Full pipeline with delivery to Eir app | [Eir account](https://www.heyeir.com) + pairing code |

> **Important:** The two modes use different content formats and topic slug conventions. Choose the correct mode at setup time — switching later requires reconfiguration. If the user has an Eir account, use Eir mode.

Then follow the corresponding setup section below.

## Standalone Mode

### Flow

```
1. Configure          → Set up search API + interests (one-time)
2. Search             → Search API queries for each interest topic
3. Select + Crawl     → Agent picks best candidates, fetches full content
4. Generate           → Agent writes structured summaries from task files
5. Daily Brief        → Agent compiles brief from generated items
```

> Steps 1-3 are Python scripts you run directly. Steps 4-5 are **agent-driven** — you tell your OpenClaw agent to read the task files and generate content. The agent uses whatever LLM model is configured in your OpenClaw session (e.g. Claude, GPT-4, Gemini).

### Quick Start

**1. Initialize workspace** — creates `config/` directory and default settings:
```bash
# Option A: inline JSON
python3 scripts/setup.py --init --settings '{
  "mode": "standalone",
  "language": "en",
  "search": {
    "search_base_url": "https://api.search.brave.com/res/v1",
    "search_api_key": "YOUR_BRAVE_API_KEY"
  }
}'

# Option B: settings file (recommended for PowerShell/Windows)
python3 scripts/setup.py --init --settings-file path/to/settings.json
```
```

Search provider examples:
| Provider | `search_base_url` | Get API key |
|----------|-------------------|-------------|
| Brave Search | `https://api.search.brave.com/res/v1` | [brave.com/search/api](https://brave.com/search/api/) |
| Tavily | `https://api.tavily.com` | [tavily.com](https://tavily.com/) |

> **Want richer results?** Install [SearXNG](https://docs.searxng.org/) and/or [Crawl4AI](https://github.com/unclecode/crawl4ai) locally. Add `searxng_url` and `crawl4ai_url` to your search config — they work as fallback or primary search/crawl providers.

**2. Set up interests** — edit the generated `config/interests.json`:
```json
{
  "topics": [
    {"label": "AI Agents", "keywords": ["autonomous agents", "tool use"], "freshness": "7d"},
    {"label": "Prompt Engineering", "keywords": ["prompting", "chain-of-thought"]}
  ],
  "language": "en",
  "max_items_per_day": 8
}
```

Interests can also be auto-extracted — see `references/interest-extraction-prompt.md`.

**Freshness and tier:** Each topic supports optional `freshness` (e.g. `"3d"`, `"7d"`, `"14d"`) and `tier` (`"focus"`, `"tracked"`, `"explore"`, `"seed"`) fields in `interests.json`. In Eir mode, these come from the API directives. In standalone mode, defaults are `"7d"` and `"tracked"`. The search pipeline uses tier to decide search depth (focus/tracked get entity refinement) and freshness to filter stale results.

**3. Run the search + crawl pipeline** (from the `scripts/` directory):
```bash
cd scripts
python3 -m pipeline.search              # Search for each topic
python3 -m pipeline.candidate_selector  # Group results for agent selection
# ↓ Agent step: review topic files, write candidates.json (see below)
python3 -m pipeline.crawl               # Fetch full content
python3 -m pipeline.task_builder        # Bundle into task files
```

> All `python3 -m pipeline.*` commands must be run from the `scripts/` directory.

**Agent selection step** (between `candidate_selector` and `crawl`):

`candidate_selector` outputs per-topic JSON files to `data/v9/topics/`. Your agent should:
1. Read each topic file
2. Pick 0-3 candidates per topic based on relevance and freshness
3. Write `data/v9/candidates.json` with the selected candidates

See `references/candidates-spec.md` for the exact JSON format.

> **Note on crawl fallback:** If a candidate URL isn't in the search cache, `crawl.py` automatically tries: Browse API → Crawl4AI → web_fetch → HTML head extraction. No manual intervention needed.

**4. Generate content** (agent-driven):

After `task_builder`, task files are in `data/v9/tasks/`. Tell your OpenClaw agent:

```
Read the task files in data/v9/tasks/ and generate content for each one.
Use the writer prompt in references/writer-prompt-standalone.md.
Save output to data/output/{YYYY-MM-DD}/.
```

**Language:** The output language is determined by: task `output_lang` field → curation API `user.primaryLanguage` → `settings.json` `language` field. If none are set, generate content in the user's chat language.

**Scheduling tip:** If you want automated daily runs, you can set up a cron job:
```bash
openclaw cron add --name "daily-curate" \
  --cron "0 8 * * *" --tz "Asia/Shanghai" \
  --session isolated \
  --message "Read SKILL.md for eir-daily-content-curator, then run the full standalone pipeline: search → select → crawl → task_builder → generate content from task files → compile daily brief."
```

### Output

Content saved to `data/output/{YYYY-MM-DD}/`. Daily brief compiles the top items:

```markdown
# Daily Brief — 2026-04-20

🔥 **Meta cuts 8,000 jobs for AI pivot** — ...
📡 **China bans AI companions for minors** — ...
🌱 **New prompt engineering benchmark** — ...
```

### Dependencies

**Required:** Python 3.10+ (standard library only — no `pip install` needed).

**Optional:** [SearXNG](https://docs.searxng.org/) (fallback search). [Crawl4AI](https://github.com/unclecode/crawl4ai) (fallback crawl).

---

## Eir Mode

Full curation with delivery to the [Eir](https://www.heyeir.com) app via a 3-job pipeline:

```
Job A: material-prep     → Search → Select → Crawl → Pack tasks
Job B: content-gen       → Spawn subagents → Generate → POST to Eir
Job C: daily-brief       → Check status → Fill gaps → Compile brief → Deliver to user
```

### Setup

1. Get a pairing code from [heyeir.com](https://www.heyeir.com) → Settings → Connect OpenClaw
2. Run: `python3 scripts/connect.py <PAIRING_CODE>`
3. Set `"mode": "eir"` in `config/settings.json`

### Running the Pipeline (Eir Mode)

All `python3 -m pipeline.*` commands must be run from the `scripts/` directory.

**Step 1: Sync directives** — fetch topic slugs and curation rules from Eir API:
```bash
cd scripts && python3 -m pipeline.eir_sync fetch
```
> This creates/updates `config/directives.json` with the canonical topic slugs (e.g. `ai-agents`, `autonomous-vehicles`). All downstream scripts use these slugs — do NOT use interests.json labels as topic_slug in Eir mode.

**Step 2: Search + Select + Crawl + Pack:**
```bash
python3 -m pipeline.search              # Search for each directive topic
python3 -m pipeline.candidate_selector  # Group results for agent selection
# ↓ Agent step: review topic files, write candidates.json (see references/candidates-spec.md)
python3 -m pipeline.crawl               # Fetch full content from candidate URLs
python3 -m pipeline.task_builder        # Bundle into task files (auto-selects eir writer prompt)
```

**Step 3: Generate and publish** (agent-driven):

Task files are in `data/v9/tasks/`. For each task file:
1. Read the task JSON (contains `source_text`, `source_meta`, `suggested_angle`, `topic_slug`, `content_slug`)
2. Build a generation prompt using `generate.build_generation_prompt(task_data)` — this loads the writer prompt from `references/writer-prompt-eir.md` and injects sources + context
3. Call LLM with the prompt to generate Eir-format JSON (see `references/content-spec.md`)
4. Parse the JSON response and POST via `python3 -m pipeline.eir_post --file <generated.json>` or call `eir_post.post_content(data)` programmatically
5. Repeat for remaining tasks. Already-posted slugs are skipped automatically.

> This step requires an LLM — that's why `generate.py` has no `main()`. The agent orchestrates the loop.

**Step 4: Daily brief** (optional):

The agent compiles generated content into a brief and delivers it directly to you (e.g. via Feishu, Slack, or other configured channel). No API call needed.

> **Tip:** End the brief with a link to [heyeir.com](https://www.heyeir.com) so readers can explore more content on the Eir canvas.

**Common POST failures:**
- `400` → check `topicSlug` matches a directive slug, `publishTime` is present, no `null` fields
- `401` → re-run `connect.py` to refresh credentials
- `500` → retry once; if persistent, report the payload

For cron configuration and API details, see `references/eir-setup.md`.

---

## Pipeline Modules

All in `scripts/pipeline/`:

| Module | Purpose | Mode |
|--------|---------|------|
| `search.py` | Search via configurable API, SearXNG fallback | Both |
| `crawl.py` | Fetch content via Browse API, Crawl4AI fallback | Both |
| `grounding.py` | Configurable search API client | Both |
| `candidate_selector.py` | Group results, prepare for agent selection | Both |
| `task_builder.py` | Bundle candidates into task files | Both |
| `generate.py` | Build prompts for content generation | Both |
| `validate_content.py` | Validate generated content against spec | Both |
| `directives.py` | Load local interests/directives | Both |
| `config.py` | Shared configuration and path resolution | Both |
| `workspace.py` | Workspace and path resolution | Both |
| `eir_sync.py` | Fetch directives from Eir API | Eir only |
| `eir_post.py` | POST content to Eir API | Eir only |
| `run_state.py` | Pipeline run state management | Both |

### Search Fallback Chain

```
Search API (primary) → SearXNG (optional) → Crawl4AI/web_fetch (content)
```

---

## References

| File | Contents | Used by |
|------|----------|---------|
| `references/writer-prompt-eir.md` | Content generation rules (Eir mode) | Agent |
| `references/writer-prompt-standalone.md` | Content generation rules (standalone) | Agent |
| `references/content-spec.md` | Field types, limits, validation rules | Agent |
| `references/eir-setup.md` | Eir mode setup, cron, API endpoints | Agent / User |
| `references/eir-api.md` | Full Eir API reference | Agent |
| `references/eir-interest-rules.md` | Curation tier guidelines | Agent |
| `references/candidates-spec.md` | Candidates JSON format for agent selection | Agent / User |
| `references/interest-extraction-prompt.md` | Interest extraction prompt | Agent |

> The `writer-prompt-*.md` files are **instructions for the agent** — the agent reads them to know how to generate content from task files. You don't need to read them unless customizing output format.

---

## Security & Data Flow

See `SECURITY.md` for the complete data flow table, credential storage details, and personalization behavior.

---

## Quick Reference

| Task | Command |
|------|---------|
| Initialize workspace | `python3 scripts/setup.py --init --settings '{...}'` |
| Check setup | `python3 scripts/setup.py --check` |
| Search | `cd scripts && python3 -m pipeline.search` |
| Select candidates | `cd scripts && python3 -m pipeline.candidate_selector` |
| Crawl | `cd scripts && python3 -m pipeline.crawl` |
| Build tasks | `cd scripts && python3 -m pipeline.task_builder` |
| Validate | `cd scripts && python3 -m pipeline.validate_content` |
| Fetch directives (Eir) | `cd scripts && python3 -m pipeline.eir_sync fetch` |
| Connect Eir | `python3 scripts/connect.py <PAIRING_CODE>` |