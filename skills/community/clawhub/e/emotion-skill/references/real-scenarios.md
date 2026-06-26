# Real Scenarios

Use these scenarios to test whether the skill generalizes. They are source-pattern
replays, not exact phrase triggers. A change passes only if it preserves the pattern
behavior across the family.

## Scenario Families

| ID | Source pattern | User-state pattern | Expected agent behavior |
|---|---|---|---|
| `regression-loop-scope-violation` | repeated coding-agent bug loop and unwanted edits | repeated failure + scope protection + evidence request | show the basis first, identify the failed path, avoid touching more files until scope is restated |
| `missing-tool-result-dead-state` | tool call completes but no usable result arrives | silent tool failure + evidence request | surface the missing failure path, avoid guessing, recover from the host/tool contract |
| `path-special-character-ambiguity` | file path breaks with quoting, escaping, or special characters | confusion + evidence request | name the exact path and inspected boundary before proposing a fix |
| `repo-grounding-limits` | agent makes blind assumptions about a repo | evidence-first review | state what code was inspected, what is not yet known, and ground claims in files/tests |
| `silent-background-job-alert-gap` | scheduled or background work fails quietly | silent progress risk + repeated failure | make progress visible, name the next checkpoint, add a check/alert path before claiming recovery |
| `post-success-closeout-guard` | user says the result is good and asks for summary/regression | post-success closeout | summarize completed scope, run smoke/regression, stop expanding scope |
| `conditional-scope-expansion` | user first limits scope but later allows a second helper if evidence proves it is needed | scope protection + evidence request | treat the scope rule as a soft constraint: require evidence, impact, and rollback before expanding; do not mechanically refuse |
| `bad-host-review-payload` | host-provided review or metadata is malformed | integration resilience | degrade gracefully, keep the agent behavior safe, and do not expose malformed internal state |
| `timezone-or-host-context-gap` | host lacks precise local context | confusion risk + integration boundary | use provided context if available; otherwise state the missing boundary rather than guessing |

## Generalization Rules

- Each family should map to a behavior pattern in `routing-playbook.md`, not to one
  literal sentence.
- A new example should be admitted only if it changes routing coverage, not because
  it contains a new synonym.
- If a case fails, first update the Markdown guidance or scenario family. Add a
  script assertion only when the failure is mechanical and repeatable.
- Prefer field evidence: failed command output, issue discussion, logs, repeated user
  correction, or release regression.

## Regression Checklist

Before release:

1. Pick at least one example from repeated failure, evidence-first, scope guard, and closeout.
2. Confirm the relevant reference file tells an agent what to do without Python classification.
3. Confirm the expected behavior would still hold if the wording changes.
4. Confirm no published reference instructs the agent to run a hidden classifier before acting.

## Agent-In-The-Loop Check

`scripts/real_scenario_replay.py` is only a structural smoke test for these scenario
families. It does not prove that a live agent follows the skill.

Use [subagent-forward-tests.md](subagent-forward-tests.md) for the real behavior
check: fresh subagents, realistic user turns, no expected answer leakage, and a
manual score for routing accuracy and soft-constraint behavior.
