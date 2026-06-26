---
name: memory-management
description: Recall and write workspace memory for OpenClaw agents using MEMORY.md, memory/YYYY-MM-DD.md, memory_search, and memory_get. Use when the user asks about prior work, decisions, dates, people, preferences, todos, or says to remember something; also use when you need to store durable notes or explain how OpenClaw memory works.
---

# Memory Management

Retrieve first. Write only what should persist.

## Core model

- `MEMORY.md` — curated long-term memory
- `memory/YYYY-MM-DD.md` — daily notes and running context
- `memory_search` — find likely snippets
- `memory_get` — read exact lines needed

## Retrieval

When user asks about prior work, decisions, dates, people, preferences, or todos:

1. `memory_search` with a tight, specific query.
2. `memory_get` for the needed lines only.
3. Answer from retrieved text, not guesswork.
4. If results are weak or empty, say you checked.

Good queries: `omar internship goal fall 2026`, `notion workspace page id`
Bad queries: whole paragraphs, vague terms like `memory`

## Writing

Write when user says "remember this," states a durable preference, or makes a decision that matters later.

| Destination | What goes there |
|---|---|
| `MEMORY.md` | Standing preferences, durable facts, recurring workflows, important long-term decisions |
| `memory/YYYY-MM-DD.md` | Day-to-day notes, progress, one-off events, session context |

Rules:
- smallest useful note
- concrete facts over commentary
- no secrets unless asked
- do not promise memory unless written

## When not to use

Skip retrieval when the answer is in the current message or task is current-turn only.
Skip writing when the fact is trivial, belongs in project docs, or is temporary scratch.

## Answering rules

- Cite file path/line when useful
- Separate memory facts from inference
- Flag stale memory
- If unavailable, say so
