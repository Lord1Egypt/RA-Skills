## Description:

agentauth requires user-initiated biometric passkey approval before an OpenClaw agent performs sensitive or irreversible actions such as deleting files, sending emails, making purchases, or modifying system configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[braga-agentauth](https://clawhub.ai/user/braga-agentauth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add human-in-the-loop authorization to OpenClaw workflows before high-risk agent actions run. It is intended for actions where explicit passkey-backed approval, notification, and auditability are needed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill becomes a broad local command executor after passkey approval.

Mitigation: Install only in environments where approved commands are still reviewed carefully and limited to the intended OpenClaw workspace.

Risk: Command metadata is sent to AgentAuth-hosted services and notification channels.

Mitigation: Keep display strings concise, avoid unnecessary sensitive details, and rely on the skill's redaction guidance before sending approval requests.

Risk: Credentials are stored in the shared OpenClaw .env file.

Mitigation: Restrict access to the OpenClaw environment file and rotate AgentAuth credentials if the file may have been exposed.

Risk: Cleanup may not fully restore the original policy file byte-for-byte.

Mitigation: Review AGENTS.md manually after cleanup and remove any remaining AgentAuth instruction block if uninstalling.

## Reference(s):

- [AgentAuth Homepage](https://agentauth.id)
- [ClawHub Skill Page](https://clawhub.ai/braga-agentauth/skills/agentauth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses auth-flow, approval-flow, notification, and cleanup commands around OpenClaw actions.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
