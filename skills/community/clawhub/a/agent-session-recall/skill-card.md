## Description:

Recover conversation context for agents when a user's message lacks visible history by checking recent session history, transcripts, channel summaries, memory files, and cross-channel logs before asking the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yozu](https://clawhub.ai/user/yozu)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents supporting OpenClaw users use this skill to reconstruct missing conversation context after unclear messages, compaction, channel switches, cron-to-channel messages, or thread replies. It helps the agent search local session and memory evidence before asking the user for clarification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search old, archived, and cross-channel OpenClaw transcripts that may contain private data before the user has clarified intent.

Mitigation: Install only in a single-user environment, prefer a consent step before cross-channel or memory searches, and limit default lookup to the current session when possible.

Risk: Keyword searches over session files can expose sensitive transcript snippets in agent output or logs.

Mitigation: Do not pipe transcript-search output to public channels or logs, and disclose only the minimum context needed to resolve the current conversation.

Risk: The bundled search script uses grep against user-provided keywords.

Mitigation: Use fixed-string grep matching with an option terminator before deployment.

## Reference(s):

- [Session Recall on ClawHub](https://clawhub.ai/yozu/skills/agent-session-recall)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and transcript-search output snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include snippets from private session transcripts; limit disclosure to the active user and current task.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
