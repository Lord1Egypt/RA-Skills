## Description:

Deploy and manage AI agents (OpenClaw, Claude Code) as first-class participants in a self-hosted Buzz workspace via ACP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darrenjrobinson](https://clawhub.ai/user/darrenjrobinson)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to connect OpenClaw or Claude Code agents to a self-hosted Buzz workspace, with setup guidance for relay services, agent identities, ACP routing, and message posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on agent services use credentials and private keys.

Mitigation: Run relay and agent services under dedicated Unix users and keep environment files outside repositories with mode 0600.

Risk: Prompt or message previews may be persisted in system logs.

Mitigation: Remove prompt and message body logging before deployment.

Risk: Agent traffic depends on the configured OpenClaw endpoint and setup commands.

Mitigation: Restrict OPENCLAW_URL to a trusted endpoint and inspect remote installers or sudo systemd commands before running them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/darrenjrobinson/skills/buzz-acp)
- [Source Homepage](https://github.com/darrenjrobinson/buzz-acp)
- [Buzz Project](https://github.com/block/buzz)
- [OpenClaw](https://openclaw.ai)
- [Claude Agent SDK](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk)
- [Architecture](docs/architecture.md)
- [Troubleshooting](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, deployment, and troubleshooting guidance for self-hosted Buzz relay and agent services.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
