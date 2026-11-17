## Description:

Monitor disk space across drives, alert before disks fill up, track usage trends, find space hogs, and suggest cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and system operators use this skill to monitor local disk usage across drives, receive threshold alerts, inspect large directories, and review disk-usage trends for cleanup planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports a local file-overwrite risk in shared temporary directories from the default history file handling.

Mitigation: Configure historyFile to a private user-owned directory and avoid running the skill as root or under a privileged service account until temp-file handling is hardened.

Risk: The security verdict is suspicious even though no external transmission was identified.

Mitigation: Review before installing and run the skill with only the filesystem access needed for disk monitoring.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/theshadowrose/skills/disk-watch)
- [Publisher Profile](https://clawhub.ai/user/theshadowrose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript code examples and formatted disk status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include disk usage summaries, warning and critical alerts, largest-directory listings, trend summaries, and cleanup suggestions.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
