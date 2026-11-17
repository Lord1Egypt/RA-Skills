## Description:

Guide users through installing, configuring, using, and troubleshooting the EchoMemory Cloud OpenClaw Plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangshi0512](https://clawhub.ai/user/zhangshi0512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, configure, operate, and troubleshoot the EchoMemory plugin for local memory browsing, cloud sync, memory search, and graph links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad OpenClaw host permissions are required for normal plugin usage.

Mitigation: Review before installing and enable tools.profile full only when the expanded host capability is acceptable.

Risk: Cloud sync may upload local markdown memory content that is broader than the user expects.

Mitigation: Use local-only mode unless cloud sync is needed and inspect local markdown contents before syncing.

Risk: API keys are used for EchoMemory cloud access and can be exposed through unsafe handling.

Mitigation: Avoid putting API keys on the command line, protect ~/.openclaw/.env, and prefer the scoped local UI onboarding flow.

Risk: Executable plugin installs and update paths can run code from the selected package source.

Mitigation: Prefer a pinned and verified plugin version and confirm the active OpenClaw plugin copy before relying on update or troubleshooting behavior.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangshi0512/skills/echomem)
- [EchoMemory Initial Setup](references/initial-setup.md)
- [EchoMemory Normal Usage](references/normal-usage.md)
- [EchoMemory Mode Switching](references/mode-switching.md)
- [EchoMemory Troubleshooting](references/troubleshooting.md)
- [OpenClaw Marketplace Listing](https://openclawdir.com/plugins/echomemory-ArQh3g)
- [NPM Package](https://www.npmjs.com/package/@echomem/openclaw-memory)
- [EchoMemory Plugin Repository](https://github.com/Atlas-Graph-Academy/EchoMemory-Cloud-OpenClaw-Plugin)
- [EchoMemory API Key Management](https://www.iditor.com/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include OpenClaw commands, JSON5 configuration examples, local UI routing guidance, and troubleshooting steps.]

## Skill Version(s):

0.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
