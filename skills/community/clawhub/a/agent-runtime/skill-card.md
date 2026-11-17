## Description:

Agent Runtime provides an agent runtime system that combines tool registration, permission controls, hook interception, context compression, and usage tracking for agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhmqq616](https://clawhub.ai/user/xhmqq616)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to prototype agent runtime behavior, including tool routing, session usage tracking, and context compaction. It is intended for agent workflows that need runtime scaffolding and integration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime includes local file access and shell command execution while its advertised permission and hook controls are not enforced.

Mitigation: Use only in an isolated sandbox and do not rely on permission labels, hook names, or agent types as access controls.

Risk: Embedding the runtime as a library can expose powerful local execution behavior before the controls are hardened.

Mitigation: Avoid library use until shell access is removed or gated, file access is scoped, hooks fail closed, and the CLI entry point is separated from imports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhmqq616/skills/agent-runtime)
- [Publisher profile](https://clawhub.ai/user/xhmqq616)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command snippets; the runtime CLI may emit plain text and JSON-like status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracks estimated token use, turn count, and context compaction status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
