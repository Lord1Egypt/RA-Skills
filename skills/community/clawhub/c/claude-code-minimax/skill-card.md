## Description:

Guides developers through configuring Claude Code to use the MiniMax-M2.5 model through MiniMax's Anthropic-compatible API endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1-m1ng](https://clawhub.ai/user/l1-m1ng)

### License/Terms of Use:


## Use Case:

Developers who use Claude Code can use this skill as a setup guide for routing Claude Code and its VS Code integration to MiniMax-M2.5. It covers configuration paths, model and environment settings, startup commands, common workflows, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisted MiniMax API keys in Claude or VS Code configuration can be exposed through shared files, logs, screenshots, or support output.

Mitigation: Use a credential manager or short-lived environment variable when possible, avoid pasting real keys into shell commands, and redact configuration before sharing logs or files.

Risk: Troubleshooting commands that print or delete Claude configuration can expose secrets or remove working agent settings.

Mitigation: Back up configuration before changing it, review commands before running them, and avoid printing full Claude settings files when credentials may be present.

Risk: The guide recommends a third-party configuration switcher.

Mitigation: Verify the installer source and release version before installing or updating cc-switch.

## Reference(s):

- [MiniMax Platform](https://platform.minimaxi.com)
- [Claude Code Documentation](https://docs.claude.com)
- [cc-switch GitHub Repository](https://github.com/farion1231/cc-switch)
- [ClawHub Skill Page](https://clawhub.ai/l1-m1ng/skills/claude-code-minimax)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guide with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, command examples, configuration snippets, usage scenarios, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
