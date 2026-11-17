## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hailinhmacduc](https://clawhub.ai/user/hailinhmacduc)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and run the gog CLI for common Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth access can expose or modify Gmail, Calendar, Drive, Sheets, Docs, and Contacts data.

Mitigation: Use only the Google services and OAuth scopes needed for the task, and review account configuration before use.

Risk: Commands can send email, create calendar events, update sheets, or clear sheet ranges.

Mitigation: Explicitly review those commands before execution, especially in non-interactive or scripted workflows.

Risk: The skill installs the gog CLI through a Homebrew formula.

Mitigation: Verify the Homebrew formula before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hailinhmacduc/skills/asdasdas)
- [gog CLI homepage](https://gogcli.sh)
- [Installation and use instructions](https://claude.ai/public/artifacts/59bf1058-3a4c-450b-af5b-c85c13cfa8ab)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for Google Workspace services and scripting guidance for JSON output and non-interactive execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
