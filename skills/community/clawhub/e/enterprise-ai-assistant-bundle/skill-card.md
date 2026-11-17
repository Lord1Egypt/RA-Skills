## Description:

Enterprise AI Assistant Bundle helps deploy a Feishu-connected OpenClaw assistant for customer service, group chat support, and workflow automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Enterprise developers and IT teams use this skill to configure and run an AI assistant that connects Feishu messages to OpenClaw-backed chat responses and bundled automation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise messages and credentials may be exposed if the Feishu webhook and API secrets are deployed without strong controls.

Mitigation: Use Feishu signature or token validation, store secrets in environment variables or a secret manager, and deploy behind TLS and controlled network ingress.

Risk: Unbounded message handling can increase abuse, cost, or availability risk.

Mitigation: Add rate limits, request size limits, logging appropriate for privacy requirements, and operational monitoring before production use.

Risk: Chat contents are sent to an external model provider.

Mitigation: Provide clear user notice and approval, review data-handling requirements, and restrict sensitive content according to enterprise policy.

Risk: Runtime dependency installation is not pinned.

Mitigation: Pin and review dependencies before installation in enterprise environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/enterprise-ai-assistant-bundle)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)
- [Feishu Open Platform](https://open.feishu.cn)
- [OpenClaw API endpoint](https://api.openclaw.ai/v1)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown documentation with bash commands, Python scripts, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local deployment configuration and assistant skill JSON when the deploy script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
