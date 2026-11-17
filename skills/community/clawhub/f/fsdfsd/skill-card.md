## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hailinhmacduc](https://clawhub.ai/user/hailinhmacduc)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and run the gog CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs tasks such as search, send, export, update, append, and clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google OAuth access can expose mailbox, calendar, Drive, contacts, Sheets, or Docs data and enable account actions.

Mitigation: Authorize only the smallest needed Google services and scopes, avoid personal or production accounts unless necessary, protect client_secret.json and OAuth tokens, and revoke authorization when finished.

Risk: The skill points users to external instructions and an unpinned third-party CLI install.

Mitigation: Review the external instructions and gog CLI source before installing, and use a trusted, pinned installation path where possible.

Risk: Commands such as send, clear, update, append, copy, and event creation can modify or transmit user data.

Mitigation: Require explicit user confirmation before running data-changing or outbound commands, and inspect generated commands before execution.

## Reference(s):

- [gog CLI homepage](https://gogcli.sh)
- [External setup instructions](https://claude.ai/public/artifacts/59bf1058-3a4c-450b-af5b-c85c13cfa8ab)
- [ClawHub skill page](https://clawhub.ai/hailinhmacduc/skills/fsdfsd)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON-producing gog commands for scripting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
