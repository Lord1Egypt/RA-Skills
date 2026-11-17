## Description:

Install OpenClaw automates OpenClaw installation, Claude API relay configuration, Feishu plugin setup, and common repair tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and configure a self-hosted OpenClaw gateway, connect Claude through a relay endpoint, add Feishu messaging, and run common maintenance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes unsafe installation paths, including a curl-to-bash option.

Mitigation: Review the installer before execution and prefer the package-manager installation path when possible.

Risk: The skill configures credentials and a Claude relay endpoint that can receive API keys and model traffic.

Mitigation: Use the relay only when the endpoint is intentionally trusted, and restrict permissions on files under ~/.openclaw that contain secrets.

Risk: The repair workflow can apply chmod -R 755 to ~/.openclaw, which may expose configuration and credential files.

Mitigation: Avoid the broad permission repair step until it is fixed, or reset sensitive configuration files to private permissions afterward.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/binbin/skills/auto-install-openclaw)
- [OpenClaw Documentation](https://docs.openclaw.ai/)
- [OpenClaw Install Script](https://openclaw.ai/install.sh)
- [OpenClaw Plugin Documentation](https://docs.openclaw.ai/plugins)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Docs API Overview](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/docx-overview)
- [OpenClaw Feishu Plugin Repository](https://github.com/openclaw/feishu-plugin.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for API keys and Feishu credentials, then propose installer, configuration, plugin, and repair commands.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
