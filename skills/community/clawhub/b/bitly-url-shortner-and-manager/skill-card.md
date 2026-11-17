## Description:

Bitly URL Shortner and Manager for a local Windows OpenClaw workspace. Use when the user wants to log into Bitly with locally stored credentials, validate auth, inspect account/group details, list/search/filter/export existing bitlinks, shorten one or many URLs, inspect long URLs and click metrics, create custom aliases, or prepare short links for X/social posting workflows without exposing secrets inside the published skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Bitly account and link workflows from an agent-guided local CLI. It supports authentication checks, group and link inspection, search and filtering, URL shortening, custom aliases, click metrics, and exports for downstream social posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Bitly access token to read account and link data.

Mitigation: Use only a token intended for agent use, set BITLY_ENV_FILE or explicit shell environment variables, and protect any token file.

Risk: Shorten, bulk-shorten, and create-custom commands can change the connected Bitly account.

Mitigation: Review requested URLs, group GUIDs, domains, and aliases before running account-mutating commands.

Risk: Export commands can write Bitly link data to local files.

Mitigation: Choose output paths deliberately and avoid exposing exported link data outside the intended workspace.

Risk: A legacy bitly-credentials.json file may be used if no access token is set elsewhere.

Mitigation: Review or remove any legacy credential file before use.

## Reference(s):

- [Bitly API notes](references/api-notes.md)
- [Local env example](references/env-example.md)
- [Bitly API v4 base URL](https://api-ssl.bitly.com/v4)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with PowerShell commands; CLI output may be JSON, CSV, TXT, or file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Bitly access token and can write exported link data to local files]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
