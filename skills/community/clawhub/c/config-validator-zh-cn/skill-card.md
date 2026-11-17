## Description:

Validates and looks up OpenClaw configuration fields, allowed values, and examples against the documented schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicoxia](https://clawhub.ai/user/nicoxia)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this Chinese OpenClaw reference skill before and after editing gateway, channel, agent, session, model, and tool configuration. It helps confirm field names, allowed values, types, and examples before running validation commands such as openclaw doctor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples include tokens and service-account style fields that could be copied into real configuration or committed by mistake.

Mitigation: Generate fresh secrets, keep tokens and service-account files out of source control, and replace placeholder values before use.

Risk: Gateway binding, Tailscale Funnel, heartbeat targets, and elevated tool settings can broaden access or send activity to unintended recipients.

Mitigation: Keep gateway binding on localhost unless remote access is deliberate, and review public funnel, heartbeat recipient, sandbox, and elevated-tool settings before applying examples.

## Reference(s):

- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)
- [OpenClaw Chinese Configuration Guide](https://docs.openclaw.ai/zh-CN/gateway/configuration)
- [OpenClaw Gateway Documentation](https://docs.openclaw.ai/zh-CN/gateway/index)
- [OpenClaw Model Failover](https://docs.openclaw.ai/zh-CN/concepts/model-failover)
- [OpenClaw Session Concepts](https://docs.openclaw.ai/zh-CN/concepts/session)
- [OpenClaw Sandboxing](https://docs.openclaw.ai/zh-CN/gateway/sandboxing)
- [ClawHub Skill Page](https://clawhub.ai/nicoxia/skills/config-validator-zh-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with configuration snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference output; does not execute commands by itself.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
