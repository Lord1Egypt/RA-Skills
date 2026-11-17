## Description:

Persistent semantic memory for AI agents that helps them recall past decisions, store facts and preferences, search conversation history, and maintain context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannydvm](https://clawhub.ai/user/dannydvm)

### License/Terms of Use:


## Use Case:

External developers and agent operators use Engram to give agents local, persistent memory for facts, decisions, preferences, events, relationships, and prior conversation context across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent agent memory can retain sensitive raw transcripts, credentials, health, financial, client, or proprietary data across sessions.

Mitigation: Store only necessary facts, decisions, and preferences; avoid sensitive raw data; review and delete memories when they are no longer needed.

Risk: Broad recall across sessions can surface stale, private, or irrelevant context in later agent work.

Mitigation: Use memory scoping and targeted searches, review recalled memories before relying on them, and prefer a pinned, reviewed npm package version before installation.

## Reference(s):

- [Engram ClawHub skill page](https://clawhub.ai/dannydvm/skills/engram-memory)
- [dannydvm publisher profile](https://clawhub.ai/user/dannydvm)
- [engram-memory npm package](https://www.npmjs.com/package/engram-memory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to use local Engram CLI commands for memory search, storage, ingestion, relationship management, import, and export.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
