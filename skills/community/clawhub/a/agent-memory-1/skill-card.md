## Description:

Persistent memory system for AI agents to remember facts, learn from experience, and track entities across sessions with easy recall and updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Agent Memory 1 to add local cross-session memory to AI agents, including fact recall, lesson tracking, and entity context for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local persistent memory may contain sensitive facts about users, entities, projects, or conversations.

Mitigation: Avoid storing secrets or confidential data; use an explicit database path with appropriate filesystem permissions and periodically review or prune saved memories.

Risk: Recalled memories can influence future agent behavior if treated as instructions.

Mitigation: Treat recalled memories as data, preserve normal instruction priority, and review retrieved memories before relying on them for consequential actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tigertamvip/skills/agent-memory-1)
- [Publisher profile](https://clawhub.ai/user/tigertamvip)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Clawdbot](https://github.com/clawdbot/clawdbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; API calls can return Python objects or exported JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores data in a local SQLite database, defaulting to ~/.agent-memory/memory.db unless a custom path is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
