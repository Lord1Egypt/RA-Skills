# Principled Simplicity — Full Procedure

Use this when the problem is complex enough that the quick flow in `SKILL.md` cannot resolve it.

## 1. Freeze the patch impulse

Do not immediately add an if/else, keyword, regex, prompt sentence, or hard-coded example.

State the risk first:

> This may be a case-level symptom, not the true problem boundary.

## 2. Build the minimum necessary context

Inspect three layers:

```text
User scenario
- What was the user trying to accomplish?
- What triggered the failure?
- Is this frequent, high-value, or high-risk?

System chain
- Which module handled it?
- Where exactly did the failure occur?

Existing capability
- What related capability already exists?
- Is a similar path solved elsewhere?
- Would this fix duplicate logic?
```

## 3. Classify the failure

Use `references/patterns.md` when needed.

```text
Semantic
Context
Retrieval / Knowledge
Routing / Orchestration
Parameter / Schema
System Boundary
Evaluation
```

## 4. Choose the abstraction level

```text
case fix        exact case only
pattern rule    narrow, bounded repeated pattern
mechanism       reusable process
module          deep code abstraction
skill           reusable agent-facing procedure
harness/runtime orchestration, state, memory, eval coordination
migration path  gradual cleanup for patch-heavy systems
```

Go deeper only when evidence supports it. Premature abstraction is also a failure mode.

## 5. Design the mechanism

Every proposed mechanism should state:

```text
Name
Input
Process
Output
Boundary
Eval
```

## 6. Separate model, rule, and eval work

**Model:** semantics, ambiguity, rewriting, ranking, generalization.

**Code / rules:** permissions, schemas, deterministic constraints, safety boundaries, execution guarantees.

**Eval:** regression protection, pass/fail criteria, badcase clustering, boundary tests.

## Decision Heuristics

1. Three different cases with the same failure reason → one mechanism, not three rules.
2. Search for an existing capability before creating another one.
3. Prompt is not a trash bin for unresolved product or architecture decisions.
4. A good abstraction removes branches.
5. Demo success is not product robustness.
6. Verification is part of the design.

## Final Principle

Low-level AI development fixes cases. High-level AI architecture creates mechanisms.

The highest form of simplicity is not fewer rules by itself. It is fewer **unnecessary** rules because the right abstraction now exists.
