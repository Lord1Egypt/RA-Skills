---
name: battle-tested-agent
version: 1.5.0
description: >
 19 production-hardened patterns for AI agents — memory, verification, ambiguity
 handling, compaction survival, delegation, proof-based handoffs, stale-worker recovery,
 and self-improvement. Use when hardening an agent for production reliability, when an
 agent keeps hallucinating or losing context, when handoffs between agents drop details,
 when delegated work silently fails, or when someone says "my agent is unreliable" or
 "how do I make this more robust." Works with OpenClaw, Claude Code, Cowork, or any
 SKILL.md-based agent setup. Includes the Isolated Agent Fabrication Guard plus new
 delegation hardening patterns for brief quality, completion contracts, acceptance gates,
 silent-worker recovery, and scoped verifier use.
author: Zye ⚡ (Don Zurbrick)
license: MIT
tags: [production, reliability, memory, compaction, multi-agent, security, self-improvement, heartbeat, delegation, battle-tested]
homepage: https://github.com/zurbrick/battle-tested-agent
metadata:
  openclaw:
    emoji: "⚔️"
    requires:
      bins: ["bash", "grep", "find", "wc"]
      optionalBins: ["openclaw"]
---

# Battle-Tested Agent

**19 production-hardened patterns for AI agents. Every one earned from failure.**

Use this skill when you are:
- hardening an agent that will run repeatedly or autonomously
- tightening memory, verification, or anti-hallucination behavior
- reducing compaction failures, weak handoffs, or orchestration drift
- reviewing an agent workspace for missing production patterns
- debugging why an agent keeps losing context, guessing, or dropping work

Do not use this skill for:
- persona writing or onboarding polish
- one-off prompt tweaks with no reusable pattern behind them
- adding new tools, servers, or runtime capabilities
- turning a simple workspace into process theater

## Default workflow

1. **Audit first**
   Run `bash scripts/audit.sh <workspace>` to see which patterns are present.
   The script checks for all 16 patterns and tells you what to fix first.

2. **Start with the smallest tier that fits**
   Implement starter patterns first, then intermediate, then advanced.
   Do not cargo-cult every pattern into every agent.

3. **Patch the actual failure mode**
   Change the mechanism, not just the wording. "ALWAYS check X" is not a fix —
   a verification gate is a fix.

4. **Keep patterns lightweight**
   Add only the pieces that materially reduce failures or operator burden.

## Pattern tiers

- **Starter (5):** baseline reliability for almost every agent
- **Intermediate (5):** daily-driver patterns for briefs, heartbeats, and recurring work
- **Advanced (6):** multi-agent orchestration, handoffs, and self-improvement discipline

### Pattern clusters

Some patterns reinforce each other naturally. Adopt them together when the failure
mode calls for it:

- **Trust chain:** WAL Protocol + Anti-Hallucination + Agent Verification — ensures
  data is captured, sourced, and measured before reporting
- **Handoff loop:** Delegation Rules + Completion Contract + Acceptance Gate + Task State Tracking — prevents
  work from disappearing between agents or being certified without proof
- **Survival kit:** Working Buffer + Compaction Injection Hardening + Silent Worker Recovery — keeps context
  alive across long sessions and prevents silent delegated drift
- **Quality gate:** QA Gates + Verify Implementation + Decision Logs — ensures output
  quality and traceable reasoning
- **Delegation hardening:** Brief Quality Gate + Scoped Verifier Gate — keeps delegation tight without turning the whole system into bureaucracy

### When patterns conflict

If two patterns seem to give contradictory advice:
- **Safety patterns win over speed patterns.** Ambiguity Gate overrides Simple Path First
  when the request is ambiguous. Verify before acting, even if the simple path is obvious.
- **Evidence patterns win over action patterns.** Anti-Hallucination overrides "just try it"
  when reporting data. Never guess a number to move faster.

## Assets — how to use them

The `assets/` folder contains starter files you copy into your workspace and customize.
They are templates, not drop-in replacements.

```bash
# Merge delegation and decision log rules into your existing AGENTS.md
cp assets/AGENTS-additions.md ~/workspace/ # Review, then merge

# Add QA gates
cp assets/QA-gates.md ~/workspace/QA.md

# Set up self-improvement tracking
mkdir -p ~/workspace/.learnings
cp assets/learnings-template.md ~/workspace/.learnings/LEARNINGS.md
cp assets/errors-template.md ~/workspace/.learnings/ERRORS.md
cp assets/features-template.md ~/workspace/.learnings/FEATURE_REQUESTS.md
```

Read `references/audit-usage.md` for the full rollout order and bootstrap workflow.

## References

- `references/starter-patterns.md` — WAL, anti-hallucination, ambiguity, simple-path-first, unblock-before-shelve
- `references/intermediate-patterns.md` — verification, working buffer, QA gates, decision logs, verify implementation
- `references/advanced-patterns.md` — delegation, brief quality, proof-based handoffs, acceptance gates, orchestration, stale-worker recovery, compaction hardening, recurrence tracking
- `references/audit-usage.md` — audit script usage, install/copy snippets, and expected outcomes

## Included scripts

- `scripts/audit.sh` — workspace audit for all 19 patterns (supports AGENTS.md, CLAUDE.md, SOUL.md, and system.md)

## Rules of thumb

- Audit before expanding
- Prefer progressive disclosure over giant core files
- Silence is better than hallucination
- Ambiguity is a stop sign, not permission
- The orchestrator should preserve oversight, not sink into implementation
- Mechanism changes beat wording changes
- After acting, verify the new state before declaring success
- Partial progress is not success; recovery steps matter as much as first-attempt steps

## Outcome

A leaner, more resilient agent that survives compaction, hands work off cleanly,
reports only what is verified, and improves without spiraling into bureaucracy.
