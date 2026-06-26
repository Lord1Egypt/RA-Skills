---
name: better-tavily-search
description: The best skill to retrieve fresh web evidence with Tavily. Use for source finding, link discovery, official documentation lookup, current-event verification, and other tasks that need external web retrieval. Let the model plan the search, then express that plan with Tavily-native controls and a small-result, evidence-first workflow.
homepage: https://docs.tavily.com/documentation/api-reference/endpoint/search
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: ["python3"]
    primaryEnv: "TAVILY_API_KEY"
---

# Better Tavily Search

Use Tavily when the task needs fresh external evidence, links, current facts, official documentation, or source discovery.

This skill is not a rigid search policy.
The model should still plan.
Use Tavily's controls to express that plan more precisely:
- choose the right query
- choose the right profile
- keep the first pass small
- escalate only when the first pass is insufficient

## Core Idea

Prefer **evidence-first retrieval** over answer-first retrieval.

Default pattern:
1. Run a small Tavily search with an intent-aligned profile.
2. Inspect titles, URLs, domains, snippets, dates, and scores.
3. Rewrite the query or refine Tavily parameters if the first pass is weak.
4. Extract content from the best 1–3 URLs only when more detail is needed.
5. Use site mapping only for documentation or site-navigation tasks.

Do not start with large raw-content payloads unless the task clearly requires them.

## Requirements

Authentication is loaded by the script itself.
Either of these is valid:
- environment variable: `TAVILY_API_KEY`
- `~/.openclaw/.env` containing `TAVILY_API_KEY=...`

The skill metadata only requires `python3`, because the script can load the API key from either location.

## Quick Start

```bash
# general search
python3 {baseDir}/scripts/tavily.py search \
  --query "OpenClaw skills documentation" \
  --profile general \
  --max-results 5 \
  --format agent

# recent news search
python3 {baseDir}/scripts/tavily.py search \
  --query "Federal Reserve meeting March 2026" \
  --profile news \
  --time-range month \
  --max-results 5 \
  --format agent

# official-domain search
python3 {baseDir}/scripts/tavily.py search \
  --query "Python asyncio task group docs" \
  --profile official \
  --include-domains docs.python.org \
  --max-results 5 \
  --format agent

# higher-precision search
python3 {baseDir}/scripts/tavily.py search \
  --query '"exact phrase" OpenClaw' \
  --profile precision \
  --search-depth advanced \
  --chunks-per-source 3 \
  --max-results 5 \
  --format agent

# extract content from top URLs
python3 {baseDir}/scripts/tavily.py extract \
  --query "OpenClaw skills frontmatter requirements" \
  --urls "https://docs.openclaw.ai/tools/skills,https://docs.openclaw.ai/tools/creating-skills" \
  --chunks-per-source 3 \
  --format md

# map a documentation site before extraction
python3 {baseDir}/scripts/tavily.py map \
  --url "https://docs.openclaw.ai" \
  --format raw
```

## Working Principles

- Keep search queries compact, entity-heavy, and task-specific.
- Keep the first pass small: usually `max_results=3..5`.
- Prefer explicit parameters over broad, vague prompting.
- Use Tavily-native knobs to match intent instead of stuffing instructions into the query.
- Default to `--include-answer` off and let downstream reasoning synthesize the answer.
- Default to `--include-raw-content` off on the first pass.
- Prefer `search -> extract` over `search + huge raw content`.
- Use `--auto-parameters` only as a recovery step or when the intent is genuinely ambiguous.

## Intent Profiles

Think in profiles, not in a flat list of low-level flags.
Choose the smallest profile that matches the task.

### `general`
Use for ordinary web search, concept lookup, background verification, and broad source finding.

Default shape:
- `topic=general`
- `search_depth=basic`
- `max_results=3..5`
- `include_answer=false`
- `include_raw_content=false`

### `news`
Use when the user asks about recent events, recent policy changes, sports, politics, or anything framed as latest, recent, today, or this week.

Default shape:
- `topic=news`
- add `time_range` or `start_date/end_date` when the time window matters
- start with `search_depth=basic`

### `finance`
Use for company, market, filings, earnings, and finance-specific information.

Default shape:
- `topic=finance`
- start with `basic`
- add `time_range` or domain filters if needed

### `official`
Use when the user implicitly wants official docs, vendor docs, standards, API references, or primary sources.

Default shape:
- `topic=general`
- use `include_domains`
- keep `max_results` small
- escalate to `advanced` only if the first pass is noisy

### `precision`
Use when exact wording, a specific page, or a narrow entity match matters.

Default shape:
- use quoted strings when appropriate
- consider `exact_match=true`
- use `search_depth=advanced`
- set `chunks_per_source=2..3`

