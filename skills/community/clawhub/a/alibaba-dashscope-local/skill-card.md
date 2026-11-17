## Description:

Configure OpenClaw to use Alibaba Cloud Bailian provider (Pay-As-You-Go or Coding Plan) through a strict interactive flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[papabearclaw](https://clawhub.ai/user/papabearclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add, switch, or repair Alibaba Cloud Bailian model provider settings for OpenClaw. It guides plan and site selection, validates the DashScope API key, backs up existing configuration, and writes OpenClaw-compatible provider defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow handles real paid Alibaba Cloud API keys and may expose secrets if users pass keys on the command line or store them inline.

Mitigation: Prefer an environment variable or secret manager, avoid passing keys with --api-key, and avoid inline storage unless plaintext local-file risk is accepted.

Risk: Configuration files and backups may contain sensitive provider settings or inline API keys.

Mitigation: Check config and backup file permissions, avoid sharing generated files, and rotate any key written to shared config, backup, shell history, or logs.

## Reference(s):

- [OpenClaw Alibaba Cloud Bailian Configuration](references/openclaw_alibaba_cloud.md)
- [Alibaba Cloud Model Setup on ClawHub](https://clawhub.ai/papabearclaw/skills/alibaba-dashscope-local)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run a Python setup script that validates credentials, creates backups, and updates local OpenClaw JSON configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
