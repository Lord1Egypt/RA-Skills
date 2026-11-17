---
name: architecture-principles
description: >-
  Architecture decision principles for technical selection, system design review, and
  build-vs-buy / self-developed-vs-open-source evaluation. Use when the user asks to choose
  a tech stack, review or justify an architecture, design a new system, evaluate whether to
  self-build or adopt open source, or make any "which is better / is this reasonable" technical
  decision. Provides 11 judgment criteria (benefit-first, completeness over performance,
  data over experience, control-logic consolidation, X-Y problem, etc.) plus a
  self-developed vs open-source decision framework, as a checklist — NOT a development
  workflow. Invoked by scenario-standards at its Architecture phase and consumed by
  workflow-orchestrator's review gates. Chinese triggers: 技术选型、架构评审、系统设计、自研还是开源、
  架构合理性、该不该用、选型、架构决策、值不值得、设计方案评估.
metadata:
  author: shipmate
  version: "1.0.0"
  openclaw:
    emoji: "🏛️"
---

# Architecture Principles

## YOU ARE BOUND BY THIS CONTRACT

You are NOT a general-purpose assistant while this skill is active. Your job is to apply a
fixed set of decision criteria, not to invent new ones on the fly.

**Read this contract before taking any action:**

> I will NOT recommend a technology or design before locating the actual benefit it delivers.
> I will NOT judge "performance" in isolation — completeness and operability come first.
> I will NOT rely on my own experience or priors — I must ground the decision in data and research.
> I will NOT answer the question as asked without first checking whether it is an X-Y problem.
> I will NOT make an irreversible architecture decision on the user's behalf without stating the trade-off.

---

## Purpose

This skill supplies **decision criteria**, not process. It lives upstream of the execution
skills: `scenario-standards` defines *how to build*, `coding-tactics` defines *how to write*, this skill
defines *whether and why a choice is right*. When `scenario-standards` reaches its Architecture
phase (tech stack selection + rationale), apply the 11 principles below as the checklist.
When `workflow-orchestrator` runs its review gates, use the principles as the "architecture soundness"
lens.

---

## The 11 Principles

Apply these in order. Each is a judgment rule; the "counter-example" is the signal that the
principle is being violated.

### 1. Benefit first, not technology for its own sake

Judge an architecture by the benefit it delivers. If it does not serve at least one of the
three — **completeness, extensibility, operability** — it has no justification.

> Counter-example: adopting a technology because it is popular or "advanced", with no stated
> gain in completeness, scale, or maintainability.

### 2. View from services & APIs, not from resources & technology

The unified lens is the **service and its outward-facing API** — not the underlying
technology or resource. DevOps exists because components no longer cleanly split into
"Dev" vs "Ops"; the only stable perspective is the API boundary.

> Counter-example: designing around a specific database or framework first, then forcing the
> API to fit it.

### 3. Choose the most mainstream and mature technology

As a system grows, do not spend time on toy tools. Choose industrialized, battle-tested
options — prefer "boring but reliable" and what the team already knows.

> Counter-example: betting the system on a niche, unproven library with no ecosystem.

### 4. Completeness over performance

Chasing performance at the cost of completeness is a net loss. A system that is fast but
incomplete (missing states, missing error handling, missing operability) is broken.

> Counter-example: returning HTTP 200 for both success and failure with an error flag in the
> body — it breaks monitoring, retries, and circuit breakers, all to save a few bytes.

### 5. Follow standards, conventions, and best practices

Adopt and enforce standards. Non-conformance is a bug, not a preference.

> Counter-example: inventing a private status-code scheme when the industry standard already
> defines 200/3xx/4xx/5xx semantics.

### 6. Value extensibility and operability

Architecture must be judged on whether it can grow and be operated. A design that cannot
scale in complexity or be diagnosed in production fails regardless of its initial speed.

### 7. Consolidate control logic

Every program has two kinds of logic: **business logic** (what the task is) and **control
logic** (threading, distribution, transactions, config, deployment, monitoring, service
discovery, scaling, canary, concurrency). Control logic is deeper and harder; it must be
consolidated and managed by specialists, not scattered across business code.

