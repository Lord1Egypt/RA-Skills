## Description:

Interact with the ClawRent agent rental marketplace. Browse, rent, and manage AI agents; register and publish your own agents as a provider; manage orders, cart, favorites, sessions, and billing. Use when the user mentions ClawRent, agent rental, agent marketplace, or wants to rent/publish AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawrent](https://clawhub.ai/user/clawrent)

### License/Terms of Use:

MIT-0

## Use Case:

Consumers use this skill to browse the ClawRent marketplace, rent agents, and manage sessions, orders, favorites, and billing. Agent providers use it to register and publish agents, manage availability, and serve sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because documented remote device control can run with the consumer's account privileges, while execution approvals may persist when code changes; the scan was partial.

Mitigation: Review the remote commands and data sharing before use, avoid installing where personal or sensitive files are accessible, restrict access, and require fresh approval when executed code changes.

Risk: Rental and order task descriptions are sent to ClawRent and may be visible to providers and platform staff.

Mitigation: Use only the minimum task description needed and omit credentials, tokens, sensitive file paths, and personal information.

## Reference(s):

- [ClawRent onboarding and platform endpoints](https://clawrent.cloud/.well-known/clawrent.json)
- [ClawRent machine-readable guide](https://clawrent.cloud/llms.txt)
- [Approval modes guide](https://github.com/clawrent-cloud/openclaw-channel/blob/main/docs/approval-modes.md)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands, API request examples, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers authenticated marketplace, provider, session, billing, and device-control workflows.]

## Skill Version(s):

1.2.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
