## Description:

Remote control aria2 via JSON-RPC to add magnet, HTTP, and FTP downloads, check progress, pause or resume tasks, remove tasks, and batch-add links from text for a configured remote aria2 service rather than a local aria2c CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiastia](https://clawhub.ai/user/aiastia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage a configured remote aria2 download service, including adding links, reviewing progress, and controlling downloads by GID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The aria2 RPC token grants control over the configured download queue and could be exposed if the configuration file is not protected.

Mitigation: Use an HTTPS aria2 RPC endpoint or a trusted local-only endpoint, keep .aria2-config.json out of version control, and restrict file permissions.

Risk: Remove operations act on the supplied GID without an additional confirmation step.

Mitigation: Confirm the target GID from the task list before requesting removal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiastia/skills/aria2-downloader)
- [Publisher profile](https://clawhub.ai/user/aiastia)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided aria2 JSON-RPC URL and token; reports task status only when requested.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
