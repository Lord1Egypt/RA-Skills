---
name: agentype
description: >-
  Run the Agentype workflow for local AI-agent usage analysis: collect and cache deterministic JSON, infer a persona/archetype from aggregate usage signals, then render a terminal summary or PNG poster. Supports Claude Code, Codex, OpenCode, pi-agent, Gemini CLI, OpenClaw, Nanobot, and configured Nanobot-compatible roots. Use when the user asks to understand their agent usage, AI workflow, token footprint, preferred agents/models/projects, or "agentype".
version: 0.1.8
tags: [ai-agents, analytics, persona, tokens, local-first]
---

# Agentype

Agentype summarizes a user's local AI-agent history into a persona/archetype and usage overview.

**When this skill is triggered, you MUST complete all four steps below.** Do not stop after collecting stats, do not skip persona inference, and do not skip delivering the final poster or summary to the user.

## When to Use

Use this skill when the user asks:

- "what is my agentype?"
- "analyze my agent usage"
- "show my AI usage stats"
- "which agents or models do I use most?"
- "what persona am I based on my AI workflow?"
- `/agentype`

Do not use it for billing estimates. Agentype reports tokens and local usage signals, not provider invoices.

## What It Reads

Agentype collects local session and token metadata from supported agents where available:

- Claude Code
- Codex
- OpenCode
- pi-agent
- Gemini CLI
- OpenClaw
- Nanobot
- Nanobot-compatible JSONL roots configured through `AGENTYPE_NANOBOT_ROOTS`

## Required Workflow (all four steps are mandatory)

The PyPI distribution is `agentype-cli` because `agentype` is not available on PyPI. The installed command is still `agentype`.

### Step 1 — Collect stats

Run the CLI with `--json-out` to collect deterministic usage data and write it to `output/agentype.json`:

```bash
agentype --json-out
```

If `agentype` is not installed and there is no source checkout:

```bash
uvx --from agentype-cli agentype --json-out
```

From a source checkout:

```bash
uv run agentype --json-out
```

> The CLI output at this point is raw stats only — it is **not** the final result. Continue to the next step.

### Step 2 — Infer and fill the persona (agent-side, no CLI call)

Read `output/agentype.json`. From the aggregate signals — top projects, agents, models, skill metadata, token shape, and usage rhythm — infer the user's persona yourself. Then write these four top-level fields back into `output/agentype.json`, preserving all other fields:

- `archetype`: short persona label (e.g. "Polyglot Automator").
- `description`: one-line explanation of the archetype.
- `keywords`: 3–6 concise keywords.
- `comment`: 2–3 evidence-grounded sentences starting with "You are a...".

### Step 3 — Render the filled JSON

Pass the updated file back to the CLI to produce the final formatted output:

```bash
agentype --json-in output/agentype.json
```

For chat, IM, or gateway environments that can display images, also generate the poster:

```bash
agentype --json-in output/agentype.json --png-out
```

### Step 4 — Deliver to the user

- **Terminal agents**: relay the full rendered text output (persona/archetype + top stats) directly to the user.
- **Chat or IM gateway agents**: send a compact text summary and attach `output/agentype.png`.

Do not expose raw session files, prompts, private transcripts, or full JSON unless the user explicitly asks for debugging data.

## Custom Local Paths

If the user's agent history lives outside default locations, configure `AGENTYPE_NANOBOT_ROOTS` before Step 1:

```bash
AGENTYPE_NANOBOT_ROOTS="/path/to/workspace:/path/to/another/root" agentype --json-out
```

For unsupported agent layouts, the collector paths live in `src/agentype/paths.py` and source adapters in `src/agentype/sources/`.

## Debugging

If the user asks for debugging or validation, re-run Step 1 with `-v` and share the verbose output:

```bash
agentype -v --json-out
```
