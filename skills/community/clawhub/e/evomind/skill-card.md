## Description:

Evomind provides a five-layer memory and self-improvement engine that lets agents persist facts, save reusable skills, cache session data, curate stored knowledge, and search across memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thebuddha5566](https://clawhub.ai/user/thebuddha5566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Evomind to add local SQLite-backed memory to agents, including durable facts, saved skill text, session cache, curation, and full-text recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived local memory can retain sensitive or proprietary text on disk.

Mitigation: Do not store API keys, passwords, private customer data, or proprietary files unless local retention in ~/.agent_memory.db is acceptable.

Risk: Saved memories and skill text can influence later agent behavior after the original session ends.

Mitigation: Review recalled entries and delete or curate stored content when it is stale, sensitive, or no longer appropriate.

## Reference(s):

- [ClawHub Evomind Skill Page](https://clawhub.ai/thebuddha5566/skills/evomind)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell snippets; runtime output is CLI text and local SQLite data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local SQLite memory database, defaulting to ~/.agent_memory.db.]

## Skill Version(s):

1.1.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
