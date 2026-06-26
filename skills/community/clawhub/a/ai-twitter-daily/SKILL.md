---
name: ai-twitter-daily
description: Generate daily AI Twitter report from top AI researchers and companies. Use when user asks for AI Twitter summary, daily AI news, or wants to track AI community discussions.
---

# AI Twitter Daily Report

Generate comprehensive daily reports tracking AI researchers and companies on Twitter/X.

## Setup

Set required environment variables:

```bash
export GROK_API_KEY="your-api-key-here"
export GROK_API_URL="https://api.cheaprouter.club/v1/chat/completions"  # optional
export GROK_MODEL="grok-4.20-beta"  # optional
```

## Usage

Run the daily report script:

```bash
python3 scripts/daily_report.py
```

## What It Tracks

- **User Interactions**: Who replied/retweeted/mentioned whom
- **High-frequency Mentions**: AI models, companies, papers, tools, projects, events
- **Hot Topics**: AGI timeline, open vs closed source, safety/alignment, embodied AI, multimodal, new architectures, Agent progress
- **Daily Summary**: Latest AI developments and discussion highlights

## Monitored Accounts

See `references/users.txt` for the full list of 22+ top AI researchers and organizations.

## Output Format

Structured Chinese report with tables and bullet points for easy daily tracking.
