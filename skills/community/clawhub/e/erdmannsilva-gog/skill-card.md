## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erdmannsilva](https://clawhub.ai/user/erdmannsilva)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to operate Google Workspace services from an agent through the gog CLI, including account setup, Gmail, Calendar, Drive, Contacts, Sheets, and Docs workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party gog executable installed through an unpinned Homebrew formula.

Mitigation: Review the gog CLI source and Homebrew tap before installing, and prefer a pinned or otherwise trusted release.

Risk: The skill can guide commands that send email, create calendar items, modify Sheets, or export Drive and Docs data.

Mitigation: Grant only the Google service scopes needed for the intended task and review commands before executing data-changing or data-exporting operations.

## Reference(s):

- [Gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/erdmannsilva/skills/erdmannsilva-gog)
- [ClawHub publisher profile](https://clawhub.ai/user/erdmannsilva)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of an external gog executable and may produce commands that access or modify Google Workspace data.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