### `regional`
Use when the source region matters more than the global web average.

Default shape:
- add `country`
- combine with `general`, `news`, or `finance` intent as needed

## Query Planning

Plan the query at the semantic level, then let Tavily do the retrieval work.

Good first-pass queries usually have these properties:
- one main information goal
- the main entities named explicitly
- little or no conversational filler
- no unnecessary formatting instructions
- optional date or source constraints only when they help retrieval

Prefer:
- `OpenClaw skills documentation site:docs.openclaw.ai`
- `SEC 10-K NVIDIA fiscal 2026`
- `Boston University data science tuition 2026 official`

Avoid:
- long essay prompts
- combining many unrelated asks in one query
- asking Tavily to already write the final answer inside the query

For detailed rewrite patterns, read:
- `references/query_playbook.md`

## Command Surface

The implementation lives at:
- `scripts/tavily.py`

### Search

```bash
python3 {baseDir}/scripts/tavily.py search --query "..."
```

Main flags:
- `--profile {general,news,finance,official,precision,regional}`
- `--topic {general,news,finance}`
- `--search-depth {ultra-fast,fast,basic,advanced}`
- `--max-results N`
- `--time-range {day,week,month,year}` or exact `--start-date YYYY-MM-DD --end-date YYYY-MM-DD`
- `--include-domains ...`
- `--exclude-domains ...`
- `--country ...`
- `--exact-match`
- `--auto-parameters`
- `--chunks-per-source N`
- `--include-answer [basic|advanced]`
- `--include-raw-content [markdown|text]`
- `--include-favicon`
- `--safe-search`
- `--format {agent,raw,md,brave}`

### Extract

```bash
python3 {baseDir}/scripts/tavily.py extract --urls "https://..."
```

Main flags:
- `--query ...` for reranking extracted chunks
- `--chunks-per-source N`
- `--extract-depth {basic,advanced}`
- `--content-format {markdown,text}`
- `--include-images`
- `--include-favicon`
- `--request-timeout SECONDS`
- `--format {agent,raw,md}`

### Map

```bash
python3 {baseDir}/scripts/tavily.py map --url "https://..."
```

Main flags:
- `--instructions ...`
- `--max-depth N`
- `--max-breadth N`
- `--limit N`
- `--select-paths ...`
- `--select-domains ...`
- `--exclude-paths ...`
- `--exclude-domains ...`
- `--allow-external` / `--no-allow-external` (default is to exclude external links)
- `--request-timeout SECONDS`
- `--format {agent,raw,md}`

For exact flag behavior, run `--help` on the relevant subcommand.

## Escalation Ladder

Use the lightest step that can solve the task.

### Step 1 — Small search
Start with a profile-aligned `search` call.

### Step 2 — Rewrite the query
If results are broad, stale, or noisy, rewrite the query before expanding result count.

### Step 3 — Refine parameters
Use one or more of:
- `topic`
- `time_range` or `start_date/end_date`
- `include_domains` / `exclude_domains`
- `country`
- `exact_match`
- `search_depth=fast|advanced`
- `chunks_per_source`

### Step 4 — Extract top URLs
When snippets are promising but insufficient, run `extract` on the best 1–3 URLs.
Pass the same user intent as `query` so Tavily can rerank extracted chunks.

### Step 5 — Map then extract
When the task is really about navigating a documentation site or knowledge base, map the site first, then extract selected pages.

### Step 6 — Stop escalating
If the top sources already answer the question, stop. Do not keep searching just because more knobs exist.

For the detailed decision tree, read:
- `references/escalation_rules.md`

## Output Philosophy

Expose a stable shape to the model while preserving Tavily signals that help planning.

Preferred default output is `agent`, which preserves:
- the original query
- the executed query and parameters
- the selected profile
- source domain
- score when available
- snippet or extracted content chunks
- usage metadata when available
- response time and request identifiers when available

Use `raw` when you need the closest representation of Tavily's response.
Use `md` for human inspection.
Use `brave` only when a downstream consumer expects a Brave-like result shape.

For the detailed schema, read:
- `references/output_contract.md`
- `references/param_matrix.md`

## When Not to Use This Skill

Do not use this skill when:
- the answer is fully contained in local files or already-open documents
- the task is pure writing or transformation with no need for external sources
- a specialized tool already exists for the target system
- the task is a large, asynchronous research workflow better handled by Tavily Research or another research-specific workflow

## Notes for the Implementer

This wrapper should reflect Tavily's design, not fight it.
Expose the parameters that matter for model planning, but still protect context size and credit usage with conservative defaults and stable output contracts.
