## Description:

Manage Things 3 via the `things` CLI on macOS (add/update projects+todos via URL scheme; read/search/list from the local Things database).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent manage Things 3 tasks on macOS: adding or updating todos through the Things URL scheme and reading, listing, or searching inbox, today, upcoming, project, area, and tag data from the local Things database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install path uses mutable third-party code via a Go module at `@latest`.

Mitigation: Install only after reviewing the upstream things3-cli project, and prefer a pinned reviewed version instead of `@latest`.

Risk: Reading the Things database may require broad macOS Full Disk Access for Terminal or Clawdbot.app.

Mitigation: Try a specific `THINGSDB` path before granting broader permissions, and grant Full Disk Access only when the user understands that other commands run through the same app may gain access to protected local data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cs995279497-byte/skills/chen-things-mac)
- [things3-cli project](https://github.com/ossianhempel/things3-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; depends on the `things` CLI and local Things 3 data access]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
