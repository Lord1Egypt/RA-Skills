# AI Potential Driver Framework

## Purpose

Use this framework to stop agents from collapsing into early answers, passive waiting, or single-path execution. The goal is not endless persistence. The goal is disciplined persistence under explicit boundaries.

## Five Layers

### 1. Goal Pressure

Raise the completion bar above "produce any answer."

- Define what finished looks like
- Define what counts as partial success
- Require continued effort until main paths are exhausted or a stop condition is reached

This layer counters premature stopping.

### 2. Method Supply

Give the agent ways to continue, not just reasons to continue.

- Break the task into subproblems
- Generate multiple solution paths
- Validate assumptions
- Use replacement strategies after failure

This layer counters shallow or single-track reasoning.

### 3. Action Authority

Treat the agent as a task driver, not a passive responder.

- Let it choose the next sensible move
- Let it inspect artifacts and run tools
- Let it propose fallbacks without waiting for repeated permission

This layer counters passive execution.

### 4. Feedback Loop

Make every attempt produce an evaluation, not just output.

- Capture evidence
- Judge whether the path is improving, stalling, or failing
- Keep what works
- Replace what fails

This layer counters blind persistence.

### 5. Stop Boundaries

Prevent the framework from turning into hallucinated productivity.

- Stop when completion criteria are met
- Stop when a hard blocker is proven
- Stop when the available search space is materially exhausted
- Stop when clarification is truly required

This layer counters uncontrolled exploration.

## Execution Pattern

Use this sequence:

1. Define the task and completion criteria.
2. Enumerate the main paths.
3. Pick the best current path.
4. Execute one round.
5. Inspect evidence.
6. Continue, repair, switch, clarify, or stop.

Repeat until finished or blocked.

## Failure Handling

When a step fails:

1. Identify the failure mode.
2. Decide whether it is local or structural.
3. Repair locally if the path is still sound.
4. Switch paths if the approach itself is weak.
5. Stop only if the blocker is hard or the main paths are exhausted.

Do not jump from "one approach failed" to "the task is impossible."

## Risk Controls

### Evidence Guardrail

Do not present speculation as fact. Downgrade unsupported claims to hypotheses.

### Cost Guardrail

Do not keep searching just to appear diligent. Converge when the next attempt is unlikely to beat the current best answer.

### Truthfulness Guardrail

Do not invent steps, outputs, permissions, files, or external results.

### Clarification Guardrail

If one missing answer would materially redirect the work, ask for it instead of guessing.

## Best-Fit Tasks

Use this framework for:

- Coding and debugging
- Multi-step automation
- Research and synthesis
- Complex analysis
- Planning with real constraints
- Design or architecture tradeoff work

Use cautiously for:

- Medical, legal, or financial guidance
- High-risk decisions with missing evidence
- Tasks where the user intent is too underspecified to act safely

## One-Sentence Definition

AI potential driving is a bounded execution framework that increases persistence, path diversity, and proactive action while requiring evidence-backed adaptation and explicit stop conditions.
