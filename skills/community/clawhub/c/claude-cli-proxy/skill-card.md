## Description:

Set up a local HTTP proxy that routes OpenClaw model requests through Claude Code CLI using a Team/Max/Pro subscription instead of API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxsorto](https://clawhub.ai/user/maxsorto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure a local Anthropic-compatible proxy that forwards OpenClaw requests to Claude Code CLI through an existing Claude subscription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full OpenClaw prompts, system context, and conversation history are routed through Claude Code and Anthropic using the operator's subscription account.

Mitigation: Install only when that routing is intended, and review what agent context may be sent before enabling the proxy.

Risk: The proxy writes system context to `.ccproxy-system-context.md`, which may persist on disk between requests.

Mitigation: Restrict workspace file permissions and avoid placing the proxy in shared or broadly readable directories.

Risk: Security evidence reports persistent configuration changes and a command-injection risk around session-name handling.

Mitigation: Review and harden the scripts before deployment, especially session-name handling and any global Claude Code settings changes.

## Reference(s):

- [Auto-Start Configuration](references/autostart.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript scripts, shell commands, and JSON or service configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup instructions and local proxy scripts for OpenClaw-to-Claude Code routing.]

## Skill Version(s):

2.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
