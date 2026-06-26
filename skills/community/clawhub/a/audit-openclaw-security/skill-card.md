## Description: <br>
Audit and harden OpenClaw deployments and interpret `openclaw security audit` findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw deployments they own or have permission to assess, interpret security findings, and plan practical hardening steps for gateway exposure, access policy, tool permissions, plugins, secrets, logs, and deployment platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit folders and reports can reveal host, network, gateway, plugin, skill, and configuration posture. <br>
Mitigation: Review and redact generated outputs before sharing them outside the trusted operating context. <br>
Risk: Running audit or remediation steps against systems without authorization can create security and operational harm. <br>
Mitigation: Use the skill only for OpenClaw deployments the user owns or has explicit permission to assess. <br>
Risk: Configuration edits, fix operations, firewall changes, or restarts can disrupt an OpenClaw deployment. <br>
Mitigation: Create a verified backup and obtain explicit user approval before making changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tristanmanchester/audit-openclaw-security) <br>
- [Command cheat sheet](references/command-cheatsheet.md) <br>
- [OpenClaw audit checks](references/openclaw-audit-checks.md) <br>
- [OpenClaw baseline config](references/openclaw-baseline-config.md) <br>
- [Platform playbook: AWS EC2](references/platform-aws-ec2.md) <br>
- [Platform playbook: Docker](references/platform-docker.md) <br>
- [Platform playbook: Mac mini](references/platform-mac-mini.md) <br>
- [Platform playbook: personal laptop](references/platform-personal-laptop.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with command blocks, findings tables, remediation plans, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local audit folders and reports when the user has shell access; generated diagnostics should be reviewed before sharing.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
