## Description:

Helps plan multi-stage work with task dependencies, shared budgets, acceptance checkpoints, and a read-only check of which tasks are ready next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

People managing multi-stage research and delivery use this skill to track dependencies, accepted work, budget commitments, and blocked actions without repeating uncertain external operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A suggested ready task could be mistaken for permission to perform an external action.

Mitigation: Review the plan and obtain explicit authorization before sending, publishing, paying, or otherwise acting externally.

Risk: Retrying an uncertain external action could duplicate a payment, message, or publication.

Mitigation: Check the external outcome and receipt first; do not retry an uncertain write automatically.

Risk: Task inputs could expose sensitive account data.

Mitigation: Keep passwords, tokens, and private account exports out of plans and task inputs.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-kortix-flowith-orchestration)
- [Acceptance scenarios](references/acceptance.md)
- [Example task plan](examples/plan.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON]

**Output Format:** [Markdown planning guidance and JSON readiness checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Readiness and merge status are planning checks, not execution authorization or verification of external evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
