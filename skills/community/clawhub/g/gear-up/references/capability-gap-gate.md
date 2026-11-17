# Capability Gap Gate

Use this reference only when it is unclear whether a new temporary capability is justified.

## A real capability gap has four properties

1. **Material** — failure to close it can change task success, safety, correctness, or effort substantially.
2. **Operational** — the gap concerns what the agent can reliably *do*, not merely what it does not know.
3. **Uncovered** — installed skills, runtime tools, current context, generic operations, and relevant Academy entries do not already solve it adequately.
4. **Testable** — there is an observable condition showing whether the new capability closes the gap.

If any property is missing, prefer not to generate.

## Diagnose before creating

Classify the problem:

| Symptom | Likely response |
|---|---|
| "I do not know the current policy" | `know-enough`, not `gear-up` |
| "I know the method but need to run one SQL query" | existing SQL/data tool |
| "I repeatedly need a domain-specific transformation that generic tools perform inconsistently" | possible temporary tool |
| "I keep losing a task-wide constraint across many steps" | possible temporary context instruction |
| "This task requires a specialized decision procedure not covered by an installed skill" | possible temporary skill |
| "I want a separate agent because the task is large" | not sufficient evidence of a capability gap |

## Reuse search order

Search in this order and stop at the first adequate solution:

1. current instructions and already-loaded skills;
2. installed but not loaded skills/tools;
3. generic runtime operations (filesystem, shell, code, SQL, browser, RAG, etc.);
4. Skill Academy metadata/index;
5. only then generate.

Do not load full Academy artifacts merely to browse them. Search lightweight metadata first.

## Value test

State a before/after test such as:

```text
Before: requirement normalization loses source IDs in >5% of sampled rows.
After: 100% of the validation sample preserves source IDs and normalized text.
```

or:

```text
Before: no available tool can call the required local API.
After: generated tool completes the read-only API request and returns schema-valid output.
```

"The artifact exists" and "the code runs" are not value tests.
