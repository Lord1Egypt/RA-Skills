## Description:

Triage failed automations: separate execution failure from delivery failure, re-verify current state against stale baselines, then decide re-run, new task, or abandon. Produces a verdict, evidence, and an action plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to investigate failed or silent scheduled tasks. It separates work failures from delivery failures, checks current system and plugin state, and recommends whether to complete the work now, schedule a new task, or close it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Interface-switching guidance could be interpreted as retrying an operation after a permission, policy, or approval denial, potentially bypassing approval controls.

Mitigation: Review the interface-switching steps before use and stop when an operation is denied; do not retry a rejected operation through another path.

Risk: The security scan was partial because referenced memory files were missing, leaving persistence behavior incompletely assessed.

Mitigation: Verify that conclusions are recorded in the intended memory location before relying on them or considering external delivery.

## Reference(s):

- [Automation Repair Triage on ClawHub](https://clawhub.ai/zuoyunlai/skills/automation-repair-triage)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown with a failure verdict, supporting evidence, and an action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a concise memory note for the diagnosis and reusable lessons.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
