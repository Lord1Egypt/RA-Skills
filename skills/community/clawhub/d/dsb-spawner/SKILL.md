---
name: spawner
description: Spawn sub-agents for independent work that needs file edits, builds, or long-running tasks. Use when work is too heavy for inline execution. NOT for quick reads, one-liner fixes, or anything under 2 minutes.
---

# Spawner

## Before Spawning
1. **Role**: Pick ONE — coder, writer, browser-automator, researcher, reviewer.
2. **Exit criteria**: What artifact proves done? A file path, URL, test result.
3. **Context**: Only inject files the agent needs. Task description under 2K tokens.

## Model Routing
All sub-agents use free models (groq-llama → cerebras-llama → nim-llama → or-scout).
Never spawn on premium models unless explicitly requested.

## Task Template
```
You are a [ROLE]. Your job: [ONE SENTENCE].
Files you need: [LIST PATHS]
Exit criteria: [ARTIFACT]
If stuck after 2 attempts, STOP and report what failed.
```

## After Completion
- Verify output file exists. If missing, retry inline or on fallback.
- Read only output files — never load sub-agent transcripts into context.

## Rules
- 1 sub-agent at a time.
- Don't poll in a loop — they auto-announce.
- Don't retry on the same model that just 429'd.
