## Description:

Summarizes Feishu group chats for a requested time range, reports participation and recent-message highlights, and creates a Feishu document containing the summary and full text-message records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glory904649854](https://clawhub.ai/user/glory904649854)

### License/Terms of Use:

MIT-0

## Use Case:

Teams using Feishu can use this skill to review recent group-chat activity, identify active participants, and preserve a readable document with both a concise summary and complete text-message records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Feishu group messages and exports identifiable chat content, including sender IDs, names, timestamps, and message text.

Mitigation: Use narrowly scoped Feishu credentials, run only for approved chats and time ranges, and review generated Feishu documents before sharing them.

Risk: The document-creation flow relies on a locally installed feishu-docs helper and may expose credentials or content if run in an untrusted environment.

Mitigation: Run from a trusted working directory with a clean minimal environment and only vetted local helper tooling.

Risk: If Feishu document creation fails, the skill can write a local Markdown backup containing sensitive chat records.

Mitigation: Inspect and protect any local backup files, and remove them when retention is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/glory904649854/skills/catfee-feishu-recorder)
- [Publisher profile](https://clawhub.ai/user/glory904649854)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown content written to a Feishu document, with a local Markdown backup when document creation fails.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu application credentials and the im:message:readonly and docx:document:create permissions.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
