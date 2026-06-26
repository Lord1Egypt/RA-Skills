## Description: <br>
Guides agents through diagnosing acpx bridge timeouts and configuring OpenClaw Feishu multi-account setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger0808](https://clawhub.ai/user/roger0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to troubleshoot acpx and OpenClaw ACP bridge failures, verify gateway token setup, repair local acpx configuration, update acpx, and configure Feishu accounts without direct JSON edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gateway tokens, Feishu app secrets, or diagnostic output could expose credentials. <br>
Mitigation: Use placeholder secrets, restrict token-file permissions, protect Feishu credentials, and avoid sharing diagnostic output. <br>
Risk: Repair scripts and guidance can overwrite local acpx or OpenClaw configuration. <br>
Mitigation: Back up ~/.acpx/config.json and ~/.openclaw files before applying changes. <br>
Risk: Restarting Gateway or globally updating acpx can interrupt active work. <br>
Mitigation: Confirm the maintenance window and impact before running gateway restarts or npm global updates. <br>


## Reference(s): <br>
- [ACP Protocol Troubleshooting Reference](references/acp-协议故障排查.md) <br>
- [acpx Configuration Reference](references/acpx-配置参考.md) <br>
- [OpenClaw Feishu Multi-Account Configuration Reference](references/openclaw-飞书多账户配置.md) <br>
- [OpenClaw ACP CLI Documentation](https://docs.openclaw.ai/cli/acp) <br>
- [OpenClaw GitHub Repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file edits, package updates, diagnostic commands, and service restarts that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
