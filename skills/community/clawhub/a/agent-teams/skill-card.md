## Description:

Interact with Microsoft Teams - send messages, read channels, manage reactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devxoul](https://clawhub.ai/user/devxoul)

### License/Terms of Use:


## Use Case:

Agents, developers, and operators use this skill to inspect Microsoft Teams state, send channel messages, manage reactions, upload files, and run example automation workflows through the agent-teams CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill extracts Teams desktop session cookies and stores a usable token locally.

Mitigation: Review the credential model before installation, keep the local credentials file private, and avoid use on shared or highly sensitive accounts unless that access pattern is approved.

Risk: The skill can act in Microsoft Teams with the authenticated user's permissions.

Mitigation: Use only accounts and teams where automated message sending, file access, reactions, and channel reading are authorized.

Risk: Templates may print or save Teams data such as snapshots and recent messages.

Mitigation: Review generated files and terminal output handling, and avoid storing sensitive message content outside approved locations.

Risk: Install guidance is inconsistent between the metadata package name and some shell template text.

Mitigation: Verify that the intended package is agent-messenger and the intended executable is agent-teams before installing or running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/devxoul/skills/agent-teams)
- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands operate through the agent-teams CLI and may read, write, or summarize Microsoft Teams content according to the authenticated user's permissions.]

## Skill Version(s):

1.10.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
