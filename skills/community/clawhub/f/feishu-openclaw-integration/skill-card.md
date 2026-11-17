## Description:

Integrates Feishu with OpenClaw so teams can configure enterprise AI assistants for group chat, customer support, and automated workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and enterprise automation teams use this skill to connect Feishu bots to OpenClaw for chat assistants, customer support, scheduled notifications, file processing, and message analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forwarding Feishu messages, files, or chat history to OpenClaw may expose sensitive enterprise data.

Mitigation: Use only a trusted private OpenClaw endpoint over HTTPS, avoid forwarding sensitive files or full chat histories without authorization, and restrict Feishu scopes to the minimum needed.

Risk: Feishu app credentials and verification tokens are required for setup.

Mitigation: Store secrets outside versioned configuration files and manage FEISHU_APP_ID and FEISHU_APP_SECRET through the runtime environment or a secrets manager.

Risk: The Node.js SDK path installs npm dependencies for the integration.

Mitigation: Pin and review npm dependencies before production deployment.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/feishu-openclaw-integration)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, JSON, YAML, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, npm, FEISHU_APP_ID, and FEISHU_APP_SECRET for the documented integration paths.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
