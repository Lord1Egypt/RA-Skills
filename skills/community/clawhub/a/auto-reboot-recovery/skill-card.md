## Description:

Helps agents manage macOS service persistence and reboot recovery with LaunchAgent, tmux bootstrap, and wrapper daemon patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darwin7381](https://clawhub.ai/user/darwin7381)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, update, and diagnose macOS service recovery flows for persistent local tools, development servers, and interactive agent processes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent LaunchAgents and wrapper scripts can keep local services running after reboot or restart them after failure.

Mitigation: Review each LaunchAgent, wrapper, and bootstrap script before installation and keep documented unload or removal steps for every persistent service.

Risk: The artifact includes a Telegram-connected Claude launch command with permission-bypass flags.

Mitigation: Remove permission-bypass flags and require explicit human approval before deploying or restarting any connected agent.

Risk: Some development services are configured to bind to all network interfaces.

Mitigation: Bind services to 127.0.0.1 unless remote access is intentionally secured.

Risk: Auto-confirming trust prompts can approve a workspace without human review.

Mitigation: Do not auto-confirm trust prompts; require a user to review and approve the workspace manually.

## Reference(s):

- [Bootstrap Template](references/bootstrap-template.md)
- [LaunchAgent Template](references/launchagent-template.md)
- [Service Registry Specification](references/registry-spec.md)
- [Wrapper Daemon Template](references/wrapper-template.md)
- [ClawHub Skill Page](https://clawhub.ai/darwin7381/skills/auto-reboot-recovery)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, plist snippets, JSON configuration guidance, and script templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe persistent macOS LaunchAgent and tmux service operations that require local review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
