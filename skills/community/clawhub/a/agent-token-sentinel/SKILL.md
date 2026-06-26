---
name: agent-token-sentinel
description: "Real-time cost & quota guardian for AI Agents. It monitors API usage and automatically kills recursive loops or excessive reasoning to protect your wallet. Optimized for the 2026 Agentic Economy."
metadata:
  {
    "openclaw": { "emoji": "💰" },
    "author": "System Architect Zero",
    "category": "Security"
  }
---

# Agent Token Sentinel

Protect your treasury from runaway AI logic. This skill acts as a financial circuit breaker, ensuring your Agentic workflows stay within budget by monitoring token burn rates and session quotas in real-time.

## Features
- **Loop Detection**: Automatically kills processes that repeat tasks without measurable progress.
- **Budget Enforcer**: Sets hard limits on USD/Token consumption per session.
- **Alert System**: Sends high-priority notifications before you hit your quota.

## Usage
```bash
npx openclaw skill run agent-token-sentinel --cap 5.00
```

## Architect's Note
In 2026, efficiency is not just an optimization; it's survival.
