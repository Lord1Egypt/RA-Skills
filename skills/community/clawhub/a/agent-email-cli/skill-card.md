## Description:

Operate the agent-email CLI to create disposable inboxes, poll for new mail, retrieve full message details, and manage local mailbox profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaddy6](https://clawhub.ai/user/zaddy6)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to create disposable inboxes, poll for incoming email, retrieve message details, and manage local mailbox profiles from a terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to install an unpinned global npm or Bun package when the CLI is missing.

Mitigation: Install only trusted package sources, and prefer pinning or reviewing @zaddy6/agentemail before global installation.

Risk: Mailbox content and local account profiles may expose sensitive information to the agent runtime.

Mitigation: Avoid using the CLI in environments with unrelated sensitive secrets, and do not print, store, or summarize password or token fields.

## Reference(s):

- [Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON field summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Avoids repeating secret values such as mailbox passwords or tokens.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
