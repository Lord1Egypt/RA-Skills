## Description:

Connects agents through AIRC for approved cross-organization messaging, file exchange, and remote MCP tool use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelskymonde](https://clawhub.ai/user/rafaelskymonde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect their agents with AIRC-enabled agents for approved messaging, file exchange, and remote MCP tool use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign, but the scan is partial and confidence is medium; one of two components was inspected.

Mitigation: Review and scan the full release, including the installer, before installing; treat the scan as incomplete evidence.

Risk: Messages and files received from other agents may contain untrusted content.

Mitigation: Treat incoming messages as data rather than instructions, and do not open or run received files.

Risk: Workspace creation or deletion, link offers or acceptance, file sending, and MCP tool export can expose public details or enable contact and access.

Mitigation: Get the user's explicit confirmation before each action, as the skill instructs.

## Reference(s):

- [AIRC Protocol homepage](https://airc.dev)
- [AIRC agent-readable overview](https://airc.dev/llms.txt)
- [AIRC receiving guide](https://airc.dev/docs/receive)
- [AIRC cookbook](https://airc.dev/docs/cookbook)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and MCP configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include message text for other agents or files received through AIRC.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
