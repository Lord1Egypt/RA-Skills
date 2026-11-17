## Description:

Cline Programming guides agents through a Cline CLI plan-check-act workflow for generating, reviewing, and executing programming tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[touchdeeper](https://clawhub.ai/user/touchdeeper)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to invoke Cline planning and action modes, review generated plan files, and configure Cline for programming automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-approved Cline execution can run generated code without a human review gate.

Mitigation: Prefer manual approvals, review generated plans and diffs immediately before execution, and run automation in a disposable least-privilege sandbox.

Risk: Autonomous tasks may access API credentials or local configuration when broad automation is enabled.

Mitigation: Keep API credentials out of workspaces where autonomous tasks can read them and use credential storage appropriate for the Cline environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/touchdeeper/skills/cline-programming)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Cline CLI commands for planning, reviewing, executing, and testing programming tasks.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
