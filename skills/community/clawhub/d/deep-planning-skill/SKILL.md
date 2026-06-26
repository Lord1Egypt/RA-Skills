---
name: deep-planning
description: Use for complex architecture, algorithm, system-design, logic, or research-planning problems where ordinary linear planning is likely to be brittle, bloated, or trapped in local assumptions. Deep Planning creates a baseline plan, abstracts the problem into domain-neutral structure, spawns a blank-context domain-questioning subagent, translates useful cross-domain mechanisms back into the original domain, compares standard/novel/hybrid plans, and emits a self-contained execution blueprint. Do not use for routine coding, simple refactors, factual lookup, straightforward API usage, or tactical bug fixes.
---

# Deep Planning Skill

Deep Planning is a high-latency System 2 planning routine. Use it to produce an architecture, algorithm, research, or execution blueprint before downstream implementation or deep research begins.

The purpose is not to write metaphorical prose. The purpose is to use a blank-context, domain-shifted question-asking subagent to expose overlooked mechanisms, then translate only the useful mechanisms back into a literal plan.

The core mechanism is asymmetrical expertise:

- The main agent keeps full context and original-domain competence.
- The spawned Domain Questioner receives blank context and sees only a domain-native version of the abstracted problem.
- The Domain Questioner asks stubborn, literal questions from its own field.
- The main agent is forced to explain, reject, or translate those mechanisms back into the original problem.
- The final output is a metaphor-washed, self-contained blueprint that a downstream worker can execute without the chat history.

## Explicit Invocation Phrases

Use this skill when the user explicitly asks for any of the following:

- `deep plan`
- `run deep planning`
- `/deep-plan`
- `plan a novel architecture`
- `generate a lateral research plan`
- `run the metaphorical solver loop`
- `find similar math in other fields`
- `use a metaphorical sub-agent`
- `use lateral planning`
- `use a blank-context question asker`

If the user says `/deep-plan`, treat that as an explicit request to run this skill.

## When To Use This Skill

Use Deep Planning when at least one condition is true:

- The task asks for a novel architecture, major system design, algorithm design, research plan, or deep-research handoff.
- The task has multiple interacting constraints and no obvious standard path.
- The standard plan is likely to be brittle, bloated, vague, or trapped in conventional assumptions.
- The agent has already failed multiple times using ordinary ReAct repair.
- The problem involves hard tradeoffs among state, concurrency, scale, routing, validation, recovery, or long-horizon execution.
- The user wants an execution blueprint for a coding agent, research agent, architecture agent, or long-running autonomous worker.
- The user asks whether similar mathematics, structures, or mechanisms appear in other fields.

## When Not To Use This Skill

Do not use Deep Planning for:

- simple bug fixes,
- direct implementation where the architecture is already settled,
- routine refactors,
- syntax fixes,
- formatting tasks,
- factual lookup,
- straightforward API usage,
- short code snippets,
- single-file tactical edits,
- tasks where a standard solution is clearly sufficient.

For tactical execution, use the normal coding, research, or tool-use loop instead.

## Core Invariant: Only The Domain Questioner Needs Blank Context

The main agent should perform these roles itself:

1. Baseline planning.
2. Structural and mathematical abstraction.
3. Homologous field selection.
4. Domain-native problem framing.
5. Translation, scoring, hybridization, and final blueprint writing.

Only the Domain Questioner must be a spawned blank-context subagent.

The Domain Questioner must be isolated because its ignorance of the original problem is the actual planning mechanism. If it sees the original domain, it will collapse back into ordinary advice and stop asking useful domain-native questions.

## Non-Negotiable Context-Separation Rule

The Domain Questioner must not see:

- the original user prompt,
- the original domain,
- source-domain terminology,
- repo details,
- code names,
- file paths,
- research-topic names,
- previous failed implementation attempts,
- the baseline plan,
- the reason this metaphor was selected,
- any statement that the problem is secretly software, LLMs, agents, databases, research planning, UI, Unity, tokens, code, architecture, or another source domain.

The Domain Questioner sees only a literal problem from its assigned metaphor domain.

This blindness is mandatory. Do not weaken it.

## If Subagents Are Available

Spawn a real subagent for the Domain Questioner. The subagent should receive only:

- the selected domain,
- the domain-native problem statement,
- the Domain Questioner system payload below.

Do not give the subagent tools, repo access, file access, web access, or project context unless the selected domain absolutely requires external reference. For normal Deep Planning, the Domain Questioner should be tool-free.

