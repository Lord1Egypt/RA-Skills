## Description:

Fast Apple Mail search via SQLite on macOS for finding, listing, and reading local Apple Mail messages by subject, sender, recipient, date, body, thread, or attachment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rhlsthrm](https://clawhub.ai/user/rhlsthrm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on macOS use this skill to search local Apple Mail data quickly, inspect threads and message bodies, and export selected results when normal AppleScript or Spotlight searches are too slow or unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read sensitive Apple Mail metadata and message bodies and can export results.

Mitigation: Use it only for explicit local-mail searches, avoid broad exports unless necessary, and handle generated result files as sensitive data.

Risk: The installable shell script has input-validation concerns around numeric IDs, limits, and dates.

Mitigation: Review the script before installation and validate message IDs, limits, and dates before use.

Risk: Using --no-copy queries the live Apple Mail database while Mail.app may be writing to it.

Mitigation: Keep the default safe-copy behavior unless the operator explicitly accepts live database integrity risk.

## Reference(s):

- [Installation Guide](artifact/references/install.md)
- [ClawHub Skill Page](https://clawhub.ai/rhlsthrm/skills/fruitmail)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires sqlite3, python3, Apple Mail local data, and Full Disk Access for the invoking terminal or shell]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
