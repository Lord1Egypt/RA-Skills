---
name: council-of-llms
description: "Real multi-model council deliberation for OpenClaw subagents. Spawns 3 parallel subagents with different LLMs and distinct analytical perspectives (Strategy, Analysis, Creativity), then synthesizes their independent outputs into a unified verdict with consensus points, disagreements, and action items. Fixes the single-model roleplay anti-pattern that causes context overflow and shallow analysis. Requires the subagent-orchestration skill for base spawning patterns. Triggers on: council, deliberate, debate, review, stress-test, multi-model, decision, verdict, analysis, perspectives."
tags:
  - council
  - multi-model
  - deliberation
  - analysis
  - decision-making
  - subagent
  - orchestration
  - llm
  - review
  - stress-test
---

# Council of LLMs

## Overview

A real council spawns **3 parallel subagents**, each with a different model and perspective, then synthesizes their outputs into a unified verdict. This is NOT one model roleplaying 3 experts — it's genuinely different models providing independent analysis.

## Models

Configure your council models in `~/.openclaw/council-config.json`:

```json
{
  "council_models": [
    "your-strategic-model",
    "your-analytical-model",
    "your-creative-model"
  ],
  "default_timeout": 900,
  "max_tokens": 8192
}
```

**Choose models with different strengths:**
- **Strategos (Strategic):** Pick a model known for strategic thinking, long-context reasoning, and business insight
- **Analyticos (Analytical):** Pick a model known for data analysis, technical precision, and logical reasoning
- **Creativos (Creative):** Pick a model known for creative thinking, novel perspectives, and user empathy

The more diverse the models, the better the council output. Using the same model for all three defeats the purpose.

**Example configuration:**
```json
{
  "council_models": [
    "ollama/kimi-k2.6:cloud",
    "ollama/deepseek-v4-pro:cloud",
    "ollama/gemma4:31b-cloud"
  ],
  "default_timeout": 900,
  "max_tokens": 8192
}
```

## Perspectives

Each model gets a different analytical lens:

| Perspective | Role | Focus |
|------------|------|-------|
| **Strategos** | Strategic analyst | Big-picture strategy, business impact, feasibility, ROI |
| **Analyticos** | Data & logic analyst | Technical correctness, edge cases, data quality, consistency |
| **Creativos** | Creative thinker | Novel alternatives, user experience, unconventional approaches |

## How to Run a Council

### Step 1: Prepare the Context

Gather all relevant data BEFORE spawning. Council agents cannot browse the web or access your conversation history. Paste everything they need inline.

### Step 2: Spawn 3 Parallel Subagents

Read the model names from `council-config.json` and spawn each with a different perspective:

```
sessions_spawn(
  runtime: "subagent",
  mode: "run",
  model: <first model from config>,
  label: "Council-Strategos",
  lightContext: true,
  runTimeoutSeconds: <default_timeout from config>,
  task: "You are Strategos, a strategic analyst. [PASTE CONTEXT HERE]

  Analyze from a STRATEGIC perspective:
  - Business impact and feasibility
  - Resource requirements and ROI
  - Strategic risks and opportunities

  Return your analysis as a structured review with: verdict, conditions, risks, recommendations."
)

sessions_spawn(
  runtime: "subagent",
  mode: "run",
  model: <second model from config>,
  label: "Council-Analyticos",
  lightContext: true,
  runTimeoutSeconds: <default_timeout from config>,
  task: "You are Analyticos, a data and logic analyst. [PASTE CONTEXT HERE]

  Analyze from an ANALYTICAL perspective:
  - Data quality and completeness
  - Technical correctness and edge cases
  - Logical consistency

  Return your analysis as a structured review with: verdict, conditions, risks, recommendations."
)

sessions_spawn(
  runtime: "subagent",
  mode: "run",
  model: <third model from config>,
  label: "Council-Creativos",
  lightContext: true,
  runTimeoutSeconds: <default_timeout from config>,
  task: "You are Creativos, a creative thinker. [PASTE CONTEXT HERE]

  Analyze from a CREATIVE perspective:
  - Novel alternatives and unconventional approaches
  - User experience and usability
  - What's missing that no one else would think of

  Return your analysis as a structured review with: verdict, conditions, risks, recommendations."
)
```

### Step 3: Synthesize

When all 3 return, merge their verdicts:

1. **Consensus points** — where all 3 agree
2. **Disagreements** — where they differ and why
3. **Blind spots** — what none of them caught
4. **Final verdict** — weighted synthesis with conditions
5. **Action items** — concrete next steps

Write the synthesis to `council-review-[topic].md`.

## Critical Rules

1. **Paste ALL context inline** — agents have no conversation history
2. **Keep task descriptions under 2000 words** — longer = context overflow = failure
3. **Use `lightContext: true`** — always, to prevent context bloat
4. **Set `runTimeoutSeconds` from config** — default 900, increase for complex topics
5. **Don't spawn with too much data** — if pasting 10k+ words, summarize first
6. **Wait for ALL 3 to complete** — don't synthesize with 2/3 results
7. **Never re-spawn** — if one model times out, note it in the synthesis

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| All 3 return empty | Gateway overload | Kill zombie subagents, wait, retry |
| One model times out | Slow model + complex task | Increase timeout or simplify task |
| Context overflow (300k+ tokens) | Too much data pasted | Summarize to <2000 words |
| Shallow analysis | Vague task description | Be specific about what to analyze |
| All 3 say the same thing | Not enough perspective differentiation | Make perspective prompts more distinct |

## Security & Safety

This skill is **read-only and sandbox-safe**:
- Spawns 3 text-in/text-out subagents via `sessions_spawn` — no filesystem access, no arbitrary commands, no network calls
- Subagents receive a text prompt and return a text analysis — that's it
- No `exec`, no shell commands, no file reads/writes, no API calls
- Models are configured locally — you control which models run
- All output is a markdown synthesis file written to your workspace

## Anti-Patterns

- Spawning one subagent and asking it to "be 3 experts" — that's roleplay, not a council
- Pasting 10k+ words of raw data — summarize first
- Using the same model for all 3 perspectives — defeats the purpose
- Synthesizing before all 3 complete — wait for everyone
- Ignoring disagreements — disagreements are the most valuable output