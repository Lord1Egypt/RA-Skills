---
name: gemini-deep-research
description: "Gemini Deep Research via the gemini-cli deep-research MCP extension. Use when user wants to research a topic deeply, run market/industry analysis, or generate a comprehensive report. Triggers on: deep research X, 帮我研究 X, gemini deep research X, 研究一下 X, do a deep search on X. Requires the gemini-cli and gemini-deep-research extension to be installed and a paid Google AI API key to be configured."
---

# Gemini Deep Research

Executes a full Deep Research workflow using the official `gemini-deep-research` MCP extension.

## Prerequisites

See `references/setup-guide.md` for full setup instructions. The skill assumes:

- `gemini` CLI installed (`npm install -g @google/gemini-cli`)
- `gemini-deep-research` extension installed and enabled
- Paid Google AI API key configured via `gemini extensions config gemini-deep-research`

If any prerequisite is missing, inform the user and link to `references/setup-guide.md`.

## Workflow

### Step 1 — Confirm Intent & Parameters

Ask the user to confirm:

1. **Research topic** (exact wording goes to Gemini — make it clear and specific)
2. **Report format** — present as a choice:
   - `Comprehensive Research Report` (default, most thorough)
   - `Executive Brief` (concise, ~1-2 pages)
   - `Technical Deep Dive` (detailed, technical audience)
3. **Save path** — default: `~/ObsidianVault/Default/DeepResearch/<YYYYMMDD>-<slug>.md`

If user does not specify format, use `Comprehensive Research Report`.

If user does not specify a save path, use the default and inform them.

### Step 2 — Build the Command

```bash
node <skill>/scripts/dr-client.js \
  --input "<user's research topic>" \
  --output "<full save path>" \
  --format "<chosen format>" \
  --timeout 900000
```

- `<skill>` = the skill's scripts directory (resolved by the agent)
- Timeout defaults to 15 minutes (900,000 ms)

### Step 3 — Spawn as Background Sub-agent

Use `sessions_spawn` with `runtime: "subagent"` to run the script in the background so the main session remains responsive.

Pass all parameters (input, output, format, timeout) via the `task` string.

Monitor completion via the sub-agent's completion event.

### Step 4 — Handle Result

Parse the JSON output from the script:

- `status: "completed"` → Report the success to the user with the file path
- `status: "error"` → Report the error message to the user with a suggestion to check the API key or extension setup

### Step 5 — Notify

Send a Discord message (via current session reply) confirming:
- Topic researched
- File path
- Format used
- Any errors if applicable

## Report Format Reference

| Format | Description |
|--------|-------------|
| `Comprehensive Research Report` | Full multi-section report with analysis, data, and citations |
| `Executive Brief` | Condensed summary for decision-makers, ~1-2 pages |
| `Technical Deep Dive` | Detailed technical analysis, suited for specialists |

The format is passed as-is to the Gemini API — it serves as a style hint, not a strict guarantee.

## Error Handling

| Error | Likely Cause | Resolution |
|-------|-------------|------------|
| `API key not found` | Key not configured | Guide user to `references/setup-guide.md` step 4 |
| `429 Too Many Requests` | Free-tier key used or quota exceeded | Requires paid key — inform user |
| `Research timed out` | Took > 15 minutes | Retry or shorten query |
| MCP server spawn failed | Extension not installed or path wrong | Verify `~/.gemini/extensions/gemini-deep-research/` exists |

## File Naming

Default pattern: `YYYYMMDD-<slug>.md`

- `YYYYMMDD` = today's date
- `<slug>` = sanitized version of the research topic (lowercase, spaces to hyphens, strip special chars)
- Example: `20260325-iran-hormuz-strait-market-impact.md`
