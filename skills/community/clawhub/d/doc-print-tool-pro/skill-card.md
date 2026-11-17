## Description:

Enterprise teams use this skill to guide agents through document credential registration, batch discovery, on-chain identity verification, reputation governance, directed task dispatch, dispute handling, subscriptions, security prechecks, and tenant audit workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise operators and developers use this skill to configure and execute tenant-scoped document credential registration, on-chain verification, reputation scoring, directed task routing, dispute workflows, subscriptions, and audit exports. It is intended for teams managing collaborator credentials and trust governance across shared workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tenant credentials, API keys, reputation records, and audit exports may expose sensitive enterprise data.

Mitigation: Use least-privilege API keys, store secrets only in environment variables or files with restrictive permissions, redact sensitive output, and restrict export destinations.

Risk: Bulk registration, import/reset, dispute, webhook, and export workflows can affect many tenant records or business processes.

Mitigation: Require explicit human approval, tenant scoping, and a dry-run or preview before high-impact actions.

Risk: Webhook and shell-command examples may be unsafe if adapted without validation.

Mitigation: Whitelist commands, avoid interpolating untrusted input into shell arguments, validate HTTPS endpoints, and verify webhook signatures before processing events.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doc-print-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and bash or Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured responses may include status, result data, execution logs, and error fields.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
