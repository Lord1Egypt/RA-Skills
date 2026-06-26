---
name: bounded-memory
description: Gives your OpenClaw AI a perfect memory. Ask things like "did we discuss this before?", "what did we decide about X?", and "find that conversation about Y" — it searches through all your past conversations instantly. Great for recalling decisions, preferences, and context from months ago. Use when: (1) user asks "did we talk about X before?", (2) "search my old conversations", (3) "find what we decided about project Y", (4) "remember what I asked last week". Triggers: "search sessions", "find earlier conversation", "recall past discussion", "what did I say about".

Privacy: search indexing and execution are 100% offline. LLM summarization is opt-in (use --llm flag) and disabled by default. No external API calls without your explicit consent.
---

# Bounded Memory

Gives your OpenClaw AI agent a **perfect memory** — it can recall anything you've ever discussed, even from months ago.

## What It Does

Without this skill: each OpenClaw session starts fresh. The AI forgets everything.

With this skill: ask things like:
- "Did we discuss X before?"
- "What did we decide about Y?"
- "Find that conversation from last month"

## Privacy Design

| What runs | How |
|-----------|-----|
| Search indexing | ✅ 100% offline — SQLite only |
| Search execution | ✅ 100% offline — no network calls |
| LLM summarization | ⚠️ Opt-in only — use `--llm` flag to enable |

**No external API calls by default.** The `--llm` flag (disabled by default) sends snippets to your configured LLM for summarization — only when you explicitly ask for it.

## Quick Start

```bash
# Index your conversations (first time)
python3 skills/session-search/scripts/index-sessions.py --agent main

# Search (fully offline)
python3 skills/session-search/scripts/search-sessions.py "what did we decide about the logo design"

# Search with AI summary (opt-in)
python3 skills/session-search/scripts/search-sessions.py "question" --llm
```

## What It Solves

| Problem | Without | With Bounded Memory |
|---------|---------|---------------------|
| "I asked this before but can't remember" | AI has no idea | Instant recall |
| "What did we decide in that meeting?" | Forgot | Searches all sessions |
| "Did I mention this before?" | No way to know | Searches everything |

## Example

```
You: "Search our conversations about the robot project"
→ Found 3 discussions:
  1. [Last week] We discussed the design direction...
  2. [2 weeks ago] You asked about pricing...
  3. [Last month] The AI suggested adding...
```
