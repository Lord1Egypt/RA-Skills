# ARTA — Agentic Real-Time Awareness

**⚠️ Advanced Setup Required**

This skill requires extra configuration and is not beginner-friendly. You'll need to:
- Configure your agent identity
- Set up channel detection (Telegram, Discord, Slack, etc.)
- Optionally install an OpenClaw hook for automatic capture

See SKILL.md for full configuration instructions.

---

## What

ARTA lets an agent know what it's doing in other channels in real-time.

Without ARTA:
- Fragmented agent across channels
- Can't answer: "What am I doing elsewhere?"

With ARTA:
- Unified awareness
- Real-time answers

## Core Protocol

- **Register** → On session start
- **Update** → On activity
- **Query** → "What am I doing elsewhere?"
- **Leave** → On session end

## Simple Implementation

Just an in-memory class. No database, no external services.

```javascript
const arta = new ARTA('my-agent');
arta.register({ instanceId, channel, human, task });
arta.update({ instanceId, task });
const others = arta.queryOtherThan(sessionId);
```

## The Awareness Test

**Goal:** Agent knows what it's doing in other channels, without memory files.

**After ARTA:**
```
User: What are you discussing in other channels?
Agent: Let me check... I'm reviewing code in the development channel.
```

## Files

- SKILL.md — Full framework with configuration instructions
- POLICY.md — Quick reference
- TEMPLATE.md — Drop-in code

## Install

```bash
clawhub install arta
```

## Recommended: Also Install IBT

For best results, pair ARTA with **IBT** (Instinct + Behavior + Trust):

```bash
clawhub install ibt
```

IBT provides execution discipline while ARTA provides awareness. Together they give your agent both judgment and self-knowledge.

## Why Separate from IBT?

- Different problem (awareness vs execution)
- Evolves independently
- Works with any agent
