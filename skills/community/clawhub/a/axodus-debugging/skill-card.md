## Description:

Diagnose failures using reproduce \u2192 isolate \u2192 fix \u2192 verify workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose failing tests, runtime errors, performance regressions, and unexpected output with a structured reproduce, isolate, fix, and verify workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation trigger metadata may be unreliable, causing the skill to invoke less predictably than intended.

Mitigation: Review trigger metadata before release and invoke the skill explicitly when predictable activation matters.

Risk: Debugging inputs can include logs, traces, environment details, or other sensitive operational data.

Mitigation: Redact secrets and sensitive identifiers before sharing logs, traces, environment variables, or repro details with the agent.

Risk: Debugging guidance or fix proposals could introduce incorrect changes or weaken validation.

Mitigation: Require a stated root cause, minimal changes, regression tests, and verification commands; do not disable tests or checks without explicit approval and justification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mzfshark/skills/axodus-debugging)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown or text with a YAML summary for root_cause, fix, verification, and follow_ups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands, tests, small code changes, diagnostics, and follow-up hardening recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence, skill.yml, and metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
