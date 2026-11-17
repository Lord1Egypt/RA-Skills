## Description:

Import ChatGPT conversation history into OpenClaw's memory search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to convert exported ChatGPT conversations into local markdown and an OpenClaw-compatible SQLite memory database for searchable archival and retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ChatGPT exports can contain secrets, personal data, business data, or regulated information.

Mitigation: Review or filter conversations before conversion and embedding; avoid importing content that should not be retained or shared.

Risk: Conversation chunks are sent to OpenAI for embeddings.

Mitigation: Use the skill only when that data flow is acceptable for the user or organization, and use a scoped OpenAI API key where possible.

Risk: Converted markdown files and the SQLite memory database store chat contents locally.

Mitigation: Store generated files in controlled locations and manage access, retention, and backups according to the sensitivity of the conversations.

## Reference(s):

- [ChatGPT export guide](references/export-guide.md)
- [ClawHub skill page](https://clawhub.ai/samdickson22/skills/chatgpt-import)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and YAML snippets; supporting scripts create markdown files and a SQLite database.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ChatGPT conversations.json export and an OpenAI API key for embedding.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
