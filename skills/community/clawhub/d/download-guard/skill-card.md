## Description:

Download Guard helps Windows agents manage download and install commands by checking configured storage paths and disk space, avoiding silent C-drive fallback, logging downloads, and guiding cache scans or migrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nihaoljx](https://clawhub.ai/user/nihaoljx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users on Windows use this skill to make AI-agent initiated downloads, installs, model pulls, and clones more transparent and less likely to fill the system drive. It also helps inspect tool-cache locations and guide cache migration when C-drive usage is risky.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags risky default configuration and recommends review before installation.

Mitigation: Reset config.md to an unconfigured state before first use, then choose and verify the intended download root during setup.

Risk: Cache migration and warning fixes can make persistent npm, pip, yarn, pnpm, uv, PATH, and environment changes.

Mitigation: Review the target path and proposed changes before running migration or fix commands, and keep a backup of existing settings.

Risk: Download logs may display filenames or paths that originated outside the trusted workspace.

Mitigation: Treat log contents as untrusted display data and avoid copying paths or filenames into privileged commands without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nihaoljx/skills/download-guard)
- [README](artifact/README.md)
- [Reference](artifact/reference.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status messages with inline PowerShell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused; requires PowerShell for bundled helper scripts.]

## Skill Version(s):

5.4.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
