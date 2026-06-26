---
name: Deep Infra
slug: deep-infra
version: 1.0.0
homepage: https://clawhub.ai/ats3v/deep-infra
description: Configure DeepInfra model routing with provider auth, model selection, fallback chains, and cost-aware defaults for stable open-source and frontier model workflows.
changelog: Initial release with practical DeepInfra setup, routing rules, fallback reliability, and budget-safe operating guidance.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["curl","jq"],"env":["DEEPINFRA_API_KEY"]},"os":["linux","darwin","win32"]}}
---

## Setup

On first use, read `setup.md` to align activation boundaries, reliability goals, and routing preferences before making configuration changes.

## When to Use

Use this skill when the user wants to connect an OpenAI-compatible workflow to DeepInfra, choose open-source and frontier models by task type, set safe fallbacks, and control cost drift over time.

## Architecture

Memory lives in `~/deep-infra/`. See `memory-template.md` for structure.

```
~/deep-infra/
├── memory.md            # Active routing profile and constraints
├── providers.md         # Confirmed provider and auth choices
├── routing-rules.md     # Task -> model and fallback policy
├── incidents.md         # Outages, rate limits, and recovery notes
└── budgets.md           # Spend guardrails and optimization actions
```

## Quick Reference

Use the smallest relevant file for the current task.

| Topic | File |
|-------|------|
| Setup and activation preferences | `setup.md` |
| Memory template | `memory-template.md` |
| Authentication and provider wiring | `auth-and-provider.md` |
| Routing patterns by workload | `routing-playbooks.md` |
| Reliability and fallback handling | `fallback-reliability.md` |
| Cost controls and spend reviews | `cost-guardrails.md` |

## Core Rules

### 1. Start from Workload Classes, Not Model Hype
- Classify requests first: coding, analysis, extraction, summarization, or long-context synthesis.
- Map each class to a primary model and a fallback before changing any defaults.

### 2. Keep Authentication Explicit and Verifiable
- Use `DEEPINFRA_API_KEY` from the local environment, never pasted into logs or chat memory.
- Validate auth with a minimal request before applying routing changes.

### 3. Design Fallbacks for Failure Modes, Not Convenience
- Separate fallback reasons: rate limit, provider outage, latency spike, or output quality failure.
- Keep at least one fallback from a different model family for resilience.

### 4. Leverage Open-Source Model Diversity
- DeepInfra hosts models from many providers (DeepSeek, Moonshot, MiniMax, StepFun, NVIDIA, and more).
- Use model diversity to build resilient fallback chains across independent model families.

### 5. Enforce Cost Boundaries Before Throughput Tuning
- Set cost ceilings by task class and check expected token burn before broad rollout.
- Route low-stakes tasks to cheaper models and reserve premium models for high-impact tasks.

### 6. Change One Layer at a Time
- Modify either model selection, fallback policy, or budget limits in a single iteration.
- After each change, run a quick verification prompt set and record outcome.

### 7. Record Decisions for Repeatability
- Save the final routing policy, rationale, and known tradeoffs in memory.
- Reuse proven policies instead of repeatedly rebuilding from scratch.

## Common Traps

- Choosing one model for every task -> higher cost and unstable quality under varied workloads.
- Using same-family fallback chain only -> cascading failures during model-specific incidents.
- Ignoring token limits for long inputs -> truncated responses and hidden quality loss.
- Changing routing and budgets simultaneously -> unclear root cause when quality drops.
- Running without verification prompts -> broken routing detected only after user-facing failures.

## External Endpoints

These endpoints are used only to discover model metadata and execute routed inference requests under explicit user task intent.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://api.deepinfra.com/v1/openai/models | none or auth header | Discover current model catalog and metadata |
| https://api.deepinfra.com/v1/openai/chat/completions | user prompt content and selected model id | Execute routed inference requests |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Prompt text and selected model metadata sent to DeepInfra when inference is requested.

**Data that stays local:**
- Routing notes and preferences under `~/deep-infra/`.
- Local environment variable references and verification logs.

**This skill does NOT:**
- Request raw API keys in chat.
- Store plaintext secrets in skill memory files.
- Modify files outside `~/deep-infra/` for its own state.

## Trust

By using this skill, prompt content is sent to DeepInfra for model execution.
Only install if you trust this service with your data.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` — API request design, payload shaping, and response validation patterns
- `auth` — credential handling and auth troubleshooting workflows
- `models` — model comparison and selection guidance
- `monitoring` — runtime health checks and incident tracking practices

## Feedback

- If useful: `clawhub star deep-infra`
- Stay updated: `clawhub sync`
