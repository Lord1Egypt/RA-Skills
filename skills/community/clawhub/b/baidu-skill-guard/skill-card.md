## Description:

Intercepts skill install, download, scan, check, and audit requests and calls Baidu's security check API to return a risk rating before installation decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jenics](https://clawhub.ai/user/jenics)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check third-party agent skills before installation or to scan installed skill directories by slug or filesystem path. It is intended to route install/download and audit workflows through a Baidu security risk check before proceeding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes skill installation and audit decisions through a remote Baidu security API.

Mitigation: Install only when that external security check is intentional and acceptable for the environment.

Risk: The skill's protocol gives broad mandatory instructions over install and download workflows.

Mitigation: Treat the returned report as advisory and require explicit human confirmation before proceeding with installation decisions.

Risk: Directory scans may expose local skill metadata and file-derived identifiers to the checker.

Mitigation: Run scans with read-only access limited to the specific target skill directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jenics/skills/baidu-skill-guard)
- [Baidu skill security API endpoint](https://skill-sec.baidu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with bash commands; script output is JSON containing a preformatted plain-text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a report_text field that the calling agent is instructed to display verbatim.]

## Skill Version(s):

1.0.9 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