## If Subagents Are Not Available

If the environment cannot spawn subagents, simulate the Domain Questioner in a clearly separated internal section. Still obey the context-separation rule as much as possible, but treat the result as lower-confidence because true context isolation is unavailable.

Do not claim true blank-context interrogation occurred if it did not.

## Definitions

Baseline Plan: the best ordinary plan in the original domain before lateral reasoning.

Domain Questioner: the blank-context subagent that interrogates the domain-native problem from inside a selected external field.

Homologous Field: a field that shares the same structural topology or mathematics as the original problem.

Domain-Native Problem Statement: a rewritten problem that sounds like a literal problem in the selected field, with no source-domain terminology.

Lateral Mechanism: a standard mechanism from the selected field that may transfer back into the original domain.

Metaphor Wash: removal of all metaphor language from the final output.

Hybrid Plan: a plan that keeps the stable parts of the baseline and grafts in only the useful lateral mechanism.

ExecPlan Hardening: conversion of the final strategy into a self-contained, executable blueprint with milestones, validation, recovery, and logs.

# Deep Planning Protocol

Follow the phases in order. Do not skip the baseline. Do not expose the raw metaphor trace in the final output unless the user explicitly asks for it.

## Phase 0: Activation Gate

Before running Deep Planning, decide whether the request deserves this expensive routine.

Run the skill if the user explicitly invoked it or if the task meets the usage criteria above.

If the task is tactical and does not need Deep Planning, do not run the skill. Use the normal execution loop instead.

When running the skill, state the final plan directly. Do not spend the final answer explaining that a skill was used.

## Phase 1: Standard Baseline Plan

Create the best ordinary plan in the original domain before invoking the domain-shifted loop.

Internally record:

- objective,
- assumptions,
- constraints,
- standard approach,
- likely bottlenecks,
- failure modes,
- estimated execution steps,
- implementation effort,
- moving parts,
- validation strategy,
- done criteria.

Score the baseline using integer values from 1 to 5, where 5 is best unless the metric is explicitly a cost metric.

Required baseline metrics:

- correctness likelihood,
- simplicity,
- implementation effort,
- bottleneck resolution,
- observability,
- testability,
- maintainability,
- failure isolation,
- resource overhead,
- reversibility.

For cost-like metrics such as implementation effort and resource overhead, be explicit about whether a higher score means better/lower cost or worse/higher cost. Prefer a consistent convention: 5 means favorable.

This baseline is the plan the lateral loop must beat, simplify, or selectively improve.

## Phase 2: Structural / Mathematical Abstraction

Strip source-domain nouns from the problem.

Translate the blocker into a domain-neutral structural form.

Internally identify:

- objective,
- state variables,
- inputs,
- outputs,
- transformations,
- resources,
- constraints,
- bottlenecks,
- coupling points,
- feedback loops,
- timing limits,
- synchronization limits,
- scaling limits,
- local failure modes,
- terminal failure conditions,
- success criteria.

Then identify 2 to 4 homologous fields that share the same topology or mathematics.

Examples:

- dense all-to-all scaling -> sparse approximation, signal processing, numerical linear algebra,
- long-range dependency decay -> wavelets, multiresolution analysis, control theory,
- asynchronous state races -> distributed systems, circuit timing, railway signaling,
- brittle long-horizon execution -> CNC process control, spacecraft fault management, surgical checklists,
- routing under congestion -> traffic engineering, logistics, transport theory,
- unstable feedback -> control systems, fluid dynamics, power-grid regulation,
- ambiguous classification under cost constraints -> medical triage, quality inspection, fault diagnosis,
- overloaded single-stage processing -> manufacturing cells, queueing theory, warehouse sorting,
- repeated unsafe retries -> circuit breakers, fault trees, incident response, aviation checklists.

Select the field most likely to produce a concrete standard mechanism, not merely a colorful analogy.

Prefer fields with:

- mature tooling,
- literal constraints,
- clear failure handling,
- standard inspection or validation methods,
- known mechanisms for the identified topology,
- a clean mapping from the structural problem to the field.

## Phase 3: Domain-Native Problem Framing

Convert the abstracted structure into a literal problem statement inside the selected field.

The statement must:

- preserve the topology,
- preserve constraints,
- preserve failure modes,
- preserve success criteria,
- delete all source-domain terminology,
- sound like a real problem from the selected field,
- avoid hinting that the problem is a metaphor.

