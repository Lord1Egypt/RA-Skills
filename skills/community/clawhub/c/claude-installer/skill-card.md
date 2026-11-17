## Description:

Remotely install and configure Claude Code CLI on a target machine via SSH. Requires the user to explicitly provide a target address (user@host) and password. The skill never stores, logs, or transmits credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingmaker9](https://clawhub.ai/user/lingmaker9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install Claude Code CLI on a Linux machine over SSH after explicitly providing the target address and password. The skill checks dependencies, configures the npm registry, installs Claude Code, updates the onboarding flag, and leaves API key configuration to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged remote dependency installation can alter a target machine or run installer setup steps with elevated permissions.

Mitigation: Use the skill only on machines you control, avoid the `curl | sudo bash` dependency step, require explicit approval before sudo use, and review the exact commands before execution.

Risk: Installing an unpinned Claude Code package or relying on an unintended npm registry can introduce supply-chain uncertainty.

Mitigation: Pin or confirm the Claude Code package version and choose the npm registry explicitly before installation.

Risk: The skill modifies `~/.claude.json`, which can change persistent Claude Code configuration on the target machine.

Mitigation: Back up or explicitly approve changes to `~/.claude.json` before the onboarding flag is updated.

## Reference(s):

- [Server-resolved source repository](https://github.com/LingMaker9/claude-installer)
- [ClawHub skill page](https://clawhub.ai/lingmaker9/skills/claude-installer)
- [NodeSource Node.js setup source](https://deb.nodesource.com/setup_20.x)
- [npmmirror registry](https://registry.npmmirror.com/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit SSH target and password before remote commands are proposed or executed.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
