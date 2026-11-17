## Description:

Automates multi-repo GitHub bounty searches, estimates values, generates fixes through a coding agent, prepares pull requests, and monitors payout progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeysolovyev](https://clawhub.ai/user/sergeysolovyev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bounty hunters use this skill to search GitHub bounty issues, estimate likely payouts, generate candidate fixes, prepare pull requests, and track payout-related follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could use GitHub accounts or repositories beyond the user's intended scope.

Mitigation: Require explicit account, organization, and repository allowlists before search, clone, branch, pull request, or notification actions.

Risk: The skill could open pull requests or post claim notifications without enough user control.

Mitigation: Require user approval before creating pull requests, posting comments, sending notifications, or claiming payouts.

Risk: Temporary clones and coding-agent execution may leave local artifacts or run untrusted project code.

Mitigation: Use isolated temporary workspaces, avoid running untrusted code without approval, and define cleanup for clones, branches, credentials, and generated files.

## Reference(s):

- [CashMachine Bounty Hunter on ClawHub](https://clawhub.ai/sergeysolovyev/skills/cashmachine-bounty-hunter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell commands, pull request text, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include GitHub search plans, bounty analysis, generated fix steps, pull request preparation, and payout-monitoring guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
