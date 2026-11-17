# Crew Contract — Main–Sub Delegation (主-子分工)

*The main agent conducts — it doesn't play every instrument. A method-layer skill for any agent harness: a main agent keeps goal/constraints/evidence/final judgment, bounded subagents do noisy execution, and an independent reviewer gates material changes — with model-agnostic route selection built in.*

[English | [中文](README.zh-CN.md)]

## Why

Multi-agent work fails in predictable ways: reviewers grade their own family's output more kindly (measured family bias: 3.4–8.4pp), uncoordinated parallel agents amplify errors up to 17.2×, orchestration costs ~15× chat tokens, and truncated subagents lose their work. Crew Contract encodes what the evidence supports — and just as importantly, when *not* to orchestrate.

## What you get

- **Five bounded roles** (explorer / researcher / worker / tester / reviewer) with strict separation of duties — the reviewer is always a fresh, separate context; agents never self-review and never commit.
- **Delegation contract + copy-paste brief template** — self-contained briefs with budget/stop discipline, an ambiguity contract (`assumptions / needs_input / default_if_forced / blocking_level`), and SAVE-EARLY durability.
- **Model selection by route card** — no model names hardcoded: candidates come from your runtime's provider registry ∩ your model policy; execution slot and reviewer slot chosen up front, criteria-based (cheap+cache-affine executor, cross-family reviewer when policy allows).
- **Evidence-backed guardrails** — admission gate (orchestrate only when ≥2 of: parallelizable / exceeds one context window / value covers cost), cache-ordered cost levers, verification priority (deterministic > weak verifiers > LLM judges), optional manifest checkpoint protocol for replay-prone work.
- **Hand-down guidance by task shape** — judge delegation fit by clarity × verifiability × blast radius, calibrate verification to what the task can prove, and accumulate recipes in a living class playbook.
- **Honest limits** — reviewer independence is partial, depth-1 children cannot ask questions, no durable resume; documented as open, with mitigations only.

## Install

```bash
npx skills add mfang0126/crew-contract   # works across 77+ agent CLIs
```

Or clone the repo and point your agent's skills loader at the directory. Hermes Agent users can also install from the repo path.

## The method in 60 seconds

1. Decide: small task → main thread only (the skill defines the "don't orchestrate" criteria).
2. Pick routes: answer the route-card prompt (executor + reviewer slots), or reuse a matching card.
3. Dispatch self-contained briefs (template included) — one writer per area, read-only exploration first.
4. Verify with the smallest decisive test; independent review scales with risk.
5. The main agent reads the actual diff/artifacts before claiming anything.

## Evidence highlights

| Claim | Source |
|---|---|
| Parallelizable +81% / sequential −39…−70%; error amplification 17.2× → 4.4× with orchestrator | [Google agent-scaling study](https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/) |
| Multi-agent ≈15× chat tokens | [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system) |
| 41–86.7% failure across 7 SOTA multi-agent systems; "fail to ask" = 6.8% of failures | [MAST, arXiv:2503.13657](https://arxiv.org/abs/2503.13657) |
| Reviewer family bias 3.4–8.4pp without self-review | [arXiv:2508.06709](https://arxiv.org/abs/2508.06709), [arXiv:2609.17857](https://arxiv.org/abs/2609.17857) |
| Long-context degradation persists under perfect retrieval (13.9–85%) | [arXiv:2510.05381](https://arxiv.org/abs/2510.05381) |

Full rule → source map: [`references/evidence-index.md`](references/evidence-index.md).

## Repo layout

```
SKILL.md                          # the method layer (harness-agnostic)
references/
  child-brief-template.md         # copy-paste dispatch template
  class-playbook.md               # living notebook: task shape → recipe
  evidence-index.md               # rule → public sources
  hermes-mechanics.md             # example adapter for Hermes Agent
```

## License

MIT. Feedback and issues welcome.

---

## 中文简介

Crew Contract（主-子分工）——**主代理是指挥，不亲自演奏每个乐器**。方法层 skill：主代理把握目标/约束/证据/最终判断，有界子代理执行，独立评审把关——内置模型无关的路线卡选择机制。证据支撑的护栏包括：准入闸门、缓存优先的成本杠杆、验证优先级（确定性检查 > 弱验证者 > LLM 裁判）、可选 manifest 断点协议；并诚实记录未解局限。详细说明见 [README.zh-CN.md](README.zh-CN.md)。
