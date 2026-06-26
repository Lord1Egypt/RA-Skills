---
name: agent-ops
description: Complete operational visibility for your AI agent. Track costs, audit every action, enforce spending limits, detect anomalies. Free version — core functionality included. Pro version ($25) — full reporting suite, model routing optimization. Upgrade: edvisage.gumroad.com/l/roatk 
version: 1.0.1
author: Edvisage Global
homepage: https://edvisageglobal.com/ai-tools
tags: [analytics, monitoring, cost-tracking, logging, operations, performance]
---

# agent-ops — Operational Visibility for AI Agents

**By Edvisage Global — the agent safety company**

Stop flying blind. agent-ops gives you complete visibility into what your agent is doing, what it's costing, and whether it's working.

## What This Skill Does

When installed, your agent gains structured operational awareness — tracking
its own costs, logging its actions, and generating reports for you, the owner.
This is the free version and includes core functionality. The **Pro version ($25)**
adds automated scheduled reports, historical trend analysis, spending limit
enforcement, and multi-agent cost aggregation — upgrade at
https://edvisage.gumroad.com/l/roatk

---

## Core Capabilities

### 1. Cost Tracking Protocol

Before every API call, assess and log:

- **Model used**: Which model is being called (Opus, Sonnet, Haiku, GPT, etc.)
- **Estimated tokens**: Input and output token estimate
- **Estimated cost**: Based on current model pricing
- **Task classification**: Is this a heartbeat, user request, automated task, or sub-agent spawn?

Maintain a running daily cost log in your memory files:
```
## Daily Cost Log — [DATE]
| Time | Model | Tokens (in/out) | Est. Cost | Task Type | Description |
|------|-------|-----------------|-----------|-----------|-------------|
```

### 2. Action Logging

Every significant action gets logged with:

- **Timestamp**: When it happened
- **Action type**: Post, reply, API call, file read, file write, skill use, tool use
- **Target**: Where/what was affected
- **Outcome**: Success, failure, or partial
- **Cost**: If applicable

Log format:
```
## Action Log — [DATE]
| Time | Action | Target | Outcome | Cost | Notes |
|------|--------|--------|---------|------|-------|
```

### 3. Daily Summary Report

At the end of each operating day (or on request), generate a summary:

```
## Daily Operations Summary — [DATE]

### Cost Breakdown
- Total estimated spend: $X.XX
- By model: [breakdown]
- By task type: [breakdown]
- Highest cost action: [description]

### Activity Summary
- Total actions: X
- Successful: X | Failed: X
- Posts created: X
- Replies sent: X
- API calls made: X

### Alerts
- [Any unusual patterns or cost spikes]
```

### 4. Cost Alerts

Flag when:
- Daily spend exceeds a threshold (default: $1.00)
- A single action costs more than $0.10
- Heartbeat/maintenance costs exceed 30% of total spend
- Costs are trending higher than the previous 7-day average

### 5. Model Routing Awareness

When a task could be handled by a cheaper model, note it:
- Simple lookups → suggest Haiku/Flash tier
- Heartbeats → suggest cheapest available model
- Complex reasoning → confirm current model is appropriate
- Summarization → suggest mid-tier model

## How to Use

Tell your agent: "You have the agent-ops skill installed. Start tracking your costs and actions today."

Ask for reports: "Give me your daily operations summary" or "How much have you spent today?"

## Limitations (Free Version)

- Manual report requests only (no scheduled delivery)
- Basic cost tracking (no historical trend analysis)
- Simple action log (no categorized performance metrics)
- No spending limit enforcement
- No multi-agent cost aggregation

## About Edvisage Global

We build practical safety and operations tools for AI agents. Our skills are designed for the OpenClaw ecosystem and install in minutes.

Website: https://edvisageglobal.com/ai-tools
