## Description:

飞书云盘 AI 管家 helps agents organize Feishu Drive files and folders through classification, search, bulk file management, storage reports, and comment management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[young-joey](https://clawhub.ai/user/young-joey)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and teams with Feishu Drive content use this skill to organize cloud files, find stale or misplaced documents, produce storage summaries, and manage file comments through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Feishu Drive content through bulk moves, folder creation, comment posting, and soft deletion.

Mitigation: Use explicit folder names, review affected file lists, and require confirmation before approving destructive or bulk actions.

Risk: Automated organization may move files into an unexpected folder structure if the user request is ambiguous.

Mitigation: Ask for clarification when folder scope or classification rules are unclear, and present the proposed plan before moving files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/young-joey/skills/feishu-drive-organizer)
- [飞书云盘操作参考](artifact/references/drive-tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or conversational text with Feishu Drive action proposals and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file lists, folder plans, storage summaries, comment actions, and confirmation prompts before bulk or destructive operations.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
