## Description:

Manages Dida365/TickTick tasks, including viewing projects, creating and completing tasks, checking completion history, and syncing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superowenx](https://clawhub.ai/user/superowenx)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an agent to manage Dida365/TickTick projects and tasks through the dida365 CLI. Typical tasks include listing projects, creating tasks, completing tasks, reviewing completed items, and syncing task data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation of the dida365 CLI can introduce supply-chain or local environment risk if the package source or version is not trusted.

Mitigation: Review the package before installing and use a pinned, trusted CLI version where possible.

Risk: Dida365 cookies, client IDs, and client secrets can be exposed through shell history, wrapper scripts, logs, backups, or repositories.

Mitigation: Avoid placing real cookies or OAuth secrets directly in commands or scripts, check where the CLI stores credentials, and rotate or revoke exposed credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/superowenx/skills/dida365-ticktick-agent)
- [Dida365 Web App](https://dida365.com)
- [Dida365 Developer Platform](https://developer.dida365.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include credential-handling guidance for Dida365 cookies, client IDs, and client secrets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
