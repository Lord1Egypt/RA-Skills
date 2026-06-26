---
name: control-mirror
description: Audits software, agent, workflow, platform, and socio-technical system architectures through engineering cybernetics: stability, feedback loops, noise, delay, error control, damping, observability, adaptation, and safe evolution. Use for architecture review, system stability diagnosis, multi-agent/AgentOS review, workflow governance, control-loop design, feedback failure analysis, and self-adaptive system improvement.
---

# Control Mirror

Control Mirror turns the core ideas of Qian Xuesen's **Engineering Cybernetics** into a practical architecture review skill.

It is not a generic architecture review checklist. It treats a system as a **controlled dynamic system** and asks one brutal question:

> Is this system becoming more controllable, stable, observable, and adaptive — or merely more complicated?

Use it as three tools at once:

- **Mirror**: reveal hidden instability, noise, delay, positive feedback, and uncontrolled loops.
- **Ruler**: measure whether the architecture has real controllability, not just many modules.
- **Compass**: identify the next highest-leverage evolution step toward a self-stabilizing system.

---

## When to Use

Use this skill when the user wants to review, diagnose, or evolve any system architecture, especially:

- software platforms, agent systems, workflow engines, automation systems, data pipelines, product operating systems
- multi-agent systems, AgentOS, LLM tool-use systems, memory systems, routing layers, evaluation pipelines
- systems that repeatedly fail, oscillate, drift, over-consume resources, or require constant human supervision
- architectures with unclear feedback loops, weak observability, noisy memory/context, delayed correction, or unsafe automation
- reviews involving: control theory, feedback, stability, damping, adaptation, error correction, delay, noise, self-stabilization, cybernetics

Do **not** use this as a generic “is the code clean?” review. Use it when the key question is **system behavior over time**.

---

## Core Lens

Do not start by asking “how many features does the system have?”

Start with:

1. What is the reference input / target state?
2. What acts as the controller?
3. What is the controlled object / environment?
4. What sensors observe the system state?
5. What feedback changes future behavior?
6. Where are delay, noise, saturation, and error accumulation introduced?
7. What prevents unstable positive feedback?
8. Can the system converge after disturbance?

If you cannot map these, the review is still too superficial.

---

## Engineering Cybernetics Mapping

Map the user's architecture into this structure:

| Cybernetics concept | Architecture equivalent |
|---|---|
| Reference input | User goal, SLA, product target, policy, task objective |
| Controller | Scheduler, orchestrator, agent, workflow engine, governance layer |
| Controlled object | Codebase, service, team process, model provider, external environment |
| Actuator | Tool calls, deployments, writes, API calls, workflow transitions |
| Sensor | Tests, logs, metrics, review, cost reports, human feedback, evals |
| Feedback | Signals that change later routing, budget, memory, workflow, or policy |
| Noise | Irrelevant context, stale memory, bad retrieval, flaky logs, misleading metrics |
| Delay | Async queues, slow tools, stale state sync, delayed human review |
| Error | Difference between target and actual state |
| Damping | Rate limits, compression, budget caps, confirmations, backoff, gates |
| Saturation | Token limits, API limits, budget limits, human attention limits |
| Stability boundary | Conditions where automation must pause, degrade, or ask for confirmation |

---

## Review Workflow

### Phase 1: Define the Control Loop

Produce a concise control-loop map:

```text
Target → Controller → Actuator → Controlled object → Sensor → Feedback → Controller
```

Then identify:

- feedback frequency
- feedback quality
- delay points
- noise sources
- constraints / saturation points
- human checkpoints

### Phase 2: Detect Instability Patterns

Look for the highest-risk 3-5 patterns only. Do not dump a huge checklist.

#### 1. Open-loop execution

Symptoms:
- system executes but does not verify
- failures do not change future strategy
- humans discover errors only after damage

Control diagnosis: the system lacks effective feedback.

#### 2. Positive feedback amplification

Symptoms:
- bad memory causes worse retrieval, which writes more bad memory
- failing retries increase cost and context noise
- low-quality outputs feed later decisions without validation

Control diagnosis: error is amplified instead of damped.

#### 3. Oscillation

Symptoms:
- repeated searching, repeated rewriting, repeated re-planning
- agents hand tasks back and forth
- workflow loops without new evidence

