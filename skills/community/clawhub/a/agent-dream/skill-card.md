## Description:

Agent Dream helps OpenClaw agents consolidate local session activity into long-term memory, prune stale entries with safeguards, and produce self-reflection notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahaaiclub](https://clawhub.ai/user/ahaaiclub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to schedule memory consolidation, maintain concise memory indexes, classify important memories, and review an agent's recent behavior. The skill is intended for local workspaces with agent memory files and session transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script may auto-select the wrong local workspace, agent ID, or session transcript path.

Mitigation: Review the generated dream-config.json before the first scheduled run and confirm workspace, agentId, and sessionsPath match the intended agent.

Risk: Scheduled dream runs may process sensitive local session transcripts and write consolidated memories.

Mitigation: Enable scheduled runs only after approving the memory rewrite setting and confirming the workspace contains data the agent is allowed to read and summarize.

Risk: Memory updates could remove or rewrite important context incorrectly.

Mitigation: Use the built-in backups, two-pass stale marking, and large-change gates; review MEMORY.md.proposed when changes exceed the configured threshold.

## Reference(s):

- [Agent Dream on ClawHub](https://clawhub.ai/ahaaiclub/skills/agent-dream)
- [Memory Types - Classification Guide](references/memory-types.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local configuration or memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local dream records, memory updates or proposed updates, setup configuration, and completion notifications.]

## Skill Version(s):

1.0.6 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
