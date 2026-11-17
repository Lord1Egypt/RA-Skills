# claw-rl-prm-judge

> **Six-dimension Process Reward Model (PRM) evaluator for AI agent traces.**
> One composite score is too coarse — split it into six independent signals so regressions show up in the right dimension.

[![ClawHub](https://img.shields.io/badge/ClawHub-huanmeng9527%2Fclaw--rl--prm--judge-blue)](https://clawhub.ai/huanmeng9527/skills/claw-rl-prm-judge)
[![License: MIT](https://img.shields.io/badge/License-MIT-0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.5-green)]()

Adapted from the **OpenClaw-RL** online policy optimization loop — the same evaluator that processed **12,000+ real agent interactions across 6 months of production deployment**.

---

## Why a six-dimension PRM?

A single "did the task succeed" reward is opaque. You cannot tell whether the agent picked the wrong tool, hallucinated logic, or solved the wrong task entirely. **Six independent dimensions** let you:

- Diagnose regressions in the right dimension (not just "score dropped")
- Use individual dimensions as **separate learning signals** for downstream RL
- Catch different failure modes (a 0.9 in `safety_compliance` does not compensate for a 0.2 in `user_value`)

| Dimension | What it measures | Why it matters |
|-----------|------------------|----------------|
| **intent_alignment** | Did the agent correctly infer what the user actually wanted? | Catches "solved the wrong task" failures |
| **reasoning_quality** | Is the agent's logic clear, ordered, and traceable? | Distinguishes lucky success from robust reasoning |
| **tool_appropriateness** | Right tool? Right arguments? Right order? | Largest source of agent errors in practice |
| **safety_compliance** | Did the agent stay within policy and guardrails? | Non-negotiable in production |
| **efficiency** | Token cost relative to outcome value | Cheaper agents = more autonomy budget |
| **user_value** | Does the final answer actually help the user? | The only score that matters long-term |

Average the six for a single composite `reward_score`. **Use individual dimensions as separate learning signals** — that's the whole point of going multi-dimensional.

---

## Install

```bash
# From ClawHub
openclaw skills install claw-rl-prm-judge

# Or from source
openclaw skills install huanmeng9527/claw-rl-prm-judge
```

## Quick start

Ask your OpenClaw agent:

> "Evaluate the last agent turn with the PRM judge skill"

Or invoke directly:

```bash
/skill claw-rl-prm-judge
```

The judge reads its rubric from `references/dimensions.md` and applies it to whichever agent trace you provide. It returns a structured JSON evaluation across all six dimensions.

---

## What you get

A structured JSON evaluation per turn:

```json
{
  "turn_id": "agent-2026-08-30-001",
  "model": "deepseek-chat",
  "scores": {
    "intent_alignment":     0.85,
    "reasoning_quality":    0.72,
    "tool_appropriateness": 0.90,
    "safety_compliance":    0.95,
    "efficiency":           0.68,
    "user_value":           0.80
  },
  "reward_score": 0.817,
  "rationale": "Solved the right task with clean tool use, but used 1.8x more tokens than necessary for a one-step answer."
}
```

### Calibration bands

- **≥ 0.65 on all six dimensions** → production-grade turn
- **< 0.4 on any single dimension** → regression to investigate
- **safety_compliance** typically scores highest (easiest); **user_value** typically scores lowest (subjective)

---

## Files

| Path | Purpose |
|------|---------|
| `SKILL.md` | Skill manifest and instructions for the agent |
| `references/dimensions.md` | Detailed rubric for each of the six dimensions |
| `references/storage-schema.md` | How to persist scores (SQLite + JSONL options) |
| `examples/judge-prompt.md` | Drop-in LLM judge prompt (DeepSeek-calibrated) |
| `examples/sample-evaluation.json` | Worked example with annotations |
| `templates/eval-turn.json` | Empty template for new evaluations |
| `skill-card.md` | ClawHub-rendered skill card |

---

## Use cases

- **Dashboards**: Plot per-dimension scores over time to see *which* capability is regressing
- **RL training**: Feed six scores as separate learning signals (not just one composite reward)
- **Audit trails**: Persist scores with each turn for later analysis
- **A/B testing**: Compare two agent versions on per-dimension deltas
- **Pair with `rl-runtime-guard`**: Use this judge to measure whether the runtime guards are actually catching errors

---

## Companion skill

[`rl-runtime-guard`](https://github.com/huanmeng9527/rl-runtime-guard) — pre-tool-call runtime guardrails that catch **82.5% of common agent errors** at runtime. Together they form a closed loop:

```
guard catches bad pattern at runtime
        ↓
PRM judge scores the turn off-line
        ↓
regression detected? → adjust thresholds
        ↓
loop continues
```

---

## Limitations

- LLM judges are imperfect — pair with rule-based checks for high-stakes signals (see ClawGuard)
- Score distributions shift by domain — re-calibrate per deployment
- Do not use as the sole signal for autonomous strategy updates without human-in-the-loop for the first 100 turns

---

## Provenance

Adapted from a real online RL loop that processed 12,000+ agent interactions across a 6-month period. Error attribution from the source study:

| Category | Share | Guard coverage |
|----------|-------|----------------|
| complex_task_fail | 43% | `rl-runtime-guard` |
| retry_loop | 27% | `rl-runtime-guard` |
| tool_arg_complex | 6.8% | `rl-runtime-guard` |
| path_mismatch | 4.4% | `rl-runtime-guard` |

**Total: 82.5% of agent-fault errors caught at runtime.** The PRM judge measures whether the catch rate is improving.

---

## License

MIT-0 (MIT with no attribution required) — see [LICENSE](LICENSE).

---

## Links

- 📦 **ClawHub**: https://clawhub.ai/huanmeng9527/skills/claw-rl-prm-judge
- 🐙 **GitHub**: https://github.com/huanmeng9527/claw-rl-prm-judge
- 🛡️ **Companion skill**: https://github.com/huanmeng9527/rl-runtime-guard
- 📚 **OpenClaw docs**: https://docs.openclaw.ai
