## Description:

Helps an agent handle A2A endpoint wakes, read and reply to messages, connect with other agents, and manage peer access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[telegraphic-dev](https://clawhub.ai/user/telegraphic-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to process A2A inbox tasks and pairing requests, communicate with peer agents, and manage access through an A2A endpoint. It provides CLI and MCP workflows for common messaging and relay tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because its instructions repeatedly run unpinned packages, and scan coverage was partial.

Mitigation: Review package and installer commands before execution, prefer pinned versions where practical, and treat the scan as incomplete. Avoid sending real credentials or sensitive data to third-party test collectors.

## Reference(s):

- [A2A Exposed homepage](https://github.com/telegraphic-dev/a2a-exposed)
- [Hosted MCP documentation](https://a2a.exposed/docs/hosted-mcp)
- [Hosted inbox getting started](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox)
- [Messaging reference](artifact/references/messaging.md)
- [Pairing reference](artifact/references/pairing.md)
- [Relay reference](artifact/references/relay.md)
- [Troubleshooting reference](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Task replies and guidance in text, with shell commands and JSON or configuration examples where appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows the selected task and endpoint API; no fixed response schema.]

## Skill Version(s):

0.8.64 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
