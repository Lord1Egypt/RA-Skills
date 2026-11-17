## Description:

Guides developers through troubleshooting acpx bridge timeouts and OpenClaw Feishu multi-account setup, including token files, acpx configuration, version updates, validation commands, and known routing limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roger0808](https://clawhub.ai/user/roger0808)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose OpenClaw/acpx bridge failures, repair local acpx and gateway token configuration, and configure Feishu multi-account routing with the recommended OpenClaw commands. It is especially relevant when connections hang during initialize, WebSocket 1005 errors appear, or bindings do not route as expected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A sample gateway token appears in the skill text and should be treated as exposed.

Mitigation: Do not reuse the shown token; rotate any matching token and store real token files with owner-only permissions.

Risk: Feishu app secrets may be exposed through shell history or process listings when passed as command-line arguments.

Mitigation: Prefer secret-safe input methods where available and redact app secrets from logs, diagnostics, tickets, and shared terminal output.

Risk: Companion scripts can overwrite local acpx configuration and restart OpenClaw gateway services.

Mitigation: Review scripts before execution, back up affected configuration files, and run them only in the intended user environment.

Risk: The guidance recommends a global acpx@latest upgrade, which changes local tooling supply chain state.

Mitigation: Pin or review the acpx version before upgrading when reproducibility or change control is required.

## Reference(s):

- [ACP protocol troubleshooting reference](references/acp-协议故障排查.md)
- [acpx configuration reference](references/acpx-配置参考.md)
- [OpenClaw Feishu multi-account configuration reference](references/openclaw-飞书多账户配置.md)
- [OpenClaw ACP CLI documentation](https://docs.openclaw.ai/cli/acp)
- [OpenClaw GitHub repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference companion shell scripts that inspect or modify local OpenClaw and acpx configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
