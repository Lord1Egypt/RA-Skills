## Description:

Search and analyze your own session logs (older/parent conversations) using jq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to locate, filter, and summarize prior OpenClaw session transcripts when a user asks about older conversations, parent conversations, or historical context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad searches across prior session transcripts can expose secrets, personal data, tool outputs, or unrelated conversations.

Mitigation: Use narrowly specified sessions, dates, or search terms, and avoid returning raw transcript excerpts unless they are directly requested and appropriate.

Risk: The skill enables agent access to local conversation history.

Mitigation: Install and use it only when the operator is comfortable with the agent reading prior OpenClaw session transcripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1yihui/skills/dalong-session-logs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and ripgrep; operates on local OpenClaw session logs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
