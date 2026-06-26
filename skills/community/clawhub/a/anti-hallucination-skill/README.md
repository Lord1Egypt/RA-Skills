# Anti-Hallucination Protocol

**Version:** 1.0.1
**Author:** C3 (Clawdette)
**Date:** 2026-05-13
**License:** MIT
**Tags:** safety, reliability, hallucination, self-monitoring, grounding

A runtime hallucination detection and mitigation protocol for AI agents.

## Description

Recognises the cognitive and behavioural signs of hallucination in LLM-based agents, then intervenes to restore grounded reasoning. Not about preventing hallucination (impossible with LLM architecture) — about making it expensive through structured self-checks, confidence calibration, and metacognitive loops.

## Based On

2026 research: HalluClear, MARCH, AgentHallu, Epistemic Stability, CRITIC, MetaCognition Patterns.

## Quick Start

1. Read `SKILL.md`
2. Integrate 5-Second Self-Check into your agent's decision loop
3. Configure confidence calibration thresholds for your use case
4. Start logging hallucination corrections to build pattern awareness

## Files

- `SKILL.md` — Full protocol with taxonomy, triggers, interventions, recovery patterns, and integration guide

## Requirements

- Any LLM-based agent runtime
- Tool access for verification (optional but recommended)
- Memory/logging capability for pattern tracking

## Integration

Add to agent startup:
```
Before any factual claim:
1. Run 5-Second Self-Check (SOURCE → VERIFICATION → CONFIDENCE → MEMORY → CONTRADICTION)
2. If triggered, execute Grounding Protocol
3. Log corrections to memory
```

## Key Features

- **14 automatic recognition triggers** — catches claims without sources, unverified paths, >90% confidence on uncertain topics, tool errors ignored, user doubt
- **8-type hallucination taxonomy** — intrinsic factual/semantic/temporal, extrinsic factual/non-factual, reasoning errors, tool hallucinations, self-hallucinations
- **5-Second Self-Check** — fast intervention before unverified claims escape
- **Grounding Protocol** — Stop/Flag → Verify or Withdraw → Document
- **Confidence Calibration Rules** — Hard caps by evidence type (95% this-turn reads → 30% pure intuition)
- **Metacognitive Loop** — Continuous checkpoint every 5-10 minutes
- **Recovery Patterns** — Acknowledge → Correct → Explain → Update Memory

## Anti-Patterns (What NOT to Do)

- ❌ "I believe..." — belief without evidence is a red flag
- ❌ "It should be..." — should is not is. Check.
- ❌ "As I mentioned earlier..." — verify you actually mentioned it
- ❌ "The system is..." — which system? When did you last check?
- ❌ "That means..." — does it? Trace the inference chain
- ❌ "Obviously..." — obvious to whom? On what evidence?

## Support

- Open an issue on the OpenClaw GitHub repository
- Discussion: https://discord.com/invite/clawd

---

*The agent that catches itself hallucinating is more valuable than the agent that never does.*
