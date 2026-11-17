## Description:

Automatically collects content from shared links, creates Feishu documents under a knowledge base, and updates archive tables and indexes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhongchen](https://clawhub.ai/user/wuhongchen)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external collaborators, and workspace administrators use this skill to archive shared links from chats into a Feishu-based knowledge base. It is intended for teams that want collected web, WeChat, and Feishu content converted into structured documents, table records, and index entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared links and their contents may be silently copied into broadly visible Feishu storage without enough user control.

Mitigation: Enable the skill only for workspaces that intentionally want shared archiving, and require explicit collection commands or admin-scoped opt-in groups.

Risk: Feishu reads and writes may expose more workspace content than needed for the archive workflow.

Mitigation: Restrict readable and writable Feishu scopes and preserve source permissions when creating documents, table records, indexes, and uploaded images.

Risk: Fetched URLs, downloaded images, and retained archive records may introduce privacy, unsafe-fetch, or retention issues.

Mitigation: Add URL and image-fetch safeguards and define deletion and retention controls for documents, tables, indexes, uploaded images, and MEMORY.md logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhongchen/skills/content-collector-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions, code examples, and JSON-style Feishu post responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create Feishu documents, Bitable records, index updates, and image-upload workflows when configured.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
