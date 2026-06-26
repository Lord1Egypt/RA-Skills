---
name: Agentic Engineering
slug: agentic-engineering
version: 1.0.0
homepage: https://clawic.com/skills/agentic-engineering
description: Work effectively with AI coding agents using parallel terminals, blast radius thinking, atomic commits, and pragmatic tool selection.
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---

## When to Use

User works with AI coding agents (Claude Code, Codex CLI, or similar) and wants to maximize productivity. Use for workflow optimization, parallel agent coordination, context management, and developing intuition for agentic development.

## Quick Reference

| Topic | File |
|-------|------|
| Parallel workflow | `parallel.md` |
| Blast radius | `blast-radius.md` |
| Context & prompts | `context.md` |
| Tool selection | `tools.md` |

## Core Philosophy

Agentic engineering is about **working WITH AI coding agents effectively**, not building agent systems. The term was popularized by Peter Steinberger (steipete.me) in late 2025.

Core principle: **Just talk to it.** Skip the elaborate tooling, RAG setups, and complex orchestration. Develop intuition through practice.

## Core Rules

### 1. Run Parallel Agents
Run 3-8 coding agent instances simultaneously in a terminal grid:
```
┌─────────┬─────────┬─────────┐
│ Agent 1 │ Agent 2 │ Agent 3 │
│ (main)  │ (refac) │ (tests) │
├─────────┼─────────┼─────────┤
│ Agent 4 │ Agent 5 │ Agent 6 │
│ (ui)    │ (docs)  │ (debug) │
└─────────┴─────────┴─────────┘
```
Most agents work in the same folder. No worktrees. Pick non-overlapping areas.

### 2. Think in Blast Radius
Before each prompt, estimate:
- How many files will this touch?
- How long will this take?
- Can I run this in parallel with other work?

Small blast radius → multiple parallel agents.
Large blast radius → one focused agent.

### 3. Agents Do Atomic Commits
Configure agents to commit their own changes:
- One commit per logical change
- Only commit files the agent edited
- Clean commit messages

This keeps history navigable when multiple agents work simultaneously.

### 4. Refactor Regularly
Spend ~20% of time on refactoring (also done by agents):
- Code duplication (jscpd)
- Dead code (knip)
- Consolidate similar patterns
- Break apart large files
- Add tests for tricky parts

Iterate fast, then pay back tech debt.

### 5. CLIs Over MCPs
Prefer CLIs that agents already know:
```
✅ gh, vercel, psql, axiom
❌ Complex MCPs that pollute context
```
One line in AGENTS.md: "logs: use vercel cli" is enough.

### 6. Screenshots in Prompts
50%+ of prompts should include screenshots:
- Drag image into terminal
- Agent finds matching strings/elements
- Far more precise than text descriptions

No need to annotate — agents are good at matching.

### 7. Stop and Steer
If something takes longer than expected:
1. Press Escape
2. Ask "what's the status"
3. Help find the right direction, abort, or continue

Don't be afraid to stop agents mid-work. File changes are atomic.

## Common Traps

- **Over-engineering setup** → Skip RAG, complex subagents, plugins. Just talk to it.
- **One agent at a time** → Run parallel, pick non-overlapping areas.
- **Elaborate prompts** → Short prompts + screenshot often work better.
- **Worktrees/branches per change** → Slows you down. Same folder, atomic commits.
- **Background agents only** → Hard to steer. Keep agents visible.

## Scope

This skill ONLY:
- Provides workflow patterns for using AI coding agents
- Guides tool and setup decisions
- Shares best practices from the agentic engineering community

This skill NEVER:
- Implements agents directly
- Accesses external systems
- Modifies files outside skill documentation

## Security & Privacy

**Data that leaves your machine:**
- None — this skill provides guidance only

**Data that stays local:**
- No persistent storage required

**This skill does NOT:**
- Access credentials or make network requests
- Execute code autonomously
