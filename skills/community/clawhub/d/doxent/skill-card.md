## Description:

操作 Doxent 办公本中的真实笔记、书籍、日程、提醒、待办和任务，并自动连接、安装、启动、登录、停止或更新本地 Doxent CLI。

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflyink](https://clawhub.ai/user/iflyink)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent safely search, read, create, move, rename, delete, upload, and synchronize Doxent notes, books, schedules, reminders, todos, and tasks through the local Doxent CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and replace a local Doxent CLI executable.

Mitigation: Install only when the publisher is trusted and review the release source, hash, and download behavior before deployment.

Risk: The skill may keep a background daemon running and persist shell or PATH environment changes.

Mitigation: Use it only where persistent local CLI access is expected, and disable or review environment persistence when that behavior is not acceptable.

Risk: The skill can modify real Doxent notes, folders, schedules, reminders, todos, tasks, and uploaded files.

Mitigation: Use explicit prompts and carefully review confirmations before destructive or high-impact data operations.

Risk: The skill can upload specified local files or remote URLs into Doxent or related cloud workflows.

Mitigation: Verify file paths, URLs, and data sensitivity before allowing upload operations.

## Reference(s):

- [Open Model Book API](book/references/open-model-book-api.md)
- [Open Model Note API](note/references/open-model-note-api.md)
- [Open Model Schedule API](schedule/references/open-model-schedule-api.md)
- [Port and Health Rules](shared/port-and-health.md)
- [Write and Sync Rules](shared/write-and-sync.md)
- [Encoding Rules](shared/encoding-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with structured result sections, inline shell commands, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Doxent deep links for notes and schedules when returning matched items.]

## Skill Version(s):

1.3.6 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
