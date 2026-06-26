# Bounded Memory

[![Version](https://img.shields.io/badge/version-v1.1.1-blue.svg)](https://github.com/canmaxice-maker/bounded-memory)
[![ClawHub](https://img.shields.io/badge/ClawHub-bounded--memory-green.svg)](https://clawhub.com/bounded-memory)

**Gives your OpenClaw AI a perfect memory.** Search through all your past conversations instantly — recall decisions, preferences, and context from months ago.

## The Problem It Solves

OpenClaw AI starts fresh every session. It forgets everything from previous chats.

That means every new session, you have to re-explain:
- Your projects and preferences
- Past decisions you've made
- What you discussed and agreed on
- Context from earlier conversations

**Bounded Memory fixes this.** It gives your AI an always-on memory of everything you've ever discussed.

## What You Can Do

```
"Did we discuss the logo design?"
→ Instantly finds all relevant past conversations

"What did we decide about the budget?"
→ Shows you the exact discussion and decision

"Find that conversation about the robot project from last month"
→ Pulls it up immediately
```

## How It Works

```
1. Index (once)
   Your conversation files → Local search database (SQLite)

2. Search (anytime you ask)
   Your question → Instant results from full history

3. Recall
   You get the answer + the original conversation context
```

## Privacy First

- **100% offline search** — SQLite FTS5 runs entirely on your machine
- **No external services** — search indexing never calls any API
- **LLM is opt-in** — disabled by default, only enabled when you add `--llm`
- **You control it** — uninstall anytime, remove the database anytime
- **Git-ignored** — your conversation database is never committed

## Installation

```bash
# ClawHub (recommended)
clawhub install bounded-memory

# Manual
git clone https://github.com/canmaxfire/bounded-memory.git
mv bounded-memory ~/.openclaw/workspace/main/skills/session-search
```

## Quick Start

```bash
# 1. Index your conversations (first time)
python3 ~/.openclaw/workspace/main/skills/session-search/scripts/index-sessions.py --agent main

# 2. Search (fully offline, no external calls)
python3 ~/.openclaw/workspace/main/skills/session-search/scripts/search-sessions.py "your question"

# 3. Optional: enable AI summaries of results (requires API key)
python3 ~/.openclaw/workspace/main/skills/session-search/scripts/search-sessions.py "question" --llm
```

## Privacy Details

| Feature | Behavior |
|---------|----------|
| Search indexing | ✅ Fully offline — SQLite FTS5 only |
| Search execution | ✅ Fully offline — no network calls |
| LLM summarization | ⚠️ Opt-in only — disabled by default |
| API key | Only read if `--llm` flag is used |

The `--llm` flag reads your LLM API key from `~/.openclaw/openclaw.json` and sends the conversation snippets to your configured LLM endpoint for summarization. Without `--llm`, no external calls are made.

## What Changes

| Before | After |
|--------|-------|
| "I know we discussed this before but..." | "Found it — we talked about this on April 3rd" |
| AI has no idea what you asked last month | Instantly recalls months of conversations |
| Re-explaining context every session | Context carries across all sessions |
| Forgetting important decisions | Never lose track of what was decided |

## Architecture

```
~/.openclaw/agents/main/sessions/*.jsonl
    ↓ (indexed once, updated daily)
~/.openclaw/workspace/main/skills/session-search/db/sessions.db
    ↓ (searched on demand — no network)
Instant results from your full conversation history
```

## Credits

Inspired by [Hermes Agent](https://github.com/NousResearch/hermes-agent)'s bounded memory architecture.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| [v1.1.1](https://github.com/canmaxice-maker/bounded-memory/releases/tag/v1.1.1) | 2026-04-21 | Fix: LLM is now truly opt-in, docs match code |
| [v1.1.0](https://github.com/canmaxice-maker/bounded-memory/releases/tag/v1.1.0) | 2026-04-21 | Rewrite: plain language, user benefit focus |
| [v1.0.0](https://github.com/canmaxice-maker/bounded-memory/releases/tag/v1.0.0) | 2026-04-21 | Initial release |

## License

MIT
