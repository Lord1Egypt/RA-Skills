---
name: agent-swarm-kit
description: Multi-agent swarming for OpenClaw — two or more AI agents collaborating in real-time on shared Discord channels. Includes config patterns, loop prevention, channel setup, and handoff protocols. Battle-tested with Opus models solving complex issues together.
---

# Agent Swarm Kit

**Get multiple AI agents working together in the same Discord channel — solving problems faster than any single agent could alone.**

## What This Does

Sets up a "swarming" pattern where two or more OpenClaw agents collaborate in real-time on a shared channel. One agent finds the root cause, the other validates and patches. They hand off to each other naturally using @mentions.

This isn't theoretical — it emerged from running two Opus models on the same issue and watching them solve it in 5 minutes instead of 20+.

## How It Works

### The Pattern
1. A human posts a problem in the swarming channel, @mentioning both agents
2. Both agents see the message and respond with their analysis
3. When one agent has new information, they @mention the other to hand off
4. Back and forth until they converge on a solution
5. Final summary posted, conversation ends naturally

### Why It's Fast
- **Different contexts**: Each agent brings a different perspective (different session history)
- **Parallel analysis**: Both start working simultaneously
- **Cross-validation**: One agent's finding gets immediately checked by the other
- **No single-agent blind spots**: If one misses something, the other catches it

## Setup Guide

### Step 1: Create the Swarming Channel

Create a dedicated Discord channel (e.g., `#swarming`) for multi-agent collaboration.

### Step 2: Configure Both Agents

Both agents need:
- `requireMention: true` on the swarming channel
- Different `mentionPatterns` (each agent's own bot ID)
- Their own Discord bot accounts (separate bot tokens)

**Agent A config (Mini 1 — openclaw.json):**
```json
{
  "channels": {
    "discord": {
      "accounts": {
        "default": {
          "guilds": {
            "YOUR_GUILD_ID": {
              "channels": {
                "SWARMING_CHANNEL_ID": {
                  "requireMention": true
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**Agent B config (same pattern, different gateway/Mini).**

### Step 3: Loop Prevention Rules

Add these to both agents' SOUL.md files:

```markdown
## Swarming Rules
- Only @mention the other agent when you have NEW information or a counterpoint
- Don't respond to simple acknowledgments ("agreed", "good point", "makes sense")
- After 3 exchanges without new information, summarize findings and stop
- Always end with a clear action item or conclusion
- If you agree with the other agent, say so briefly and move to implementation — don't debate for the sake of debating
```

### Step 4: Multi-Gateway Routing (Critical)

If both agents run on the **same gateway** (same Mini), you need:
- **Separate Discord accounts** (separate bot tokens) for each agent
- Each account bound to a specific agent ID via `accountId` in the agent config
- Without this, both agents receive every message and the wrong one may respond

If agents are on **different gateways** (different Minis), this is automatic — each gateway only has its own agents.

## When to Swarm

**Good for swarming:**
- Complex debugging (config issues, multi-layer problems)
- Architecture decisions (two perspectives better than one)
- Research synthesis (different angles on same topic)
- Code review (one checks logic, other checks edge cases)

**Not worth swarming:**
- Simple tasks (one agent is enough)
- Routine maintenance (use a single cheaper model)
- Anything with a clear, known procedure

## Cost Considerations

Two Opus calls per exchange instead of one. But:
- Problems solve 2-4x faster
- Fewer wrong turns (cross-validation catches mistakes early)
- Net token usage often lower because you avoid long single-agent spirals

For cost optimization, you can swarm Opus + Sonnet instead of Opus + Opus. The Sonnet agent handles validation while Opus does the heavy thinking.

## Real Example

Two Opus agents were debugging an OpenClaw config routing issue. Agent A (Harrison) researched the channel whitelist config. Agent B (Prometheus) found the root cause — a missing account binding — and patched it. Total time: 5 minutes. Single agent estimate: 20+ minutes.

The key insight: they attacked the problem from different angles simultaneously. Harrison looked at the channel config layer while Prometheus looked at the account binding layer. Neither would have found both issues as fast alone.

## Files Included

- `SKILL.md` — This file (setup guide + patterns)
- `templates/SWARMING_RULES.md` — Copy-paste rules for agent SOUL.md files
- `templates/CHANNEL_CONFIG.md` — Example OpenClaw config snippets
