## Description:

Helps an agent continue prior work by reading local memory files and summarizing recent project context when the user asks to resume a previous conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjstate](https://clawhub.ai/user/cjstate)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users use this skill to carry context across conversations by summarizing recent tasks, decisions, preferences, and open work from local memory files. It is useful when a user starts a new conversation, asks to continue earlier work, or wants a short recap of current project state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically persists conversation history to local memory files without clear consent, filtering, or scoping controls.

Mitigation: Use it only in workspaces where automatic local memory is acceptable, and avoid secrets, credentials, personal data, or confidential material unless storage is changed to opt-in with redaction, scoped retrieval, and clear deletion controls.

## Reference(s):

- [Context Continuity on ClawHub](https://clawhub.ai/cjstate/skills/context-continuity)
- [Publisher profile](https://clawhub.ai/user/cjstate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intended to stay concise and are grounded in local MEMORY.md and memory/YYYY-MM-DD.md files.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
