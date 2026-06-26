## Description: <br>
Create and send interactive cards to Feishu (Lark) with buttons, forms, polls, and rich UI elements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leecyang](https://clawhub.ai/user/leecyang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to send Feishu interactive cards for confirmations, choices, forms, todo lists, polls, and callback-driven workflows through OpenClaw Gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send Feishu messages and forward card interaction details through OpenClaw Gateway. <br>
Mitigation: Install only for workflows that require Feishu interactive cards, verify Feishu credentials and Gateway token settings, and restrict callback handling for destructive actions. <br>
Risk: Cards and callbacks may include unnecessary personal data or sensitive workflow details. <br>
Mitigation: Keep card content minimal, avoid placing secrets in card payloads, and review callback data before forwarding or storing it. <br>
Risk: The skill guidance encourages cards for broad uncertainty, which can be excessive for routine or sensitive replies. <br>
Mitigation: Use cards for explicit confirmations, choices, forms, polls, and similar user-interaction workflows instead of applying the broad pattern automatically. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leecyang/feishu-interactive-cards) <br>
- [Card Design Guide](references/card-design-guide.md) <br>
- [Gateway Integration Guide](references/gateway-integration.md) <br>
- [Security Best Practices](references/security-best-practices.md) <br>
- [Feishu Card Documentation](https://open.feishu.cn/document/ukTMukTMukTM/uczM3QjL3MzN04yNzcDN) <br>
- [OpenClaw Docs](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON card templates, JavaScript examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu card payloads and callback-handling guidance that rely on configured Feishu app credentials and OpenClaw Gateway settings.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, package.json, CHANGELOG released 2026-02-06) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