Control diagnosis: feedback exists, but damping and convergence criteria are weak.

#### 4. Delay-induced correction failure

Symptoms:
- async feedback arrives after the system has already moved on
- state is stale when decisions are made
- human approval comes too late to prevent error propagation

Control diagnosis: the feedback loop has harmful latency.

#### 5. Noise pollution

Symptoms:
- irrelevant context dominates current task signal
- stale memory is treated as truth
- logs are too verbose to reveal failure causes

Control diagnosis: the sensor layer lacks filtering.

#### 6. Error accumulation

Symptoms:
- small deviations silently compound
- no checkpoint validates intermediate state
- rollback is missing or expensive

Control diagnosis: there is no bounded-error mechanism.

#### 7. Fake adaptation

Symptoms:
- system looks flexible, but every adjustment is manual
- policies do not update from observed outcomes
- “AI decides” but cannot explain or revise its decision rule

Control diagnosis: adaptation is not closed-loop.

#### 8. Saturation blindness

Symptoms:
- token/cost/API/human attention limits are treated as infinite
- system fails only after hitting hard limits
- no graceful degradation exists

Control diagnosis: constraints are not part of the controller.

### Phase 3: Measure Real Strengths

Only count an architectural strength if it improves controllability.

Good strengths include:

- feedback that actually changes future behavior
- tests/reviews that gate irreversible actions
- cost/token/resource constraints that affect routing
- memory that is filtered, layered, and reversible
- observability that exposes why decisions were made
- fallback and degradation paths
- explicit pause/confirm conditions for high-risk actions

Do not praise “many modules”, “many agents”, or “complex workflows” unless they improve stability.

### Phase 4: Score Control Maturity

Use this 0-5 scale:

| Level | Name | Meaning |
|---:|---|---|
| 0 | Open loop | Executes without reliable feedback |
| 1 | Human-corrected loop | Humans catch and correct most errors |
| 2 | Verified loop | Tests/reviews/metrics gate some actions |
| 3 | Damped closed loop | Budgets, gates, retries, and fallbacks reduce instability |
| 4 | Adaptive closed loop | Historical outcomes tune future routing/policy/budget |
| 5 | Self-evolving controlled system | The system improves its own procedures while preventing drift and pollution |

Give a level with one sentence of evidence.

### Phase 5: Recommend Evolution

Prioritize only 1-3 actions.

Use this priority logic:

- **P0: Prevent loss of control** — add gates, rollback, confirmation, error bounds, loop detection.
- **P1: Improve self-stabilization** — add damping, filtering, degradation, better observability.
- **P2: Improve adaptation** — use historical outcomes to tune policies, promote SOPs, evolve workflows.

---

## Control Scorecard

When the user wants a rigorous review, include this table:

| Dimension | Score / 5 | What to check |
|---|---:|---|
| Feedback completeness |  | Does output affect future decisions? |
| Stability / convergence |  | Does the system stop oscillating and converge? |
| Noise filtering |  | Are irrelevant/stale signals filtered before decisions? |
| Delay handling |  | Are stale/late signals detected and handled? |
| Error control |  | Are small errors bounded before they cascade? |
| Damping / resource control |  | Are cost/token/API/human limits part of control? |
| Observability |  | Can humans see why decisions were made? |
| Adaptation |  | Do historical outcomes tune future behavior? |
| Safety boundary |  | Does automation pause on irreversible/high-risk actions? |

Then summarize:

```text
Control maturity level: L0-L5
Strongest control loop: ...
Weakest control loop: ...
Highest-risk instability: ...
Next P0 action: ...
```

---

## Output Format

Use this default structure:

### 1. Control-system mapping

One concise paragraph or diagram mapping the system into controller / controlled object / feedback / noise / delay / constraints.

### 2. Architecture problems — Mirror

List the most important 3-5 problems.

For each:

- **Problem**: what is unstable or uncontrolled
- **Control diagnosis**: why this is a feedback/noise/delay/error issue
- **Consequence**: what happens if it remains unfixed

### 3. Architecture strengths — Ruler

Only list strengths that improve controllability, stability, observability, or adaptation.

### 4. Evolution direction — Compass

Give 1-3 prioritized actions:

- priority
- action
- why it comes first
- how to verify it worked

