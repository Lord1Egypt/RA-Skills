## Description:

Enables agents to help configure OpenClaw's built-in browser mode, including enable, disable, status, headless, visible, and restore workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoo-unison](https://clawhub.ai/user/yoo-unison)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to toggle OpenClaw browser configuration without manually editing the OpenClaw JSON config. It is useful when agents need browser access for logged-in sites, headless automation, status checks, or restoring prior configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unverified external archive installation guidance in SHARE.md.

Mitigation: Install only from the reviewed ClawHub artifact or a verified maintainer source.

Risk: The restore workflow can replace the active OpenClaw configuration with contents from an arbitrary file path.

Mitigation: Use --restore only with trusted backup files from the OpenClaw backup directory.

Risk: Some documented troubleshooting and uninstall commands use sudo, package installation, or deletion.

Mitigation: Review commands before execution and confirm they target the intended OpenClaw files and system packages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yoo-unison/skills/browser-toggle)
- [README.md](README.md)
- [INSTALL.md](INSTALL.md)
- [SKILL.md](SKILL.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that modify OpenClaw browser configuration and create backups.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
