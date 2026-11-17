## Description:

Configures and runs Anthropic Claude Code CLI inside ArkClaw or OpenClaw, with read-only review routing and build-mode execution for coding tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bao2200220](https://clawhub.ai/user/bao2200220)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up Claude Code CLI in ArkClaw or OpenClaw, choose an AgentPlan, Coding Plan, or custom Anthropic-compatible provider, troubleshoot configuration, and delegate code review or implementation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store API keys in the user's home directory and shell startup file.

Mitigation: Use scoped or short-lived keys where possible, avoid long-lived production keys, and rotate any key that was stored in ~/.bashrc.

Risk: Build mode can delegate work to Claude Code with shell and file-write tools.

Mitigation: Use read-only review mode for assessment tasks and inspect proposed changes before allowing build-mode execution in sensitive workspaces.

Risk: The installer can fetch a mutable latest npm package.

Mitigation: Review the package source and lock or pin the installed Claude Code version in controlled environments.

## Reference(s):

- [Provider selection reference](artifact/references/providers.md)
- [Routing flow reference](artifact/references/routing-flow.md)
- [Troubleshooting reference](artifact/references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/bao2200220/skills/claude-code-allinone)
- [Volcengine console](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with shell commands, configuration changes, code edits, and Claude Code output excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run delegated Claude Code tasks with a timeout and retain task logs in the user's home directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