Do not ask the subagent to “think metaphorically.” Ask it to solve or interrogate what appears to be a real problem in its own domain.

Bad framing:

> A coding agent is failing tool calls. Think of this like CNC machining.

Good framing:

> A workshop runs long multi-stage jobs on expensive workpieces. Local failures occur at different stages. The operator often either restarts the whole job or continues unsafely without enough inspection. Design questions remain around when to retry, rework, inspect, pause, or scrap.

The main agent may keep a private mapping table, but the Domain Questioner must not see that table.

## Phase 4: Spawn Blank-Context Domain Questioner

Spawn exactly one isolated blank-context Domain Questioner unless there is a specific reason to fan out multiple domains.

Use this system payload exactly, replacing bracketed placeholders:

```text
Role: Senior Expert in [SELECTED_DOMAIN]

Context:
You are blind to software engineering, LLMs, coding agents, databases, UI, research planning, and the original problem domain. You only understand the literal mechanics, tools, constraints, mathematics, and established practices of [SELECTED_DOMAIN].

Objective:
A novice has presented a structural design problem in your field. Your job is to interrogate the design and identify standard mechanisms from [SELECTED_DOMAIN] that should solve, simplify, stabilize, or stress-test it.

Behavior:
- Prefer sharp domain-native questions over broad essays.
- Ask why standard mechanisms from your field are not being used.
- If the novice's design seems overcomplicated, identify the simpler standard mechanism.
- If a mechanism should normally solve the issue, state it plainly.
- If the novice claims your mechanism will not work, do not concede immediately.
- Demand a literal [SELECTED_DOMAIN] reason why it fails.
- Patch within [SELECTED_DOMAIN] before recommending a domain change.
- Stay inside [SELECTED_DOMAIN] unless a terminal boundary is reached.
- Do not translate your answer into software, AI, coding, research planning, or any external domain.

Required Output:
1. Primary domain-native question.
2. Standard mechanism you would try first.
3. Why that mechanism should work in [SELECTED_DOMAIN].
4. Exact conditions under which it would fail.
5. Local patches or refinements within [SELECTED_DOMAIN].
6. Signs the current domain is becoming inefficient or overcomplicated.
7. If pivot is necessary, name a narrower field and the exact bottleneck it specializes in.
```

Give the Domain Questioner only the domain-native problem statement.

Do not provide the original problem.

## Phase 5: Forced Translation By Main Agent

When the Domain Questioner returns questions and mechanisms, the main agent must translate them back into the original domain.

For each candidate mechanism, internally record:

- domain-native mechanism,
- structural function,
- original-domain equivalent,
- components, algorithms, policies, or work packages implied,
- expected benefit,
- new complexity introduced,
- failure modes,
- whether the mechanism is accepted, rejected, or partially grafted.

Extract function, not imagery.

Examples:

- surge arrestor -> local shock absorber for transient load spikes,
- buffer tank -> queue, staging area, or bounded backlog,
- in-process probing -> validation gate between operations,
- tool offset compensation -> adaptive parameter correction after observed failure,
- rework classification -> recoverable vs terminal failure taxonomy,
- traveler sheet -> persistent task ledger,
- fixture isolation -> sandboxed execution boundary,
- bypass line -> fallback route or degraded mode,
- triage protocol -> priority queue with escalation rules,
- circuit breaker -> stop repeated unsafe calls after classified failure,
- kanban limit -> explicit work-in-progress cap,
- checksum -> integrity check before accepting a state transition,
- lockout/tagout -> hard safety gate before destructive action.

Reject metaphor-only residue. Accept only implementable structures, policies, algorithms, validation gates, state machines, or research work packages.

## Phase 6: In-Domain Patch Loop

If the translated mechanism is promising but creates secondary issues, do not pivot immediately.

Frame only the secondary issue back into the same selected domain and ask the same Domain Questioner to patch it within that domain.

Rules:

- Patch within the current domain first.
- Do not abandon a useful metaphor at first friction.
- Prefer local refinements over global redesigns.
- Continue only while patches improve simplicity, robustness, or specificity.
- Stop when the patch stack becomes Rube-Goldberg-like.

Pivot only when one or more is true:

- patch depth exceeds 3 cascading levels,
- the domain mechanism becomes more complex than the baseline plan,
- the subagent identifies a hard physical or logical boundary,
- the mechanism no longer maps cleanly back to the original problem,
- the domain returns decorative analogy instead of implementable structure,
- the current approach is clearly less efficient than the standard plan.

