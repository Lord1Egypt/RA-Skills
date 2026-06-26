---
name: exa-research
description: Use the local `exa` CLI to search the live web, ask grounded questions with citations, fetch page contents, find similar links, retrieve Exa code context, or manage Exa research tasks. Use when the task needs current web information, source-backed answers, URL/page extraction, related-link discovery, code examples from the web, or Exa-specific API access. Prefer this over generic web search when Exa highlights, answer synthesis, or research workflows are specifically useful.
homepage: https://github.com/jdegoes/exa
metadata:
  {
    "openclaw":
      {
        "emoji": "🔎",
        "requires": { "bins": ["exa"], "env": ["EXA_API_KEY"] },
        "primaryEnv": "EXA_API_KEY",
      },
  }
---

# Exa Research

Use the bundled wrapper to run Exa reliably:

```bash
{baseDir}/scripts/exa-with-key.sh --help
```

## Credentials

Preferred OpenClaw-native setup:

- `skills.entries.exa-research.apiKey`
- or `skills.entries.exa-research.env.EXA_API_KEY`

Other supported auth sources:

- ambient `EXA_API_KEY`
- `EXA_API_KEY_FILE`
- default file fallback at `~/.openclaw/credentials/exa/api-key.txt`

The wrapper prefers credentials in this order:

1. existing `EXA_API_KEY`
2. `EXA_API_KEY_FILE`
3. the default file path above

## Route to the smallest command that fits

- Use `search` for live web discovery and filtered result lists.
- Use `answer` for one grounded answer with citations.
- Use `contents` when URLs or result IDs are already known and text/highlights/summary are needed.
- Use `similar` when one seed URL is known and related pages are needed.
- Use `context` for coding patterns, library usage, and implementation examples.
- Use `research` for asynchronous or longer-running research workflows.
- Use `raw` only when a higher-level command cannot express the request.

## Keep context lean

- Start narrow; broaden only if recall is poor.
- Prefer `answer` over manual search-plus-synthesis when the user wants a concise cited answer.
- Prefer `highlights` before full `text` when excerpts are enough.
- Cap payload size with `--text-max`, `--highlights-max`, and `context --tokens`.
- Add domains, categories, and date filters early instead of retrieving broad result sets.
- Do not dump large raw payloads into chat when a short synthesis will do.

## Command patterns

### Search

```bash
{baseDir}/scripts/exa-with-key.sh "latest developments in llms"
{baseDir}/scripts/exa-with-key.sh search --category news --include-domain reuters.com --highlights "AI regulation"
{baseDir}/scripts/exa-with-key.sh search --type deep --additional-query "llm releases" "latest frontier models"
```

### Answer

```bash
{baseDir}/scripts/exa-with-key.sh answer "What is the latest valuation of SpaceX?"
{baseDir}/scripts/exa-with-key.sh answer --text "What changed in the latest OpenAI release?"
```

### Contents

```bash
{baseDir}/scripts/exa-with-key.sh contents --text https://exa.ai
{baseDir}/scripts/exa-with-key.sh contents --id doc-1 --id doc-2 --highlights
{baseDir}/scripts/exa-with-key.sh contents --highlights --summary https://exa.ai https://example.com
```

### Similar

```bash
{baseDir}/scripts/exa-with-key.sh similar --highlights https://arxiv.org/abs/2307.06435
{baseDir}/scripts/exa-with-key.sh similar --text --text-max 3000 https://exa.ai/blog
```

### Context

```bash
{baseDir}/scripts/exa-with-key.sh context "React hooks for state management"
{baseDir}/scripts/exa-with-key.sh context --tokens 5000 "pandas dataframe filtering and groupby operations"
```

### Research

```bash
{baseDir}/scripts/exa-with-key.sh research create "Summarize the latest developments in AI safety research"
{baseDir}/scripts/exa-with-key.sh research list --limit 10
{baseDir}/scripts/exa-with-key.sh research get 01jszdfs0052sg4jc552sg4jc5
```

### Raw

```bash
{baseDir}/scripts/exa-with-key.sh raw /search @payload.json
{baseDir}/scripts/exa-with-key.sh raw -X GET '/research/v1?limit=10'
printf '{"query":"latest llm news"}' | {baseDir}/scripts/exa-with-key.sh raw /search -
```

## Practical guidance

- Run `{baseDir}/scripts/exa-with-key.sh <subcommand> --help` before guessing flags.
- If the task is exploratory, start with `search`, then escalate to `contents` only for selected URLs.
- If the task is code-oriented, prefer `context` over broad search.
- If the task needs longer-running synthesis, prefer `research` over ad hoc polling with `raw`.
- If the user asks for the upstream generated skill text, run `exa skill`.