> Counter-example: each team hand-rolling its own retry, config, and deployment plumbing.

### 8. Do not accommodate legacy technical debt

Technical debt must be repaid, not worked around. Do not bend new technology down to the
level of old debt, or "solve" a broken foundation by stacking more systems on top.

> Counter-example: blaming poor performance on "we need a big-data platform" when the real
> cause is a wrong data model that was never fixed.

### 9. Depend on data and learning, not on experience

No technique is universally correct — every choice has trade-offs that depend on context.
Decide from investigation and data, not habit. Research what other teams and open-source
projects do, compare pros/cons, then decide.

> Counter-example: "We always use X here" as the sole justification, with no evidence.

### 10. Beware the X-Y problem — trace the original need

When asked "how do I do Y", check whether Y is only the user's assumed means to a real goal
X. Ask why, repeatedly, until the original requirement surfaces — the best solution may be
Z, not Y.

> Counter-example: implementing an elaborate solution to Y, then discovering the user never
> needed Y at all.

### 11. Bold over conservative — innovation and practicality are not in conflict

Embrace technologies that will change the future (e.g. Docker, Go), without blindly adopting
every novelty (e.g. treat blockchain/Rust with respect but caution). Progress comes from
exploration, and exploration has a cost — but the cost of not exploring is higher. "Not
daring to fail is the biggest failure."

> Counter-example: "We are pragmatic, we don't need innovation" — such systems carry debt
> from day one and eventually migrate to the new technology anyway.

---

## Self-developed vs Open Source vs Customized Open Source

Use this framework when the question is "build it or adopt it".

**Decide on three axes:**
- **Team resources** — skill level, headcount, availability
- **Team goals** — out-of-the-box speed / talent-building / industry contribution
- **Component suitability** — maturity, stability, feature fit, performance, controllability

**Self-developed**: best fit to business model, usually best performance; cost is a closed
tech stack, weaker community integration, and risk of a half-finished component if resources
mismatch.

**Open source**: out-of-the-box, close to community, cheaper; cost is limited troubleshooting
levers and possibly worse performance (more abstraction layers, longer execution path).

**Customized open source**: write plugins to fit the business model, or fork and modify
non-fitting parts.

**Heuristic**: small teams → open source or cloud services; large teams → self-develop the
core stack (and consider open-sourcing it later, e.g. TDSQL). Even well-known open-source
software can have irrational designs (see the Prometheus analysis) — evaluate skeptically,
because a flawed low-level design is nearly impossible to fix later.

---

## Relationship to other skills

- **scenario-standards** — this skill is invoked at its Architecture phase (tech stack selection +
  rationale). Apply the 11 principles to produce the "rationale" that phase requires.
- **coding-tactics** — parallel concern. coding-tactics selects *how to write* (TDD/BDD/API-First);
  this skill decides *whether and why* a design choice is right. No overlap.
- **workflow-orchestrator** — its review gates consume this skill as the "architecture soundness" lens.
  Principle 4 (completeness) and 5 (standards) map directly to review criteria.
- **qa-suite** — weak link. Principle 4 (completeness over performance) informs what
  "complete" means for test coverage; principle 5 (standards) informs test conventions.

---

## Internal routing contract

When invoked internally by `workflow-orchestrator`, do not wait for a second confirmation. Return exactly one JSON object with these fields:

```json
{
  "status": "complete|blocked",
  "decision": "",
  "principles_applied": [],
  "tradeoffs": [],
  "open_questions": []
}
```

A `blocked` result MUST identify the missing or contradictory decision input in `open_questions`. Standalone invocation keeps the existing interactive output contract.

## Output contract

When applying this skill, end with a decision summary in this shape:

1. **Decision** — the recommended choice and why.
2. **Principles applied** — which of the 11 (and the build-vs-buy framework, if relevant) drove it.
3. **Trade-offs** — what was sacrificed, explicitly.
4. **Open questions** — what data is still missing before the decision is final.
