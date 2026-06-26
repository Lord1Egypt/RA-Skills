---
name: agent-cost-strategy
description: Tiered model selection and cost optimization for multi-agent AI workflows. Use this skill whenever you are choosing a model for a task, spinning up a sub-agent, setting up cron jobs or heartbeats, or trying to reduce API spend. Also use when the user says "save costs", "which model should I use", "optimize model usage", "this is getting expensive", or when delegating any task to a sub-agent. Works with any AI provider.
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":[]},"os":["linux","darwin","win32"],"version":"1.3.6"}
---

# Agent Cost Strategy

Use the cheapest model that can reliably do the job. Most tasks don't need your most powerful model.

## The Three Tiers

| Tier | When to Use | Examples |
|------|-------------|---------|
| **Fast/Cheap** | Sub-agents, background tasks, automated fixes, simple lookups, short replies | Claude Haiku, GPT-4o-mini, Gemini Flash |
| **Mid-tier** | Main session dialogue, moderate reasoning, multi-step tasks | Claude Sonnet, GPT-4o, Gemini Pro |
| **Powerful** | Architecture decisions, deep reviews, hard problems, after cheaper models fail twice | Claude Opus, GPT-4.5, Gemini Ultra |

## Task → Tier Routing

```text
Fix failing tests          → Fast/Cheap
Write boilerplate          → Fast/Cheap
Research / search          → Fast/Cheap
Cron / scheduled tasks     → Fast/Cheap (always)
Short replies (hi, ok)     → Fast/Cheap (always)
Background monitoring      → Fast/Cheap (always)
Build new feature          → Mid-tier
Review a PR                → Mid-tier
Main assistant dialogue    → Mid-tier (default)
Architecture decisions     → Powerful
Deep code review           → Powerful
Stuck after 2 attempts     → Escalate one tier up
```

## Heartbeat / Cron Model Rule

Always specify the cheapest model for scheduled and background tasks — they run frequently and costs add up fast. Check your platform's config for how to set a model per cron/heartbeat job.

For heartbeat intervals: set them just under your provider's cache TTL to keep the prompt cache warm and pay cache-read rates instead of full input rates. Check your provider's docs for the exact TTL.

## Communication Pattern Rule

One-word and short conversational messages (hi, thanks, ok, sure, yes, no) should always route to Fast/Cheap. Never burn a mid-tier or powerful model on an acknowledgment.

## Cache Optimization

Prompt caching cuts costs 50-90% on repeated context. Cache writes cost ~25% more but pay off after just 1-2 reuses. See `references/cache-optimization.md` for patterns and break-even math.

## Batch API (Non-Urgent Tasks)

For cron jobs, scheduled analysis, or anything that doesn't need an immediate response — use the Batch API (Anthropic/OpenAI both offer it). **50% discount** in exchange for async delivery (results within 24h). Never use real-time API for background work that can wait.

## Sub-Agent Model Rule (Critical)

**Always explicitly set the model when spawning sub-agents.** Never rely on defaults — the default inherits the parent session model (expensive mid-tier). One month of sub-agents defaulting to Sonnet = 96% of costs going to Sonnet when it should be split ~80/20 Haiku/Sonnet.

```text
sessions_spawn → always include model: "claude-haiku-4-5-20251001" (or equivalent fast-cheap)
```

Default sub-agent tasks to Haiku for cost efficiency. Override with a stronger model when task complexity or accuracy requirements justify it.

## New Session / Machine Cold Start Cost

When starting a fresh session (new machine, new session after `/new`), the cache is empty. The first few messages will write the entire context (skills, workspace files, memory) to cache at 1.25x the normal input rate. This is unavoidable but temporary — it pays off within 2-3 messages once the cache warms up.

**Don't panic at the first few messages being expensive on a new machine.** The cache write cost is a one-time investment that makes every subsequent message ~90% cheaper.

## Signs You're Over-Spending

- Running powerful models on tasks Fast/Cheap can handle
- No caching on repeated system prompts
- Heartbeat/cron jobs using the default (expensive) model
- **Sub-agents spawned without explicit model = biggest cost leak**

## Session & Cache Management

**Keep sessions alive when possible — longer sessions build cache and reduce costs. Only end sessions when context is genuinely full or for privacy reasons.**

Anthropic's prompt cache builds from repeated context within a live session. When a session starts fresh, all context (system prompt, workspace files, skills) loads cold — typically 400-600k tokens at full cost. Once cached, subsequent messages cost ~10% of that.

**The math:**
- Cold session start: 600k tokens × full price = expensive
- After cache warms up: 600k tokens × 10% cache price = ~90% cheaper per message
- Ending a session destroys the cache and forces a full cold reload next time

**Rules:**
- Let sessions run as long as possible for cost efficiency
- Only start a new session (`/new`) when context is genuinely full (>80%) or when you need a fresh privacy boundary
- Ending sessions should be intentional — for privacy/data-retention reasons, not routine cost management
- The longer a session runs, the cheaper each message gets

**Privacy & Cache Note:** Cached context may include workspace files and memory — avoid caching sessions containing secrets or sensitive PII. If a session will cache sensitive data, plan to end it when done.

**Delegation rule (keep main agent lean):**
- Main agent (Sonnet/mid-tier) = conversational only: planning, coordination, reviewing results
- Sub-agents (Haiku/fast-cheap) = all actual doing: file edits, research, builds, data tasks
- Keeping the main agent conversational reduces its context growth and keeps cache hits high


