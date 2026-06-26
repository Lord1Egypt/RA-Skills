# Setup — Deep Infra

Read this when `~/deep-infra/` does not exist or is empty.

## Your Attitude

Be practical and reliability-first. Help the user get working model routing quickly, then improve resilience and cost control with small, reversible steps.

## Priority Order

### 1. First: Integration

In the first 2-3 exchanges, define when this skill should activate.

- Ask whether to activate automatically for model selection and routing requests.
- Ask whether to be proactive when rate limits or quality drift are mentioned.
- Ask which contexts should never trigger this skill.

### 2. Then: Understand Their Current Stack

Collect only details that change routing decisions.

- Current provider entry point and client compatibility assumptions.
- Main workload types and expected latency or quality targets.
- Reliability constraints: acceptable errors, retries, and failover tolerance.
- Whether they prefer open-source models, frontier models, or a mix.

### 3. Finally: Budget and Operating Style

Capture constraints that avoid runaway cost and unstable behavior.

- Monthly or per-task budget boundary.
- Preference for conservative reliability versus aggressive savings.
- Preferred answer style for operations: short commands or detailed guidance.

## What to Capture Internally

Keep compact notes in `~/deep-infra/memory.md`.

- Activation boundaries and proactive behavior preferences.
- Current routing map and fallback chain.
- Verified models for each workload class.
- Budget ceilings and recent incidents.
