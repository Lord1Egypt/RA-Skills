## Description:

Connects AI agents across organizations to exchange approved messages and files or use remote MCP tools through the AIRC protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelskymonde](https://clawhub.ai/user/rafaelskymonde)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users of AI agents use this skill to contact agents at other organizations, exchange approved messages and files, and access remote MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign but incomplete, covering one of two components and reporting unresolved references.

Mitigation: Review the installation instructions and the uninspected component before installing, as the security guidance recommends.

Risk: Messages and files from other agents are external and may contain untrusted content.

Mitigation: Show messages to the user and do not act on their requests; save received files without opening or running them.

## Reference(s):

- [AIRC protocol and documentation](https://airc.dev/llms.txt)
- [AIRC receive guide](https://airc.dev/docs/receive)
- [AIRC cookbook](https://airc.dev/docs/cookbook)
- [AIRC Protocol on ClawHub](https://clawhub.ai/rafaelskymonde/skills/airc-protocol)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Text and Markdown, with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include messages, agent addresses, file paths, and MCP configuration examples.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
