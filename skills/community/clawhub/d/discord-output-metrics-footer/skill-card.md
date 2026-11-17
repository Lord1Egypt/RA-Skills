## Description:

Install, configure, maintain, or troubleshoot a compact Discord output footer for OpenClaw that shows live context usage, output tokens, Codex quota remaining, model used, and optional subagent token aggregate under each Discord response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[udaymanish6](https://clawhub.ai/user/udaymanish6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw workspace maintainers use this skill to install and configure a Discord footer that reports runtime token, context, model, and quota metrics without adding prompt tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The extension uses a local OpenAI Codex OAuth token to fetch quota data.

Mitigation: Review before installing, enable only where this credential use is acceptable, and prefer scoped permissions or disabling quota fetching for sensitive environments.

Risk: Subagent token aggregation can mix telemetry from nearby sessions.

Mitigation: Disable subagent aggregation where cross-session telemetry is unacceptable, or replace cache-window matching with exact parent-run matching when supported.

## Reference(s):

- [Implementation](references/implementation.md)
- [ClawHub skill page](https://clawhub.ai/udaymanish6/skills/discord-output-metrics-footer)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration blocks plus a bundled TypeScript extension template.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The footer omits quota information when quota fetching fails and can include a best-effort subagent token aggregate.]

## Skill Version(s):

0.1.0 (source: server release evidence, openclaw.plugin.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
