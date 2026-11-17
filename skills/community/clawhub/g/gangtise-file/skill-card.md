## Description:

Searches the Gangtise file center across reports, announcements, meeting summaries, chief opinions, and investment calendar items, returning file IDs, metadata, summaries, and optional full-file downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtisegts](https://clawhub.ai/user/gangtisegts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analyst agents use this skill to locate, filter, and organize Gangtise research documents and related investment materials by type, date, security, institution, industry, keyword, or other metadata. It is suited for building candidate document lists and optionally downloading selected files for separate review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Gangtise credentials and sends search terms, filters, and file IDs to Gangtise.

Mitigation: Install and run it only when that credentialed Gangtise access and data sharing are intended.

Risk: Download options and local-save settings can write result files to disk.

Mitigation: Leave GTS_SAVE_FILE unset and omit download flags unless local file output is explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gangtisegts/skills/gangtise-file)
- [研究报告调用指导](references/report.md)
- [外资研报调用指导](references/foreign_report.md)
- [公司公告调用指导](references/announcement.md)
- [会议纪要调用指导](references/summary.md)
- [首席观点调用指导](references/opinion.md)
- [投研日程调用指导](references/investment_calendar.md)
- [文件下载](references/get_file.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell command examples, returned file metadata, summaries, and optional downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gangtise credentials; search queries and filters are sent to Gangtise; most result sets are API-limited to 100 items and the docs recommend requesting 10 or fewer in most cases.]

## Skill Version(s):

1.4.12 (source: server release evidence; artifact frontmatter reports 1.4.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
