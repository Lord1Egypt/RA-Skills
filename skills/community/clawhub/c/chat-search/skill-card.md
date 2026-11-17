## Description:

Searches Feishu and Telegram chat history using semantic search with similarity scores and message source labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fhqoopp](https://clawhub.ai/user/fhqoopp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve prior Feishu or Telegram conversations from a configured private chat-history corpus. It is intended for explicit chat-history lookup workflows where message content, source labels, and similarity scores are shown to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Feishu or Telegram messages may be surfaced too broadly because the security evidence flags broad automatic triggers and under-scoped handling of private message content.

Mitigation: Narrow activation to explicit chat-history requests, require confirmation before showing messages, and choose the source or corpus before searching.

Risk: Local search dependencies may expose chat-history data if Qdrant or dependencies are installed with unsafe defaults.

Mitigation: Bind Qdrant to local-only access where possible and pin reviewed Docker and Python dependency versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fhqoopp/skills/chat-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown search results with source labels, timestamps, similarity scores, and optional setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include private chat-message excerpts from Feishu or Telegram search results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
