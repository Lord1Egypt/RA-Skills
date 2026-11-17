## Description:

Configures Codex CLI inside ArkClaw/OpenClaw sandboxes with AgentPlan, Coding Plan, Kimi, DeepSeek, Ark v3, or custom OpenAI-compatible providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bao2200220](https://clawhub.ai/user/bao2200220)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using ArkClaw or OpenClaw use this skill to install, configure, switch, and troubleshoot Codex CLI model-provider profiles without manually editing Codex settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently modifies shell startup and live Codex configuration.

Mitigation: Review planned configuration changes before installation, keep backups of existing Codex settings, and test in an isolated sandbox first.

Risk: Provider API keys are stored in plaintext in user-local shell and Codex configuration files.

Mitigation: Use disposable or tightly scoped API keys, rotate keys after testing, and avoid sharing the workspace or shell history.

Risk: Future Codex traffic may be routed through selected or custom third-party endpoints.

Mitigation: Use only trusted providers and avoid untrusted custom base URLs.

Risk: The authoritative security scan reports unsafe command-injection paths.

Mitigation: Do not run the setup scripts on sensitive systems until the shell-escaping and eval issues are fixed.

## Reference(s):

- [Routing Flow](references/routing-flow.md)
- [Third-Party Provider Configuration](references/thirdparty-providers.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/bao2200220/skills/codex-allinone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated TOML configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May install packages, update shell startup configuration, write Codex profile files, and run local relay setup commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
