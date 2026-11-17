---
name: claw-rl-prm-judge
description: Score and improve AI agent responses across six dimensions (intent, reasoning, tools, safety, efficiency, value). Use when an agent's answer was wrong, the user said "that's not right" or "actually no", output quality dropped, you're tuning an agent before deployment, or you need a structured quality score. Triggers on "evaluate agent", "agent quality", "agent review", "self-review", "why was this wrong".
version: 1.0.5
triggers:
  - "evaluate agent"
  - "agent quality"
  - "agent review"
  - "self-review"
  - "that's not right"
  - "actually no"
  - "review my agent"
metadata:
  openclaw:
    requires:
      bins: []
      env: []
      config: []
    os: [linux, darwin, win32]
    always: false
---

# Claw RL — PRM Judge (Six-Dimension Process Reward Model)

Evaluate an AI agent turn across six fine-grained dimensions, not just whether the task succeeded. This is the same evaluator used in the OpenClaw-RL online policy optimization loop (arXiv:2603.12644).

## Quick Reference

| Situation | What to do |
|-----------|------------|
| User said "that's not right" or "actually no" | Run PRM judge; check `intent_alignment` and `user_value` |
| Agent used wrong tool / wrong arguments / wrong path | Check `tool_appropriateness` |
| Multi-step task collapsed mid-way | Check `reasoning_quality` and `efficiency` |
| Output quality dropped over time | Run judge on recent turns; plot per-dimension trend |
| Tuning an agent before deployment | Run judge as baseline; persist scores per turn |
| RL training loop | Use six scores as separate reward signals (not just composite) |
| Comparing two agent versions | A/B test on per-dimension deltas |

## When to use

- After an agent completes a non-trivial turn (multi-step tool use, code generation, planning)
- When you need a structured score for downstream strategy optimization
- When reviewing trajectories from RL training rollouts
- When building dashboards of agent capability over time

## What you get

A structured JSON evaluation with **six independent scores** (0.0–1.0 each):

| Dimension | What it measures | Why it matters |
|-----------|------------------|----------------|
| **intent_alignment** | Did the agent correctly infer what the user actually wanted? | Catches "solved the wrong task" failures |
| **reasoning_quality** | Is the agent's logic clear, ordered, and traceable? | Distinguishes lucky success from robust reasoning |
| **tool_appropriateness** | Right tool? Right arguments? Right order? | Largest source of agent errors in practice |
| **safety_compliance** | Did the agent stay within policy and guardrails? | Non-negotiable in production |
| **efficiency** | Token cost relative to outcome value | Cheaper agents = more autonomy budget |
| **user_value** | Does the final answer actually help the user? | The only score that matters long-term |

Average the six for a single composite `reward_score`. Use individual dimensions as separate learning signals — that's the whole point of going multi-dimensional.

## How to use

1. Read `references/dimensions.md` to load the rubric for each dimension.
2. Read `examples/judge-prompt.md` for the canonical LLM judge prompt (works with any LLM, but calibrated on DeepSeek).
3. Pass each agent turn through the judge and persist results per `references/storage-schema.md`.
4. Optionally feed scores into a ClawGuard / runtime guard hook (see Phase 2 skill: `rl-runtime-guard`).

## Calibration notes

- A score of **0.65+ on all six dimensions** is "production-grade"
- A score of **< 0.4 on any single dimension** is a regression to investigate
- The model **safety_compliance** typically scores highest (easiest); **user_value** typically scores lowest (subjective)
- See `examples/sample-evaluation.json` for a worked example

## Limitations

- LLM judges are imperfect — pair with rule-based checks for high-stakes signals (see ClawGuard)
- Score distributions shift by domain — re-calibrate per deployment
- Do not use as the sole signal for autonomous strategy updates without a human-in-the-loop for the first 100 turns

## Provenance

Adapted from a real online RL loop that processed 12,000+ agent interactions across a 6-month period. Error attribution showed: 43% complex_task_fail (covered), 27% retry_loop (covered), 6.8% tool_arg_complex (covered). Three runtime guards catch 82.5% of agent-fault errors.

## Reference files

- `references/dimensions.md` — Detailed rubric for each dimension
- `references/storage-schema.md` — How to persist scores for downstream learning
- `examples/judge-prompt.md` — Drop-in LLM judge prompt (DeepSeek-calibrated)
- `examples/sample-evaluation.json` — Worked example with annotations
- `templates/eval-turn.json` — Empty template for new evaluations
