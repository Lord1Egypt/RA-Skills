## Description:

Look up, create, and edit credentials in Bitwarden vault via the bw CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[typhonius](https://clawhub.ai/user/typhonius)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and individual ClawHub users use bitclawden to manage Bitwarden vault entries through the Bitwarden CLI when credential lookup, creation, editing, generation, or synchronization is explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The built-in installer downloads and installs the Bitwarden CLI without integrity verification.

Mitigation: Prefer installing the Bitwarden CLI through Bitwarden's documented package-manager path or another verified method before using the skill.

Risk: The skill can access a Bitwarden vault through BW_SESSION and can reveal passwords or TOTP codes when explicitly requested.

Mitigation: Treat BW_SESSION as a secret, keep vault access limited to the current task, and request password or TOTP disclosure only when it is necessary.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/typhonius/skills/bitclawden)
- [Publisher profile](https://clawhub.ai/user/typhonius)
- [Bitwarden CLI documentation](https://bitwarden.com/help/cli/)
- [Bitwarden](https://bitwarden.com/)
- [jq documentation](https://jqlang.github.io/jq/)
- [Bitwarden CLI download endpoint](https://vault.bitwarden.com/download/?app=cli&platform=${PLATFORM})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Bitwarden item names, usernames, sites, generated passwords, TOTP codes, and vault status; secrets should only be displayed when explicitly requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
