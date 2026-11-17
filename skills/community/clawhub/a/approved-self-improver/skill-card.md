## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can propose user-approved skill and workspace-memory improvements across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to record corrections, command failures, knowledge gaps, feature requests, and recurring workflow improvements. It helps an agent prepare approval-gated improvement proposals and optional hook reminders for OpenClaw and compatible coding-agent environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted guidance can influence future agent behavior.

Mitigation: Keep entries concise and redacted, and review proposed changes before promoting them into agent instruction or workspace memory files.

Risk: Auto-update authorization can allow skill changes based on weak local approval records.

Mitigation: Keep auto-update disabled by default and require explicit user approval with diffs before skill or agent-instruction-file changes.

Risk: Global hooks or cross-session sharing can expose context in untrusted workspaces.

Mitigation: Use project-scoped opt-in hooks, avoid global hooks, and do not use transcript or messaging features unless the workspace is trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/skills/approved-self-improver)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file templates, hook code, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning logs, improvement proposals, optional hook reminders, and skill scaffold commands; no API calls are required by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
