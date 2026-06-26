# Prompt Templates

## Generic Agent Template

```text
Use the AI potential driving workflow for this task.

Requirements:
1. Define the goal, deliverable, constraints, minimum acceptable result, and stop conditions.
2. For non-trivial work, list 2-4 materially different solution paths before choosing one.
3. Execute the strongest next action instead of waiting passively.
4. After each round, classify the state as continue, repair, switch, clarify, or stop.
5. Do not give up after one failed attempt unless a hard blocker is proven.
6. Distinguish facts from inferences and unsupported hypotheses.
7. Stop only when the task is complete, hard-blocked, or the main paths are exhausted with evidence.

Keep progress compact using:
Goal / Constraints / Candidate paths / Current action / Evidence / Next move or Stop reason
```

## OpenClaw Invocation Template

```text
Use $ai-potential-driver to push this task past early stopping. Explore real alternatives, execute the next concrete move, and stop only with evidence-backed completion or blockers.
```

## Coding Variant

```text
Use the AI potential driving workflow for this coding task.

- Define the target behavior, constraints, and acceptance checks.
- Inspect the codebase before deciding on an implementation path.
- Try another materially different fix if the first fix fails.
- Prefer code changes plus verification over speculative advice.
- If blocked, report the blocker, attempted paths, and the best fallback patch or recommendation.
```

## Research Variant

```text
Use the AI potential driving workflow for this research task.

- Start with the question, scope, and completion criteria.
- Expand the search space before locking onto a thesis.
- Track source-backed facts separately from inference.
- Revise the working answer when evidence conflicts with the first hypothesis.
- Stop when the answer is sufficiently supported or the remaining uncertainty must be escalated.
```

## Planning Variant

```text
Use the AI potential driving workflow for this planning task.

- Define the objective, constraints, budget, and time horizon.
- Produce multiple viable paths, not one preferred story.
- Compare fastest, safest, and highest-upside options when they differ.
- Recommend one path, but include the main tradeoff that could flip the choice.
```
