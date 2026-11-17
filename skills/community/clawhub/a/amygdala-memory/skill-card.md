## Description:

Amygdala Memory gives AI agents persistent emotional state that can influence behavior and responses across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[impkind](https://clawhub.ai/user/impkind)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to maintain, inspect, decay, and visualize an agent's conversation-derived emotional state across OpenClaw sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read recent OpenClaw conversation transcripts and persist emotional inferences and excerpts under the workspace.

Mitigation: Install only in workspaces where transcript processing is acceptable, and review generated memory files such as emotional-signals.jsonl, emotional-state.json, and emotional-log.jsonl.

Risk: Generated emotional state can be auto-loaded into future sessions and influence agent responses.

Mitigation: Review AMYGDALA_STATE.md before relying on auto-injection, and reset or remove generated state when it no longer represents the intended agent behavior.

Risk: Optional cron setup can create recurring background emotional decay and encoding turns.

Mitigation: Avoid --with-cron unless recurring processing is intended; prefer manual runs or the pipeline's no-spawn mode for controlled operation.

Risk: The generated dashboard should be treated as unsafe for untrusted stored content until escaping is fixed.

Mitigation: Use brain-dashboard.html only with trusted local workspace content, and review or sanitize generated dashboard content before opening or sharing it.

## Reference(s):

- [Amygdala Memory ClawHub page](https://clawhub.ai/impkind/skills/amygdala-memory)
- [Publisher profile](https://clawhub.ai/user/impkind)
- [Declared project repository](https://github.com/ImpKind/amygdala-memory)
- [AI Brain series](https://github.com/ImpKind)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown state context, JSON state files, JSONL logs, HTML dashboard, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Bash, jq, and awk on Linux or macOS; optional OpenClaw cron jobs can run emotional decay and encoding.]

## Skill Version(s):

1.7.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
