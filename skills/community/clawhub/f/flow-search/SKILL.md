---
name: flow-search
description: Deep web research using Claude's native search tool. Use for comprehensive research, market analysis, competitor intelligence, or when standard search isn't enough. Free from the Flow team.
metadata:
  clawdbot:
    emoji: "🔍"
  requires:
    env:
      - name: CLAUDE_CODE_OAUTH_TOKEN
        description: Claude Code auth token — run `claude auth login` to get one. Required for all searches.
  spawns:
    - process: claude
      reason: Executes Claude CLI as a subprocess to perform native web search with synthesis. Inherits shell environment to access CLAUDE_CODE_OAUTH_TOKEN. No data is sent anywhere else.
---

# FlowSearch — Deep Web Research

**Free deep research powered by Claude Max subscription.**

Stop getting shallow answers. FlowSearch uses Claude's native search to go wide and deep — pulling from multiple sources, synthesizing conflicting information, and giving you the kind of answer a thorough analyst would write, not a one-liner.

## How it works

FlowSearch spawns Claude CLI as a subprocess with your `CLAUDE_CODE_OAUTH_TOKEN`. Claude performs multi-source web search, synthesizes the results, and returns a structured report. No data is sent to third-party APIs — it's just Claude doing what Claude does best.

> **Security note:** This skill spawns a `claude` process that inherits your shell environment to access `CLAUDE_CODE_OAUTH_TOKEN`. Review the source (`search.ts`) before running — it's 150 lines and straightforward.

## Prerequisites

1. **Claude Code CLI** — install from [claude.ai/code](https://claude.ai/code)
2. **Authenticate:** run `claude auth login` (opens browser)
3. **Claude Max subscription** recommended for best results (more search depth)

## Installation

```bash
npx clawhub@latest install flow-search
cd ~/.openclaw/skills/flow-search
npm install
```

## Usage

### Quick search (15–30s)
```bash
npx tsx search.ts "Kling AI pricing 2026"
```

### Deep research (60–180s)
```bash
npx tsx search.ts --deep "AI video generation competitive landscape"
```

### In your own skills or agents
```typescript
import { claudeSearch, claudeResearch } from "./search.ts";

// Quick answer with sources
const result = await claudeSearch("What is Kling AI pricing?");
if (result.success) console.log(result.answer);

// Deep research with guiding questions
const report = await claudeResearch("AI video market 2026", [
  "Who are the top 5 players and their pricing?",
  "What's the total addressable market?",
  "Which companies raised funding in the last 6 months?"
]);
```

## Output format

**Quick search** returns a direct answer with cited sources.

**Deep research** (`--deep`) returns a full structured report:

```
## Summary
2–3 sentence overview of findings.

## Key Findings
- Specific fact with source
- Specific fact with source
- ...

## Details
Full analysis with context.

## Sources
- [Publication Name](https://url)
```

## When to use FlowSearch vs Brave Search

| Use FlowSearch | Use Brave |
|----------------|-----------|
| Market analysis | Quick fact check |
| Competitor deep-dives | Single answer needed |
| Multi-source synthesis | Fast lookup |
| Recent news + context | Basic info |
| "What's the full picture on X?" | "What year was X founded?" |

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CLAUDE_CODE_OAUTH_TOKEN` | Yes | From `claude auth login` |

## Options

| Flag | Description |
|------|-------------|
| `--deep` / `-d` | Deep research mode (slower, more thorough) |
| `--help` / `-h` | Show usage |

## Integration example — use inside another OpenClaw skill

```typescript
// In your skill's handler
import { claudeResearch } from "~/.openclaw/skills/flow-search/search.ts";

const intel = await claudeResearch(`Competitor analysis: ${companyName}`, [
  "What are their pricing tiers?",
  "Who are their target customers?",
  "What are their main weaknesses?"
]);

if (intel.success) {
  // Pass intel.answer to your LLM or store it
}
```

## Timeouts

- Quick search: 2 minutes max
- Deep research: 3 minutes max

## About

Built by the [Flow team](https://clawhub.com/windseeker1111). Free, MIT-0 licensed — use it, fork it, build on it.

Other Flow skills: [FlowCrawl](https://clawhub.com/windseeker1111/flowcrawl) · [FlowConcierge](https://clawhub.com/windseeker1111/flowconcierge) · [FlowForge](https://clawhub.com/windseeker1111/flowforge)
