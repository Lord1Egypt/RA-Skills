## Description:

Exec Guard classifies proposed shell commands by semantic risk and helps an agent allow low-risk operations while requiring confirmation for system, network, and destructive actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Exec Guard to add semantic command review to agents that can run shell commands. It is intended to let routine read and workspace-write commands proceed while pausing higher-risk actions for explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-approval rules can allow dependency installs, network access, git pushes, or persisted sudo preferences with too little scrutiny.

Mitigation: Review and narrow auto-approval rules before installation, and require confirmation for sudo, package managers, network downloads, and git push unless they are explicitly needed.

Risk: Incorrect command classification can create a false sense of safety around shell execution.

Mitigation: Keep destructive operations confirmation-gated, inspect proposed commands before execution, and test the policy in a limited workspace first.

Risk: Persisted security preferences can carry broad approvals across sessions.

Mitigation: Audit stored preferences regularly and remove broad approvals after the task that required them is complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wavmson/skills/cmd-guard)
- [Publisher profile](https://clawhub.ai/user/wavmson)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command risk levels, confirmation prompts, and safer alternatives before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
