## Description:

宝塔面板 helps an AI agent manage aaPanel/BT Panel websites, files, databases, Docker, scheduled tasks, server state, troubleshooting workflows, and secure MCP setup for supported agent clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aapanel](https://clawhub.ai/user/aapanel)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to let an agent inspect, administer, troubleshoot, and deploy aaPanel/BT Panel services while preserving confirmation gates for high-impact server changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer live server resources and may change websites, files, databases, Docker workloads, scheduled tasks, firewall settings, or services.

Mitigation: Use read-only inspection first and require explicit confirmation before write/delete actions, recursive permission changes, service restarts, port changes, software installation, or database diagnostics.

Risk: Administrative credentials, API tokens, private keys, cookies, or database passwords could be exposed through prompts, logs, command arguments, or diagnostic output.

Mitigation: Use secure credential channels where possible, redact secrets in outputs, avoid passwords in shell arguments or temporary files, and reset any password that was provided through a lower-security channel.

Risk: The bundled website troubleshooting workflows may affect live website files or disclose database credentials if used without review.

Mitigation: Review the Chinese troubleshooting instructions before installation and require per-action confirmation for file writes/deletes, service kills/restarts, recursive permission changes, and database checks.

Risk: MCP installation grants ongoing administrative access to a Baota/aaPanel server and depends on network-retrieved official components.

Mitigation: Restrict the MCP allowlist to the minimum client IP or CIDR, verify TLS certificates for non-loopback access, and rely on the bundled helper's pinned SHA-256 check for the primary installer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aapanel/skills/btpanel)
- [Source manifest](references/vendor-sources.md)
- [Baota MCP installation documentation](https://docs.bt.cn/user-guide/ai/mcp-installation#申请可信-ip-证书)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include redacted operational summaries, confirmation prompts, and setup or troubleshooting commands.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
