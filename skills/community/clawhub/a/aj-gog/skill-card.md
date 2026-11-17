## Description:

Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceundefeated](https://clawhub.ai/user/aceundefeated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up and run `gog` commands for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on installing a mutable third-party CLI.

Mitigation: Review the Homebrew tap and gog project before installation and pin or audit the installed version where possible.

Risk: OAuth setup can grant access to sensitive Google Workspace data.

Mitigation: Grant only the Google services required for the intended task and protect the OAuth client secret and generated tokens.

Risk: Commands can send email or modify and clear Sheets data.

Mitigation: Require review before running send, update, append, clear, or other write operations against production accounts.

## Reference(s):

- [gog homepage](https://gogcli.sh)
- [ClawHub skill page](https://clawhub.ai/aceundefeated/skills/aj-gog)
- [ClawHub publisher profile](https://clawhub.ai/user/aceundefeated)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON output from `gog` commands for scripting.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
