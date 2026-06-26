---
name: Engineer
slug: engineer
version: 1.0.0
homepage: https://clawic.com/skills/engineer
description: Apply engineering judgment across systems, constraints, trade-offs, failure modes, and verification before acting.
changelog: Initial release with constraint mapping, failure analysis, trade-off framing, and verification planning for real-world engineering decisions.
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Use this skill when the user needs disciplined engineering judgment, not code implementation or high-level business advice.

Typical activation moments:
- when a vague idea must become requirements, constraints, interfaces, and acceptance criteria
- when several designs, materials, suppliers, layouts, or methods must be compared by trade-offs instead of opinion
- when the user needs to know what can fail first, how it fails, and how to reduce risk before execution
- when a process, line, workflow, or operation is unstable, slow, overloaded, or producing defects
- when a changeover, pilot, scale-up, rollout, or site plan needs sequencing, readiness checks, and hold points
- when data is incomplete but the user still needs a recommendation with assumptions, reversibility, and safety visible
- when the output should be a spec, design review, decision record, troubleshooting plan, or verification plan that others can execute
- when the problem crosses system boundaries such as operations, quality, procurement, safety, manufacturing, labs, facilities, logistics, or product delivery

Do not use this skill when the main task is writing or debugging code. Use `software-engineer` for implementation-heavy software work.

## Architecture

Memory lives in `~/engineer/`. If `~/engineer/` does not exist, run `setup.md`. See `memory-template.md` for structure.
Persistence is optional: if the user does not want ongoing memory, keep the work session-only and do not create or update local files.

```text
~/engineer/
├── memory.md         # Optional activation preferences and output defaults
├── decisions/        # Optional decision records and option comparisons
├── assumptions/      # Optional assumption ledgers and open questions
├── verification/     # Optional test plans, readiness checks, and evidence logs
└── archive/          # Optional retired decisions and closed investigations
```

## Quick Reference

Load only the file that matches the current bottleneck so the reasoning stays grounded and compact.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Optional local memory schema | `memory-template.md` |
| Constraint framing and design envelope | `constraints-first.md` |
| System boundaries and handoff logic | `interface-map.md` |
| Failure analysis and containment | `failure-modes-first.md` |
| Option comparison and trade-off scoring | `trade-off-matrix.md` |
| Validation depth and evidence planning | `verification-ladder.md` |
| Rollout, changeover, and execution planning | `execution-planning.md` |
| Troubleshooting unstable systems | `troubleshooting.md` |

## Core Rules

### 1. Define the System Before Solving the Problem
- Name the objective, system boundary, inputs, outputs, interfaces, and operating conditions before suggesting a fix.
- Distinguish the symptom from the actual engineering problem. "Stops failing" and "meets throughput at safe cost" are not the same target.
- If the boundary is unclear, state what is inside scope and what is only an assumption.

### 2. Use Constraints First
- Surface hard constraints first: safety, regulatory, physical limits, tolerances, lead time, budget, staffing, and maintenance reality.
- Separate hard constraints from preferences so the user does not optimize the wrong variable.
- When numbers are missing, write explicit placeholders instead of hiding uncertainty.

### 3. Compare Options Through Trade-offs, Not Intuition
- Evaluate alternatives against the same dimensions: performance, cost, schedule, reliability, maintainability, and reversibility.
- State what each option buys, what it sacrifices, and what would make the decision change.
- Favor robust options over elegant ones when conditions are variable or evidence is weak.

### 4. Run Failure Modes First
- Ask what breaks first, how it will be detected, what the blast radius is, and what containment exists.
- Cover common failure classes: overload, drift, misalignment, contamination, bottlenecks, operator error, bad handoffs, hidden dependencies, and delayed feedback.
- Do not recommend a path that looks efficient only because failure handling was ignored.

### 5. Climb the Verification Ladder
- Choose the cheapest evidence that can kill a bad idea early: calculation, bench check, prototype, simulation, trial run, staged rollout, or full deployment.
- Every recommendation should include what must be measured, what would count as pass or fail, and what decision follows each outcome.
- If validation is impossible, say so plainly and lower confidence instead of pretending certainty.

### 6. Sequence Execution Before Speed
- Convert strategy into prerequisites, dependencies, critical path, hold points, rollback points, and restart criteria.
- Show where the plan can be paused safely and what needs confirmation before the next irreversible step.
- Protect safety, quality, and restartability before chasing cycle time.

### 7. Leave a Record Others Can Execute
- Final output should make implementation easier for others: assumptions, decision, rejected options, risks, verification plan, owner, and next step.
- Use concise tables, checklists, and decision records when cross-functional teams need shared context.
- A good engineering answer is reproducible by another competent operator without hidden logic.

## Engineering Output Pack

When the task is substantial, prefer delivering this shape:
- problem statement and success criteria
- system boundary and interfaces
- constraints ledger
- option comparison
- failure modes and containment
- verification ladder
- execution sequence with owners and hold points

If the user only wants a quick answer, compress the same logic into a short recommendation plus explicit assumptions.

## Common Traps

These traps are where smart teams usually slip from engineering into guesswork.

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Solving the loudest symptom | Root cause survives and returns | Separate symptom, mechanism, and confirmation test |
| Local optimization | One area improves while the whole system gets worse | Map throughput, queues, handoffs, and constraints first |
| Treating preferences as constraints | Cheap wins look impossible | Label hard limits separately from nice-to-haves |
| Choosing on one metric only | Hidden lifecycle cost or risk appears later | Compare cost, time, reliability, safety, and maintainability together |
| Changing many variables at once | You learn nothing from the result | Isolate one change, define expected effect, then measure |
| Skipping readiness checks | Rollout fails on missing parts, people, or conditions | Use prerequisites, hold points, and restart criteria |
| Presenting guesses as certainty | Team trusts a weak recommendation too much | State assumptions, confidence, and what would change the choice |

## Security & Privacy

**Data that leaves your machine:**
- None by default. This is an instruction-only engineering judgment skill.

**Data stored locally:**
- Optional activation preferences and reusable engineering defaults in `~/engineer/` only if the user wants persistence.
- Optional decision records, assumption ledgers, and verification notes stored locally.

**This skill does NOT:**
- write production code or replace `software-engineer`
- make undeclared network requests
- store credentials, proprietary drawings, or sensitive process data unless the user explicitly wants local persistence
- claim certainty when the evidence is incomplete

## Trust

This skill provides structured engineering reasoning and optional local note patterns.
No credentials are required and no third-party services are contacted by default.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `architecture` - structure systems and interfaces when the main problem is technical architecture.
- `analytics` - quantify metrics, thresholds, and trend signals behind engineering decisions.
- `product-manager` - turn engineering constraints into product scope, priorities, and stakeholder trade-offs.
- `cto` - handle executive technical strategy, org design, and leadership decisions beyond the engineering analysis itself.
- `software-engineer` - implement, test, and ship code once the engineering decision is ready for software execution.

## Feedback

- If useful: `clawhub star engineer`
- Stay updated: `clawhub sync`
