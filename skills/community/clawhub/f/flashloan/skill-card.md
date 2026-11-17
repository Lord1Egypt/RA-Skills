## Description:

Flashloan advertises flashloan analysis, but the artifact behaves as a local record manager with status, add, list, search, remove, export, stats, and config commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users may use this skill when they intentionally need a simple local note or data manager. It should not be relied on as flashloan analysis without review because the security evidence identifies a purpose mismatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as flashloan analysis while the artifact implements a persistent local record manager.

Mitigation: Review the behavior before installation and use it only when a local note or data manager is intended.

Risk: The artifact can write, delete, and export local records.

Mitigation: Avoid storing sensitive entries and inspect exported files before opening or sharing them.

Risk: Security guidance identifies unsafe config handling.

Mitigation: Do not pass untrusted values to the config command until input-handling issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/flashloan)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, modify, delete, search, and export local records under the configured FLASHLOAN_DIR data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
