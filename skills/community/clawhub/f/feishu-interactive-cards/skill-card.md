## Description:

Create and send interactive cards to Feishu (Lark) with buttons, forms, polls, and rich UI elements, with long-polling callback handling for user interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leecyang](https://clawhub.ai/user/leecyang)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to send Feishu interactive cards for confirmations, choices, forms, todos, polls, and other user-interaction flows instead of relying on free-form text replies. It is intended for Feishu workspaces connected to OpenClaw Gateway callback handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The callback service reads Feishu and OpenClaw Gateway credentials and forwards interaction payloads to a configured Gateway.

Mitigation: Run it only with trusted workspace configuration, protect Gateway tokens, and verify that the Gateway destination is expected before enabling callback forwarding.

Risk: File-deletion or other destructive callback examples can affect local data if copied without permission checks and path validation.

Mitigation: Require explicit user confirmation, validate and normalize file paths inside the intended workspace, and enforce operation-specific permissions before acting on callback values.

Risk: Custom card templates can create file-handling exposure if template paths are broadened or validation is weakened.

Mitigation: Keep templates in trusted allowlisted directories, accept only JSON card templates, and review any template path handling changes before use with sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leecyang/skills/feishu-interactive-cards)
- [Security Best Practices](references/security-best-practices.md)
- [Gateway Integration](references/gateway-integration.md)
- [Card Design Guide](references/card-design-guide.md)
- [Feishu Card Documentation](https://open.feishu.cn/document/ukTMukTMukTM/uczM3QjL3MzN04yNzcDN)
- [OpenClaw Docs](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples plus JSON card templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Node.js helper scripts that read Feishu and OpenClaw Gateway configuration from local configuration or environment variables.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, CHANGELOG, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
