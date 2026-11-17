## Description:

AgenticMail provides email, SMS, persistent storage, and multi-agent coordination tools for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ope-olatunji](https://clawhub.ai/user/ope-olatunji)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to let AI agents send, receive, search, and manage email and SMS, coordinate tasks with other agents, and store persistent agent data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad authority over mail, SMS, storage, account administration, Docker setup, credentials, persistence, and external communications.

Mitigation: Install only when those capabilities are intended, review setup and Docker Compose sources before execution, and require confirmation before sending external messages or deleting mail, accounts, domains, or stored data.

Risk: Master keys and generated configuration files can enable administrative actions if exposed or overused.

Mitigation: Prefer least-privilege agent keys, avoid using a master key for routine agent operations, and protect generated configuration files.

Risk: Runtime package setup can change behavior if dependencies are not pinned.

Mitigation: Pin npm and MCP packages before deployment and review updates before applying them.

## Reference(s):

- [AgenticMail Configuration](references/configuration.md)
- [AgenticMail API Reference](references/api-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/ope-olatunji/skills/agenticmail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown with inline commands, JSON configuration, and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce operational actions for mail, SMS, storage, account administration, and agent coordination.]

## Skill Version(s):

0.5.50 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
