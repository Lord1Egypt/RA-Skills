## Description: <br>
Validates and queries OpenClaw configuration fields and allowed values, provides configuration examples, and helps check configuration against official schema references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill before and after editing OpenClaw gateway configuration to check field names, allowed enum values, value types, and examples against bundled schema references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration examples include tokens, phone numbers, user IDs, or identity-link values that should not be copied into real deployments. <br>
Mitigation: Treat these values as placeholders, generate deployment-specific high-entropy secrets, and replace identity values with approved real identifiers. <br>
Risk: Gateway settings can expose services beyond loopback or enable public access. <br>
Mitigation: Keep gateway binding on loopback unless wider access is required, and review authentication and network restrictions before enabling LAN, tailnet, or public binding. <br>
Risk: The skill is a documentation-only reference, so schema guidance may lag current OpenClaw behavior if upstream configuration docs change. <br>
Mitigation: Compare critical configuration changes against the current OpenClaw documentation and run OpenClaw validation commands before deployment. <br>


## Reference(s): <br>
- [Config Validator on ClawHub](https://clawhub.ai/nicoxia/config-validator-zh-cn) <br>
- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference) <br>
- [OpenClaw Configuration (zh-CN)](https://docs.openclaw.ai/zh-CN/gateway/configuration) <br>
- [OpenClaw Gateway](https://docs.openclaw.ai/zh-CN/gateway/index) <br>
- [OpenClaw Model Failover](https://docs.openclaw.ai/zh-CN/concepts/model-failover) <br>
- [OpenClaw Session Concepts](https://docs.openclaw.ai/zh-CN/concepts/session) <br>
- [OpenClaw Sandboxing](https://docs.openclaw.ai/zh-CN/gateway/sandboxing) <br>
- [Quick Reference](artifact/quick-reference.md) <br>
- [Channels Schema](artifact/schema-channels.md) <br>
- [Agents Schema](artifact/schema-agents.md) <br>
- [Gateway Schema](artifact/schema-gateway.md) <br>
- [Session Schema](artifact/schema-session.md) <br>
- [Tools Schema](artifact/schema-tools.md) <br>
- [Models Schema](artifact/schema-models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with schema tables, configuration examples, and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; examples may include placeholder tokens, identity values, and deployment settings that must be replaced or reviewed before use.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata; artifact package.json and SKILL.md describe 1.0.0/v1.0 content) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
