## Description:

Interact with Discord servers - send messages, read channels, manage reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:


## Use Case:

Developers, operators, and AI agents use this skill to inspect Discord server state, read and send channel messages, manage reactions, upload files, and automate common Discord workflows through the agent-discord CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can obtain and store a Discord user token that grants access equivalent to the user's Discord account.

Mitigation: Install only for trusted environments, protect the credentials file, and revoke the token by changing the Discord password if exposure is suspected.

Risk: The skill stores Discord credentials in plaintext and may create local memory or snapshot files containing sensitive server context.

Mitigation: Keep credential, memory, and snapshot files out of version control, restrict local file permissions, and delete stored data when it is no longer needed.

Risk: The artifact contains inconsistent install guidance around the agent-discord binary versus the agent-messenger package.

Mitigation: Use the server-resolved package path agent-messenger and verify provenance before installation.

Risk: Granting broad terminal permissions can expand the data available to terminal-launched processes.

Mitigation: Avoid granting Terminal Full Disk Access for this skill unless the access is explicitly required and understood.

## Reference(s):

- [Agent Discord ClawHub Page](https://clawhub.ai/devxoul/skills/agent-discord)
- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally return JSON by default, with optional human-readable pretty output.]

## Skill Version(s):

1.10.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
