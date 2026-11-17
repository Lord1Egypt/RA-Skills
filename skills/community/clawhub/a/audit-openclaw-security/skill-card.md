## Description:

Audit and harden OpenClaw deployments and interpret `openclaw security audit` findings for gateway exposure, access controls, tool permissions, sandboxing, plugins, secrets, transcripts, logs, and common macOS, laptop, Docker, and EC2 deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a defensive, permissioned audit of an OpenClaw deployment and convert OpenClaw diagnostic output into a practical remediation plan. It supports chat-assisted self-audits and local shell-access audits that produce Markdown security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit folders, reports, and diagnostics may reveal network, firewall, plugin, and OpenClaw security posture details.

Mitigation: Store collector output in a private directory and review the audit folder and report before sharing them externally.

Risk: The bundled redactor is best-effort and may miss credentials, short passwords, tokens, cookies, or API keys.

Mitigation: Manually inspect redacted output and remove any remaining secret or credential values before sharing.

Risk: Remediation guidance can involve configuration edits, restarts, firewall changes, or other operational changes.

Mitigation: Create a verified OpenClaw backup and obtain explicit approval before applying fixes or changing runtime exposure.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tristanmanchester/skills/audit-openclaw-security)
- [Command cheat sheet](references/command-cheatsheet.md)
- [OpenClaw security audit checks](references/openclaw-audit-checks.md)
- [OpenClaw secure baseline config](references/openclaw-baseline-config.md)
- [Platform playbook: Docker / Docker Compose](references/platform-docker.md)
- [Platform playbook: Mac mini or other always-on macOS host](references/platform-mac-mini.md)
- [Platform playbook: Personal laptop](references/platform-personal-laptop.md)
- [Platform playbook: AWS EC2](references/platform-aws-ec2.md)
- [OpenClaw security audit report template](assets/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and concise prose with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local audit artifact folder and a Markdown security report when shell access is available; users should review outputs before sharing.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact metadata reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
