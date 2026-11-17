## Description:

在 Windows/WorkBuddy 沙箱环境下干净卸载并重装 OpenClaw 与 Codex，并在重装后重新接入第三方模型（DeepSeek）而无需 OpenAI 账号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to guide Windows users through OpenClaw and Codex uninstall, reinstall, residue cleanup, WSL gateway reset, and post-install model-provider repair. It is intended for troubleshooting failed installs, broken Codex authentication, and desktop model-selection issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes persistent Codex credential and configuration changes, including auth.json and config.toml edits.

Mitigation: Back up Codex configuration before edits, treat API keys as secrets, prefer limited or disposable provider keys, and review all credential-related file changes.

Risk: The workflow includes irreversible reset actions such as unregistering a WSL distribution and moving profile data.

Mitigation: Require explicit user confirmation before unregistering WSL distributions, deleting or moving profile data, changing global AGENTS.md behavior, or setting up a persistent local proxy.

Risk: The security verdict is suspicious because the guide lacks enough safety boundaries around reset and credential operations.

Mitigation: Use the skill only for deep OpenClaw/Codex reinstall and provider-repair cases, and keep each destructive or persistent action separate from read-only diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junci003/skills/codex-reinstall-windows)
- [OpenClaw Windows Hub release download](https://github.com/openclaw/openclaw-windows-node/releases/latest/download/OpenClawCompanion-Setup-x64.exe)
- [OpenAI Codex issue 19694](https://github.com/openai/codex/issues/19694)
- [DeepSeek models endpoint](https://api.deepseek.com/v1/models)
- [DeepSeek responses endpoint](https://api.deepseek.com/v1/responses)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Markdown]

**Output Format:** [Markdown guidance with bash, PowerShell, TOML, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language troubleshooting instructions for Windows Codex/OpenClaw reinstall and provider recovery workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
