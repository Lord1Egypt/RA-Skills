## Description:

圖書館管家 Plus：ISBN 多源掃描 + 借還追蹤與到期提醒 + Notion 同步 + 書庫統計與匯出。基於 bookshelf skill 強化，整合 Open Library + Google Books 查 ISBN，新增借出到期日管理與逾期提醒、批量入庫、閱讀進度追蹤、書庫健康報告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuan905](https://clawhub.ai/user/xuan905)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage a personal or small-library book database, including ISBN lookup, barcode-assisted entry, Notion synchronization, lending due dates, overdue checks, reading progress, reports, and exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a Notion integration with access to the user's library database.

Mitigation: Use a dedicated Notion integration shared only with the intended library database.

Risk: Notion tokens included in cron messages or shell commands can be retained in shell history or logs.

Mitigation: Use environment variables or a secrets mechanism for tokens, avoid embedding real tokens in cron payloads, and rotate any token already exposed.

Risk: Title-based updates may target the wrong page when multiple books have similar names.

Mitigation: Verify the matched record before updates or use database-scoped page IDs for sensitive changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuan905/skills/bookshelf-plus)
- [README](artifact/README.md)
- [Notion integrations](https://www.notion.so/my-integrations)
- [Open Library Books API endpoint](https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data)
- [Google Books volumes endpoint](https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn})

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell command examples; scripts can emit text, JSON, CSV, Markdown, and HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-supplied Notion credentials and database IDs, optional local reading-log files, and optional cron schedules for reminders.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
