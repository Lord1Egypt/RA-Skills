## Description: <br>
Troubleshoots acpx bridge connection failures, initialization timeouts, gateway.token issues, Claude Code authentication failures, and ACP channel routing problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roger0808](https://clawhub.ai/user/roger0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose acpx/OpenClaw Gateway bridge failures, verify Claude Code CLI and ACP configuration, restore gateway token files, and test model endpoint or network connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect or propose changes to local credential files such as ~/.openclaw/gateway.token, ~/.openclaw/openclaw.json, and ~/.claude/config.json. <br>
Mitigation: Redact API keys, app secrets, and gateway tokens from all outputs; back up existing files; require manual approval before writing credential files. <br>
Risk: Incorrect troubleshooting commands or endpoint configuration could overwrite a working acpx, OpenClaw Gateway, or Claude Code setup. <br>
Mitigation: Review proposed commands before execution, confirm the target channel and endpoint, and test connectivity with non-destructive status checks first. <br>


## Reference(s): <br>
- [ACP bridge configuration reference](references/acp-bridge-config-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/roger0808/acpx-connection-troubleshooting) <br>
- [Bailian Anthropic-compatible endpoint](https://coding.dashscope.aliyuncs.com/apps/anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed edits to local acpx, OpenClaw Gateway, and Claude Code configuration files; secrets should be redacted before sharing or execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