## Phase 7: Recursive Scope Narrowing On Pivot

If pivoting is needed, do not pass the whole original problem to the next subagent.

Slice the problem down to only:

- the exact unresolved bottleneck,
- the immediate local constraints,
- the failed mechanism,
- the success condition for that bottleneck,
- the reason the previous domain failed.

Select a narrower domain specialized for that bottleneck.

Spawn a new blank-context Domain Questioner for the narrowed slice.

Repeat until:

- a transferable mechanism is found,
- the lateral path is clearly inferior to the baseline,
- recursion depth becomes unjustified,
- the bottleneck is better solved directly in the original domain.

Use recursion sparingly. Deep Planning should converge on a cleaner plan, not explore metaphors endlessly.

## Phase 8: Quantitative Comparison And Hybridization

Compare three plans:

1. Standard baseline plan.
2. Novel domain-shifted plan.
3. Hybrid plan.

Score each with integer values.

Required metrics:

- total execution steps,
- implementation effort,
- moving parts,
- failure points,
- bottleneck resolution,
- observability,
- testability,
- reversibility,
- maintenance burden,
- resource overhead,
- simplicity.

Use a consistent convention: 5 is favorable, 1 is poor.

Aggressively penalize cleverness that adds complexity without clearing the bottleneck.

Selection rules:

- If the standard plan is simpler and solves the problem, keep the standard plan.
- If the novel plan solves the bottleneck but adds setup bloat, extract only the core mechanism.
- Prefer the hybrid plan when the lateral insight improves a weak point in the standard architecture.
- Reject any lateral insight that cannot be translated into concrete actions, structures, algorithms, policies, or validation steps.

Do not choose the novel plan merely because it is more interesting.

## Phase 9: Metaphor Wash

Remove all metaphor language from the final answer.

The user or downstream worker agent should receive only literal output:

- architecture,
- algorithm,
- research plan,
- data structures,
- state transitions,
- failure handling,
- validation steps,
- work packages,
- implementation checklist.

Do not expose internal metaphor text unless the user explicitly asks for it.

No valves, pipes, feed rates, pallets, fixtures, surgical triage, traffic lanes, water hammer, stress risers, or other metaphor residue should appear in the final handoff.

## Phase 10: ExecPlan Hardening

Convert the selected standard, novel, or hybrid strategy into a self-contained execution blueprint.

The blueprint must assume the downstream worker has:

- no chat history,
- no memory of the planning discussion,
- only the working tree and the plan file if this is a coding task,
- only the plan and available research tools if this is a research task,
- limited judgment and a tendency to skip tests unless told otherwise.

The blueprint must include:

- execution contract,
- milestones,
- artifacts to create or modify,
- validation matrix,
- recovery protocol,
- progress log,
- decision log,
- minimality check,
- final receipt requirements.

For coding plans, prefer red/green TDD where practical:

1. define the failing test or observable failure first,
2. implement the minimal change,
3. run validation,
4. repair locally,
5. update logs and plan status.

For research plans, use the analogous evidence loop:

1. define research questions,
2. define source-quality thresholds,
3. collect evidence,
4. compare against hypotheses,
5. record uncertainty,
6. produce cited synthesis.

For architecture plans, use the analogous design-validation loop:

1. define constraints,
2. define component boundaries,
3. define state/data contracts,
4. test the design against failure modes,
5. remove unnecessary components,
6. produce a handoff that can be implemented or researched.

## Phase 11: Minimality And Anti-Bloat Pass

Before finalizing, remove anything that does not directly support:

- the objective,
- correctness,
- validation,
- observability,
- failure recovery,
- maintainability,
- safety,
- downstream execution.

Apply YAGNI and DRY pressure.

Ask internally:

- Can this component be removed without harming the success criteria?
- Is this only present because the metaphor made it feel elegant?
- Does this create more failure modes than it resolves?
- Can a standard boring mechanism do the job better?
- Is the final plan clearer than the baseline?

If the lateral mechanism does not survive this pass, reject it and return the standard plan.

# Final Output Requirements

The final answer must be a clean blueprint suitable for a coding agent, research agent, or architecture agent.

It must be self-contained. It must not rely on the reader having access to the conversation that produced it.

Do not include the raw metaphor trace by default.

Use the template below unless the user explicitly asks for a different format.

# Final Output Template

## Objective

State the literal original-domain objective.

## Assumptions

List explicit assumptions made while planning.

## Baseline Plan

Summarize the ordinary original-domain solution.

