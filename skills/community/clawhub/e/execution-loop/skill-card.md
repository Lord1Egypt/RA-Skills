## Description:

Controls agent execution loops by preventing premature stops, detecting incomplete or speculative completion, re-anchoring long sessions, and guiding headless execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add Stop-hook controls for long or complex agent tasks so the agent keeps working until completion criteria, safety valves, or cancellation conditions allow it to stop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stop-hook state and file handling can let local or repository-controlled content steer the agent or trigger command execution.

Mitigation: Enable the skill only by deliberate opt-in, validate session IDs, sanitize checklist text, and restrict verifier tools and paths before broad use.

Risk: Persistent session state can remain available longer than intended.

Mitigation: Set restrictive permissions on session state and document cleanup and retention expectations.

Risk: Loop-control hooks can continue execution longer than intended if guardrails are incomplete.

Mitigation: Hard-cap iterations and preserve cancellation, stale-state, authentication-error, and other stop safety valves.

Risk: Timestamp parsing issues can weaken stale-state or cancel-signal checks.

Mitigation: Fix and test timestamp parsing before enabling the hooks broadly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/execution-loop)
- [Ralph persistent loop](references/ralph.md)
- [Doubt Gate](references/doubt-gate.md)
- [Task completion verifier](references/task-completion.md)
- [Drift re-anchoring](references/drift-reanchor.md)
- [Headless execution control](references/headless-config.md)
- [Adaptive complexity scoring](references/adaptive-complexity.md)
- [Cancel signal with TTL](references/cancel-ttl.md)
- [Iteration-aware messaging](references/iteration-aware-messaging.md)
- [Extended execution-loop patterns](references/extended-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, JSON hook responses, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create session state files and task checklists when scripts are enabled.]

## Skill Version(s):

2.4.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