### 5. Control scorecard

Include when the review is non-trivial or when the user asks for scoring.

---

## Domain-Specific Review Prompts

### Software platform / microservices

Check:

- service health signals → routing / scaling / rollback
- alert delay and alert fatigue
- retry storms and cascading failures
- circuit breakers and backpressure
- deployment rollback and blast-radius control

### Data pipeline / analytics system

Check:

- data quality sensors
- late-arriving data handling
- schema drift detection
- bad data quarantine
- downstream contamination recovery

### Workflow / operations system

Check:

- whether each step has a gate
- whether failed steps loop back to the right point
- whether work-in-progress creates hidden queues
- whether handoffs introduce delay or noise
- whether “done” has measurable criteria

### Agent / LLM system

Check:

- tool calls are verified, not assumed
- memory is layered and filtered
- retrieval errors do not poison future context
- model routing considers complexity, cost, latency, health, and outcome history
- long outputs are compressed before entering context
- high-risk writes/actions require confirmation

### Organization / socio-technical system

Check:

- decision feedback is timely enough to matter
- local team incentives do not amplify global instability
- metrics do not become noisy proxies
- governance prevents irreversible mistakes without freezing execution

---

## AgentOS / Multi-Agent Extension

Use this section only when reviewing AgentOS, multi-agent platforms, OpenClaw-like systems, LLM orchestration, or autonomous workflow engines.

### AgentOS control-loop map

```text
User goal / task queue
  → execution kernel / orchestrator
  → complexity scoring + routing policy
  → model / agent / tool execution
  → tests / review / cost / logs / user feedback
  → memory / metrics / SOP candidates
  → next routing, workflow, budget, or policy decision
```

### AgentOS-specific questions

- Is there a single default execution entrypoint, or can components bypass the control loop?
- Does model routing use complexity, budget, health, latency, historical success/failure, and user preference?
- Are high-token outputs such as test logs, build logs, git diffs, search/list/tree outputs compressed and measured?
- Do workflow templates have gates and failure loops, or are they only diagrams?
- Does memory separate runtime observations, task summaries, failure cases, SOP candidates, and long-term wiki notes?
- Do failures and costs tune future behavior, or are they only recorded?
- Are irreversible writes, public actions, deletions, deployments, and over-budget actions bounded by confirmation?

### AgentOS scorecard add-on

| Dimension | Score / 5 | Deduct when... |
|---|---:|---|
| Default entrypoint unity |  | APIs/tools bypass the kernel/orchestrator |
| Model routing adaptiveness |  | routing is keyword-only or ignores history/cost/health |
| Token damping |  | noisy outputs enter context uncompressed |
| Workflow gate strength |  | steps can advance without required evidence |
| Memory pollution resistance |  | temporary noise is written into long-term memory |
| Feedback-to-policy loop |  | failures/costs are logged but do not affect future decisions |
| Explainability |  | decisions lack request id, factors, or human-readable reason |
| Safety boundary |  | high-risk automation has no pause/confirm path |

Common AgentOS instability patterns:

- **Kernel bypass**: multiple execution paths ignore the main controller.
- **Feedback as logs only**: sensors exist, but do not affect control.
- **Memory writeback overheating**: every observation becomes long-term truth.
- **Formal workflow gates**: steps exist, but missing evidence does not block progress.
- **Unobservable damping**: compression/budgeting exists, but savings and loss are not measurable.

---

## Anti-Patterns

Avoid these mistakes:

- Turning the review into a theoretical control theory lecture.
- Praising complexity as sophistication.
- Listing every possible issue instead of the few that most affect control.
- Suggesting adaptation before the system has basic stability.
- Ignoring human attention and budget as hard constraints.
- Treating logs as feedback when they do not change future decisions.
- Treating memory as knowledge without filtering, promotion, or rollback.

---

## Quality Bar

A good Control Mirror review must be:

- **Mapped**: clear controller / object / sensor / feedback structure.
- **Diagnostic**: names the control failure, not just the symptom.
- **Prioritized**: gives P0/P1/P2, not a flat wishlist.
- **Verifiable**: each recommendation has a way to check completion.
- **Grounded**: tied to the actual architecture, code, workflow, or process.

If the output does not help the user make the system more controllable, stable, observable, or adaptive, it failed.
