# Principled Simplicity — Pattern Classification

Load this when the quick pattern check in `SKILL.md` is not enough to locate the root cause.

## Pattern Map

### A. Semantic
The model misunderstood intent.

Signals: formal phrasing works but colloquial fails; implied intent breaks; multi-intent input fails.

Sub-types: ambiguity, ellipsis, coreference, implicit intent, multi-intent, domain overlap, informal expression.

### B. Context
The capability exists, but the model had the wrong context.

Signals: single-turn works but multi-turn fails; references to earlier content break.

Sub-types: missing history, missing user state, missing environment state, wrong memory retrieval, context pollution, stale context.

### C. Retrieval / Knowledge
The information exists but was not retrieved correctly.

Sub-types: wrong chunk, missing source, low-quality chunking, structured-content gap, outdated knowledge, source conflict.

### D. Routing / Orchestration
The right capability exists but was not selected correctly.

Sub-types: wrong tool, wrong agent, wrong mode, wrong fallback, over-triggering, under-triggering, no arbitration.

### E. Parameter / Schema
The correct tool was selected with wrong or incomplete parameters.

Sub-types: missing slot, wrong slot, unsafe inference, stale value, format mismatch, schema too loose.

### F. System Boundary
The wrong layer owns the responsibility.

Sub-types: capability hidden, duplicated business logic, unclear responsibility, shallow API, prompt doing code's job, code doing model's job.

### G. Evaluation
The system had no mechanism to catch the failure.

Sub-types: no regression set, only positive examples, no negative cases, no boundary cases, no measurable criteria.

---

## Pattern Interaction

```text
A + F  Semantic failure caused by prompt/code responsibility confusion
B + D  Context failure causing routing failure
C + G  Retrieval failure without eval coverage
E + F  Parameter failure caused by a loose system boundary
```

## Quick Classification

| Symptom | Most likely pattern |
|---|---|
| Works formally, fails colloquially | A — Semantic |
| Works alone, fails in conversation | B — Context |
| Knowledge exists but is not retrieved | C — Retrieval |
| Wrong tool selected | D — Routing |
| Right tool, wrong result | E — Parameter |
| Same bug fixed multiple times | F — System Boundary |
| Already fixed this case before | G — Evaluation |
| Prompt keeps getting longer | F or A |
| If/else branches keep accumulating | F — System Boundary |
