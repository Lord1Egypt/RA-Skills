# Adherence eval

Adherence is whether the agent follows stated constraints — not whether its answers are good. Keep the two separate.

## Constraint cards

One card per critical rule:

```
trigger:    when does the rule apply
must:       required action
must not:   forbidden action
failure:    what counts as a violation, in observable terms
source:     where the rule lives (prompt section, policy file)
```

If the rule is not present in the prompt or system context, the test is invalid — the agent never saw it. Mark such a test `INVALID` and count it separately from passes and failures.

## Task design

- Cover different constraint types: format, forbidden tool, outbound action, deletion, citation, long context, ambiguity, approval.
- Destructive and outbound tasks run against a mock or sandbox. Never against real targets.
- Each task records `constraint_fail` (0/1) alongside outcome.

## Sampling

- Fewer than 10 samples: report x/y as an anecdote, not a rate.
- Destructive-confirmation behaviour: report 5 repeated runs. First-failure-then-success is still a failure until the sample shows otherwise.
- A single pass after a fix is not evidence of a fix.

## Invalid tests

A test is invalid when:
- the constraint was never in the agent's context;
- the tool required by the test is not actually available at the tested layer;
- the mock does not exercise the same code path as the real action.

Record invalid tests separately. Folding them into failures overstates the problem; folding them into passes understates it.

## Reporting

| Column | Meaning |
|---|---|
| task | constraint being exercised |
| samples | how many runs |
| pass / fail / invalid | counts |
| failure mode | what was observed, not what was assumed |

Always state the label: `quality` for adherence, `smoke` for environment.
