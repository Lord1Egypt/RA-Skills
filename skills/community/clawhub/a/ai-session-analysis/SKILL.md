---
name: ai-session-analysis
description: Use when the user wants to analyze local AI coding assistant session data (Claude Code, Codex, Kimi Code). Triggers on requests like "analyze my coding sessions", "what tools do I use most", "compare Claude Code vs Codex usage", "give me a summary of what I've been working on", or similar session-analysis inquiries.
---

# AI Session Analysis

## Overview

Analyze session data from local AI coding tools. Three bundled scripts extract raw data. You (the agent) read the output and form your own observations — there are no hardcoded rules or thresholds in the scripts.

## Data Sources

Scripts read directly from these paths, no copying needed:

| Tool | Path | Content |
|------|------|---------|
| Claude Code | `~/.claude/projects/*.jsonl` | Full transcripts with `tool_use` blocks |
| Claude Code | `~/.claude/history.jsonl` | User input history |
| Claude Code | `~/.claude/sessions/*.json` | Session metadata |
| Codex | `~/.codex/sessions/*/*.jsonl` | Structured events |
| Kimi Code | `~/.kimi/sessions/*/wire.jsonl` | Wire protocol with ToolCall entries |

## How to Run

```bash
# Text-based analysis (terminal output)
python3 ~/.claude/skills/ai-session-analysis/scripts/analyze.py
python3 ~/.claude/skills/ai-session-analysis/scripts/tool_analysis.py

# HTML report with charts (opens in browser)
python3 ~/.claude/skills/ai-session-analysis/scripts/generate_report.py [output.html]
```

Zero dependencies, Python 3 stdlib only. All scripts are pure data extractors — they present numbers, distributions, and timelines without any interpretation.

## What Each Script Extracts

**analyze.py** — Overview:
- Per-tool: session count, message volume, tool distribution, project ranking, daily activity timeline, date range
- Cross-tool comparison table
- Recent 7-day activity: daily tool calls, active projects, tool mix, per-session timeline

**tool_analysis.py** — Deep dive:
- Shell command categories per tool (git, grep/find, npm/yarn, python, etc.)
- File operation counts (Read/Write/Edit) and file type distribution
- Project-level tool usage breakdown
- Codex: token usage, web search topics, errors
- Kimi: domain-specific tools beyond the standard set

**generate_report.py** — HTML report:
- Self-contained HTML file with embedded data and Chart.js visualizations
- Summary cards, daily activity timeline, tool distribution doughnut, project breakdown
- Shell command comparison across all three tools
- File operations, token usage, session timeline scatter plot
- Session duration distribution, hour-of-day activity heatmap
- Codex deep dive (patches, web searches, exit codes)
- Kimi domain tools

## After Running

Read both outputs carefully. Then tell the user what you see. Consider:

- What are they actually doing? (exploring code vs building features vs debugging vs reviewing)
- Which projects are getting attention, which ones went quiet?
- Tool use patterns: are they leaning heavily on one tool? is the tool mix appropriate for their work?
- Cross-tool: did they try one tool then switch? what might that say?
- Recent vs historical: any shifts in behavior, intensity, or focus?
- Anything that looks like friction: lots of failed commands, retries, errors?

**Do not** apply fixed thresholds or rules ("if bash > 40% then warn"). Look at the whole picture and use judgment. If something stands out, mention it. If nothing does, say so.

## Security Note

The HTML report (`generate_report.py`) embeds your session data directly — file paths, shell commands, project names, and tool usage patterns. This is safe for personal use on your own machine, but **do not share the generated HTML file** with others or host it publicly. The terminal-based scripts (`analyze.py`, `tool_analysis.py`) only print aggregate statistics and are safe to share.

## Common Issues

- **Claude Code shows few tools**: Tools are in `~/.claude/projects/*.jsonl` (assistant → content blocks with `"type": "tool_use"`), not in `history.jsonl`.
- **Codex sessions empty**: Check `~/.codex/sessions/2026/` subdirectories (organized by year/month/day).
- **Kimi tool names missing**: ToolCall entries are in `wire.jsonl` via `payload.function.name`.
