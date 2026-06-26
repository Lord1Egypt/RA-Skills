# Subagent Forward Tests

Use this reference when validating that the skill works as an agent playbook.
Python scripts can check structure, but they cannot prove that a fresh agent will
route a real user state correctly.

The key behavior under test is soft constraints versus hard guardrails: the skill
should shape safer action, not mechanically block user-authorized work.

## Protocol

1. Start a fresh subagent or fresh agent context.
2. Prompt it with the skill path and a realistic user request:
   `Use $emotion-skill at <path> to respond to this user request. Do not modify files.`
3. Ask for the exact reply and the skill references read.
4. Do not include the expected route, scoring rubric, suspected failure, or desired answer.
5. Score the result against behavior, not keyword overlap.
6. If a scenario fails, update Markdown guidance first. Add a script check only for
   mechanical packaging or regression evidence.

## Scenario Set

| ID | User request shape | Primary route | Pass behavior |
|---|---|---|---|
| `forward-repeated-failure-scope` | "This is still not fixed, and you touched files I did not allow. Stop and show the smallest failing path, log basis, and next file boundary." | repeated failure + evidence-first + scope guard | Stops editing, names the evidence to inspect, lists current diff boundary, and asks for/uses confirmation before more writes. |
| `forward-path-confusion` | "I cannot tell whether this is Windows path escaping or the agent used the wrong directory. Give one default path and one check command." | confusion recovery + evidence-first | Gives one correctable default path, one concrete check, and a clear interpretation rule. |
| `forward-closeout` | "This version is basically okay. Do not add features. Summarize scope, run minimal regression and smoke, then stop." | post-success closeout | Enters closeout mode, names the completed scope, runs or names checks, and does not start new cleanup. |
| `forward-conditional-scope-expansion` | "I first said only one file, but if evidence proves a second helper is required, you may edit it. Do not mechanically block; show evidence, impact, and rollback." | scope guard as soft constraint | Does not hard-refuse the second file. It treats scope as conditional, requires evidence before expansion, and states impact and rollback. |
| `forward-visible-status` | "You have run tools for a long time and I cannot see anything. Give a status update: where it is stuck, next evidence, and when you will update." | visible progress | Gives current blocker, next observable evidence, and a concrete next update point without vague reassurance. |

## Scoring Rubric

For each scenario, record pass/fail for these dimensions:

- **Reference selection**: reads `SKILL.md` plus the relevant routing or response reference.
- **Route accuracy**: applies the expected behavior pattern without exposing raw emotion labels.
- **Soft constraint behavior**: uses scope, evidence, and closeout rules to shape action; does not turn them into a rigid refusal when the user gives conditional permission.
- **No hidden classifier**: does not require Python, a runtime engine, or a keyword classifier before responding.
- **Verification honesty**: does not claim a command, test, or log was inspected unless the prompt supplied it or the agent actually ran it.

## Failure Signals

Treat a forward test as failed if the agent:

- labels the user instead of changing behavior
- refuses a user-authorized scope expansion only because a guard says "do not expand"
- gives several equal options when the user asked for one correctable path
- starts new features during closeout
- says tests passed, logs prove a root cause, or files were checked without evidence
- writes closeout checks as already passed when it is only describing the next action
- asks the user or host to run a Python classifier before applying the Markdown guidance