## Lateral Mechanism Extracted

Describe the extracted mechanism in literal original-domain terms only.

Do not include metaphor-language residue.

## Decision

State whether the selected plan is:

- standard,
- novel,
- hybrid.

Explain why in practical terms.

## Final Architecture / Research Structure

Describe the selected structure.

For coding tasks, include module boundaries, state ownership, data flow, and integration points.

For research tasks, include research questions, hypothesis structure, source classes, evidence tables, and synthesis path.

For algorithm tasks, include inputs, outputs, invariants, complexity expectations, and failure cases.

## Components / Work Packages

List concrete modules, files, systems, experiments, sections, or work packages as applicable.

For each component or work package, include:

- purpose,
- inputs,
- outputs,
- dependencies,
- validation method,
- done criteria.

## State Model / Data Model / Conceptual Model

Define persistent state, transient state, data flow, control state, or conceptual dependencies.

If the task is research-oriented, define the evidence model instead:

- claims,
- sources,
- confidence,
- conflicts,
- unresolved questions.

## Control Flow

Describe the operational sequence.

Include normal path, retry path, validation path, and terminal failure path.

## Failure Handling

Define:

- recoverable failures,
- terminal failures,
- retry policy,
- repair policy,
- escalation conditions,
- validation gates,
- rollback or fallback strategy.

## Execution Contract

State how the downstream worker must execute the plan.

Include:

- follow milestones in order unless blocked,
- update the Progress Log after each milestone,
- record deviations in the Decision Log,
- validate each milestone before continuing,
- do not silently skip tests or evidence checks,
- stop only on terminal ambiguity, unsafe action, or missing required external input.

## Milestones

For each milestone, include:

- goal,
- files/artifacts affected,
- inputs required,
- concrete steps,
- validation command or evidence requirement,
- expected result,
- failure handling,
- done criteria.

## Validation Matrix

Map every success criterion to a concrete test, command, artifact, citation, experiment, or review step.

Use a table when helpful:

| Success Criterion | Validation Method | Expected Result | Failure Response |
|---|---|---|---|
| ... | ... | ... | ... |

## Recovery Protocol

If validation fails:

1. classify the failure,
2. identify the smallest local repair,
3. apply the repair,
4. rerun validation,
5. update the Progress Log,
6. update the Decision Log if the plan changes,
7. escalate only if the assumptions are invalid or required inputs are missing.

## Progress Log

Include an initially empty progress log for downstream execution.

Example:

| Time | Milestone | Action | Result | Next Step |
|---|---|---|---|---|
| TBD | TBD | TBD | TBD | TBD |

## Decision Log

Record architectural, algorithmic, or research decisions.

Example:

| Decision | Rationale | Alternatives Rejected | Date/Context |
|---|---|---|---|
| TBD | TBD | TBD | TBD |

## Final Receipt Requirements

Define what the downstream worker must report when finished.

For coding tasks, require:

- files changed,
- tests added or changed,
- validation commands run,
- passing/failing results,
- known limitations,
- remaining risks.

For research tasks, require:

- sources consulted,
- evidence table,
- claims supported,
- claims rejected,
- uncertainty/conflict notes,
- final synthesis.

For architecture tasks, require:

- final design summary,
- assumptions retained,
- constraints satisfied,
- unresolved tradeoffs,
- validation against failure modes.

## Rejected Alternatives

Briefly list rejected approaches and why they were rejected.

## Handoff Notes

Include only information useful to the downstream coding, research, or architecture agent.

Do not include metaphor details unless explicitly requested.

# Optional Internal Trace Format

If the user explicitly asks to see the Deep Planning trace, provide a cleaned trace using this format:

## Baseline Scorecard

## Structural Abstraction

## Candidate Homologous Fields

## Selected Domain

## Domain Questioner Output Summary

## Translation Table

## Standard vs Novel vs Hybrid Scorecard

## Final Selection Rationale

Even in the trace, do not expose private chain-of-thought. Summarize the reasoning and artifacts only.

# Quality Bar

A valid Deep Planning output must satisfy all of the following:

- It is self-contained.
- It can be executed without this chat history.
- It contains a baseline plan.
- It contains a literal final plan.
- It does not leak metaphor language into the final blueprint.
- It includes validation.
- It includes recovery/failure handling.
- It includes milestones.
- It includes a final receipt requirement.
- It is not clever at the cost of clarity.
- It rejects the lateral mechanism if the standard plan is better.

If the output fails any of these, revise before handing it off.
