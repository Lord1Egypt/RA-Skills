## Description:

Track and report OpenClaw context window usage, including token totals, remaining capacity, usage trends, and a breakdown of session, prompt, and reasoning-token contributors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to check how much context window remains in the current session, understand what is consuming tokens, and decide whether a compact or detailed usage report is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local helper reads OpenClaw session metadata and transcript files to calculate token usage.

Mitigation: Install only when local session-file access is acceptable, and review the security summary and source before use.

Risk: Auto-check mode can maintain a persistent local message counter and periodically append context reports.

Mitigation: Keep auto-check disabled unless explicitly requested, and disable it when periodic context reports are no longer needed.

Risk: Some detailed fields are estimates rather than provider-exact counts.

Mitigation: Treat per-file prompt breakdowns, turns remaining, and thinking-token status as estimates; rely on total token usage for context-window fullness.

## Reference(s):

- [Data Sources](references/data-sources.md)
- [Thinking / Reasoning Tokens](references/thinking-tokens.md)
- [Project homepage](https://github.com/99rebels/context-window-tracker)
- [ClawHub skill page](https://clawhub.ai/99rebels/skills/context-window-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Compact text status line or detailed Markdown report with command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include exact provider token totals where available and estimated breakdowns for prompt components, turns remaining, and thinking-token status.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
