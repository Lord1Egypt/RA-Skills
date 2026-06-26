# 🔬 Open Deep Research — AI Skill for OpenClaw

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-5B45E9)](https://openclaw.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/midboss1028-beep/claw-deep-research?style=social)](https://github.com/midboss1028-beep/claw-deep-research)

**Turn your AI agent into a real research assistant.** Not the "search-and-summarize" kind — the kind that goes layer by layer, finds contradictions, cross-checks sources, and delivers a structured report.

Inspired by [dzhng/deep-research](https://github.com/dzhng/deep-research) (17.8k ⭐) and the architecture of [MiroMind/MiroThinker](https://dr.miromind.ai) (SOTA on GAIA/BrowseComp), but built entirely on OpenClaw's native capabilities.

Zero extra API keys. One folder drop-in. Any LLM, any search provider.

---

## Why This Exists

Most AI "research" tools just do one round: search → summarize → done. That's not research — that's a quick Google.

Real research means:
1. **Scan broadly** — cover all dimensions of a topic
2. **Find the cracks** — contradictions, gaps, single-source claims
3. **Dig deep** — targeted searches on what actually matters
4. **Verify** — cross-check key data points across multiple sources
5. **Synthesize** — a structured report with confidence levels, not just bullet points

This skill does all five, automatically.

---

## Quick Start

### Install

```bash
# Via ClawHub (recommended)
clawhub install claw-deep-research

# Or manual
cd ~/.openclaw/workspace/skills
git clone https://github.com/midboss1028-beep/claw-deep-research.git

# Restart gateway
openclaw gateway restart
```

### Trigger

```bash
/deep EV battery supply chain 2026
/deep research open source LLM monetization strategies
```

Or just say it naturally — the agent picks up on phrases like:
- "Do a deep dive on..."
- "Research the competitive landscape of..."
- "I need a comprehensive analysis of..."

---

## How It Works

### The Pipeline

```
Phase 1: Panoramic Scan  ──→  Phase 2: Gap Analysis  ──→  Phase 3: Targeted Deep Dive  ──→  Phase 4: Cross-Verification  ──→  Phase 5: Report
  (3-5 broad queries)       (find contradictions)       (6-10 precision queries)         (validate key data)           (structured output)
```

Not a rigid tree — a **reflective pipeline**. At each phase, the agent pauses to think before deciding where to search next.

### Two Execution Modes

| Mode | How it works | Best for |
|------|-------------|----------|
| **Inline** | Runs step-by-step in your current conversation | First-time use, narrow topics |
| **Sub-agent** | Spawns a dedicated research agent in the background | Deep dives, IM channels, don't-wait scenarios |

The sub-agent mode is particularly useful for chat apps (Telegram, Discord, WeChat) — you get a brief summary in chat and the full report saved to your Desktop.

---

## Output

You get a **brief summary** in chat (mobile-friendly, 15 lines max), and the **full report** saved as a Markdown file:

```
🔬 EV Battery Supply Chain 2026 — Deep Research Report

📊 Covered 6 dimensions, 18 searches, 24 research cards

Key Findings:
• China controls 75% of global battery cell production
• LFP chemistry now dominates at 55% market share, up from 30% in 2023
• Sodium-ion batteries entering commercial production at $45/kWh

Bottom Line: Market consolidation accelerating, vertical integration is the winning strategy for 2026

📁 Full report saved to: ~/Desktop/EV-Battery-Supply-Chain-2026-深度研究报告.md
```

### Report Structure

Every report includes:
- **Scope & Methodology** — what was searched, confidence notes
- **Core Findings** — by subtopic, each with confidence level (High/Medium/Low)
- **Contradictions & Controversies** — data points that don't agree
- **Synthesis** — cross-dimensional analysis and trends
- **Limitations** — what wasn't covered, where data is thin
- **Sources** — all referenced URLs

---

## What Makes This Different

| vs. | Single search | Typical AI deep research | This skill |
|-----|:------------:|:------------------------:|:----------:|
| Search rounds | 1 | fixed breadth×depth tree | **adaptive, contradiction-driven** |
| Data verification | none | none | **multi-source cross-check** |
| Confidence scoring | none | none | **High/Medium/Low on every claim** |
| Contradictions | ignored | ignored | **explicitly mined and reported** |
| Execution | inline | inline only | **inline + background sub-agent** |
| Chat delivery | full text | full text | **summary only, file for details** |
| Cross-platform | - | - | **macOS / Linux / Windows** |
| Cost | any | extra API keys needed | **zero additional cost** |

---

## Requirements

Zero. Just a running OpenClaw instance with a `web_search` provider configured.

- **Search:** MiniMax / Tavily / Brave / Google / Perplexity / DuckDuckGo — doesn't matter
- **LLM:** DeepSeek, MiniMax, Claude, GPT — doesn't matter
- **OS:** macOS, Linux, Windows — doesn't matter
- **Extra API keys:** **none needed** — reuses what you already have

---

## File Save Fallback

The agent tries to save the full report to your Desktop, but gracefully degrades:

```
Desktop writable?      → ~/Desktop/report.md ✓
   ↓ (no)
Workspace writable?    → .openclaw/workspace/report.md ✓
   ↓ (no)
Temp dir writable?     → /tmp/report.md ✓
   ↓ (no)
Nothing works?         → full report in chat (last resort)
```

---

## License

MIT — use it, share it, fork it, ship it.
