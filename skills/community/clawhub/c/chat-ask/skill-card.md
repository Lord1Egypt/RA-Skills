## Description:

Chat and ask functionality for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xander-art](https://clawhub.ai/user/xander-art)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Chat Ask to run simple local OpenClaw chat, question-answering, and chat-history workflows that return structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat input can be echoed in generated responses and local stderr logs.

Mitigation: Do not send secrets, credentials, or sensitive business data through this skill unless that handling is acceptable.

Risk: The chat history feature is basic and non-durable.

Mitigation: Treat history output as session-only context rather than a persistent conversation archive.

Risk: Responses are simple local tool outputs and may be incomplete or misleading for real user questions.

Mitigation: Review answers before relying on them for decisions or customer-facing use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON objects containing chat responses, Q&A answers, or chat history data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes status, timestamp, tool name, and tool-specific fields; chat history is in-memory for the current session.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
