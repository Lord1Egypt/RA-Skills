## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snilpmud](https://clawhub.ai/user/snilpmud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare Google Workspace CLI setup and command guidance for Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party CLI that may change behavior across releases.

Mitigation: Verify the gog CLI source and release provenance before installation, and pin or review the installed version in managed environments.

Risk: Google OAuth authorization can expose broad account data and allow changes across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

Mitigation: Authorize only the Google services needed for the task and prefer a dedicated low-privilege account where possible.

Risk: Commands can send email, create events, or modify and clear cloud-hosted data.

Mitigation: Require explicit user confirmation before write or destructive operations.

## Reference(s):

- [cs-gog on ClawHub](https://clawhub.ai/snilpmud/skills/cs-gog)
- [snilpmud publisher profile](https://clawhub.ai/user/snilpmud)
- [gog CLI homepage](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local gog CLI and Google OAuth setup; agents should seek explicit confirmation before sending email, creating events, or changing cloud data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
