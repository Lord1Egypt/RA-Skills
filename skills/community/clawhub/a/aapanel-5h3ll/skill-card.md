## Description:

aaPanel/BT-Panel server monitoring and file management skill for system resources, site status, service status, SSH logs, cron jobs, log reading, and remote file operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social5h3ll](https://clawhub.ai/user/social5h3ll)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, system administrators, and homelab operators use this skill to monitor and administer one or more aaPanel/BT-Panel servers from OpenClaw. It supports health checks, log review, site and SSL management, database and FTP administration, firewall changes, PHP version switching, and remote file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes broad aaPanel administrative control, including destructive file, site, database, SSL, firewall, FTP, download, unzip, and recursive permission operations.

Mitigation: Install only when that level of administration is intended, and manually confirm destructive operations before running them.

Risk: aaPanel API tokens are required and may be stored in the local OpenClaw configuration file or passed to commands.

Mitigation: Use a dedicated least-privilege aaPanel token when possible, keep the configuration file owner-only, and avoid exposing real tokens or passwords in command-line history or logged environments.

Risk: Disabling TLS verification for self-signed panels can weaken connection security.

Mitigation: Keep TLS verification enabled unless there is a deliberate exception for a trusted self-signed deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/social5h3ll/skills/aapanel-5h3ll)
- [aaPanel GitHub](https://github.com/aaPanel)
- [aaPanel Website](https://www.aapanel.com)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and CLI-oriented text, often with inline shell commands and JSON or table command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read, report, and propose or execute aaPanel administrative operations through local Python scripts.]

## Skill Version(s):

1.0.7 (source: server release metadata, artifact metadata, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
