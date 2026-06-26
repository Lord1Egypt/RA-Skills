---
name: costclaw
version: 0.2.0
description: >
  Zero-setup token cost analyzer for OpenClaw. Run one command, get a ranked report
  with exact dollar amounts for every optimization. No Python dependencies, no integration
  needed — reads your actual config and workspace. Use when users mention high API costs,
  token consumption, budget, "why is my bill so high", "help me save money", or "optimize costs".
license: MIT
compatibility: OpenClaw v2026.2+
metadata:
  author: ClawdActual
  homepage: https://github.com/Morpheis/costclaw
  category: optimization
  tags: [cost, tokens, optimization, budget, savings, billing]
---

# CostClaw — Token Usage Optimizer

**One command. Zero setup. Real dollar amounts.**

Most OpenClaw users overpay by 50-90%. CostClaw reads your actual config and workspace, then tells you exactly what to change and how much you'll save.

## Why CostClaw vs Alternatives?

| Feature | CostClaw | Others |
|---------|----------|--------|
| Zero setup | ✅ Just run it | ❌ Install Python scripts, configure integration |
| Reads YOUR config | ✅ Actual gateway config + workspace | ❌ Generic advice |
| Dollar amounts per file | ✅ "$TOOLS.md costs $4.20/mo" | ❌ "Consider trimming" |
| Priority ranking | ✅ Top actions by savings | ❌ Unranked checklist |
| Before/after estimate | ✅ Current vs optimized cost | ❌ Percentage ranges |
| Single command | ✅ `./scripts/analyze.sh` | ❌ 4+ scripts to learn |

## Usage

### As an Agent (Recommended)

When the user asks about costs, the agent should:

1. **Run the analyzer script:**
   ```bash
   bash scripts/analyze.sh [workspace_path]
   ```
   Default workspace: current directory. Pass explicit path if needed.

2. **For JSON output** (machine-readable):
   ```bash
   bash scripts/analyze.sh [workspace_path] json
   ```

3. **Present findings** using the report output — prioritized recommendations with dollar amounts.

### Trigger Phrases

Activate this skill when users say anything like:
- "How much am I spending on tokens?"
- "Why is my API bill so high?"
- "Optimize my costs" / "Help me save money"
- "Run a cost audit"
- "Is my setup efficient?"

### What the Analyzer Checks

1. **Workspace files** — Size of every .md file injected per turn, with per-file monthly cost
2. **Installed skills** — Count and estimated token overhead from skill descriptions
3. **Model pricing** — Current cost based on detected/configured default model
4. **Heartbeat impact** — Cost of heartbeat polling at current interval
5. **Context injection total** — Sum of all per-turn token overhead

### Reading the Report

The report has 5 sections:

1. **📁 Workspace Files** — Each file with size, estimated tokens, and monthly cost. Flagged: ⚠ LARGE (>10K tokens), ⚡ MEDIUM (>5K tokens), ✓ OK.

2. **🔧 Skills** — Count of installed skills and their aggregate token cost.

3. **⚙️ Model & Config** — Detected default model and its pricing tier.

4. **💰 Cost Summary** — Daily and monthly estimates based on actual workspace + assumed turns/day.

5. **📋 Ranked Recommendations** — Prioritized by monthly savings. Each recommendation includes:
   - What to change
   - Why it saves money
   - Estimated monthly savings in dollars
   - How to implement it

### Agent Actions After Analysis

Based on findings, the agent should:

- **For oversized files (>10K tokens):** Offer to trim them — move rarely-used sections to `memory/` files, archive old content
- **For model routing:** Suggest config changes for heartbeat/cron model overrides
- **For skill bloat:** Identify unused skills and offer to disable them
- **For heartbeat frequency:** Calculate optimal interval considering cache TTL

## Pricing Reference (March 2026)

The analyzer uses these rates. Update `scripts/pricing.env` to override.

| Provider | Model | Input $/MTok | Output $/MTok | Cache Read | Cache Write |
|----------|-------|-------------|--------------|------------|-------------|
| Anthropic | Claude Opus 4 | $15.00 | $75.00 | $1.875 | $18.75 |
| Anthropic | Claude Sonnet 4.5 | $3.00 | $15.00 | $0.30 | $3.75 |
| Anthropic | Claude Haiku 4 | $0.80 | $4.00 | $0.08 | $1.00 |
| OpenAI | GPT-4.1 | $2.00 | $8.00 | $0.50 | — |
| OpenAI | GPT-4.1 mini | $0.40 | $1.60 | $0.10 | — |
| OpenAI | o3 | $2.00 | $8.00 | — | — |
| OpenAI | o4-mini | $1.10 | $4.40 | — | — |
| Google | Gemini 2.5 Pro | $1.25 | $10.00 | — | — |
| Google | Gemini 2.5 Flash | $0.15 | $0.60 | — | — |

## Key Optimization Patterns

### 1. Workspace File Trimming (Biggest Win)
Most agents load 30-80K tokens of workspace files every turn. Trimming to essentials saves 50-80% of input costs.

### 2. Model Routing for Background Tasks
Heartbeats and cron jobs don't need Opus. Route to Haiku/Flash for 10-20x savings on background work.

### 3. Heartbeat Cache Alignment
Set heartbeat interval to 55 minutes (just under Anthropic's 1h cache TTL). Keeps cache warm = cache-read rates instead of cache-write rates.

### 4. Lazy Skill Loading
Each skill description adds ~200-500 tokens to system prompt. 20 skills = 4-10K extra tokens/turn. Consider a skill index that loads on-demand.

### 5. Context Pruning
Enable `compaction.mode: aggressive` with `maxTokens: 8000` to auto-trim conversation history.

## Privacy

All analysis runs locally. No data leaves your machine. No API calls for the audit.

---

## 🦞 CostClaw Pro — Deep Optimization Package

The free analyzer gives you a ranked report. **CostClaw Pro** gives you the tools to automate savings:

- **Session Cost Tracking** — Log per-session token costs to JSONL for historical analysis
- **Spend Alerts** — Configurable daily spend thresholds with notifications
- **Automated Config Patches** — One-command config optimization with dry-run mode
- **Cost History Viewer** — Historical trend analysis with stats
- **Pre-built Routing Configs** — Optimal, balanced, and aggressive-savings model routing templates
- **5,600+ Word Optimization Guide** — Every pattern explained with implementation details
- **Full Model Comparison Matrix** — Pricing, performance, and recommendations for every major provider

**Get CostClaw Pro:** https://buy.polar.sh/polar_cl_qKdQKVcwHd4TUo8jXWrDoZyjHZm3rSciMyVCG00EJlO

**Storefront:** https://polar.sh/morpheis

---

**Author:** ClawdActual ([@clawdactual](https://github.com/Morpheis))
**License:** MIT
