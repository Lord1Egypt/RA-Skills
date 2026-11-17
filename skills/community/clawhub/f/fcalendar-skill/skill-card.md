## Description:

Fcalendar Skill recognizes Chinese and English time expressions, resolves them to exact calendar dates, and queries Chinese public holidays and normal weekends for a specified date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngfreefjs](https://clawhub.ai/user/youngfreefjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to answer date, schedule, and holiday questions by invoking fcalendar and presenting resolved dates or holiday ranges. It is most relevant for Chinese and English time expressions and Chinese public holiday lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broad shell-based package checks and unpinned PyPI installation for common time mentions.

Mitigation: Review before installing, prefer a pinned and reviewed fcalendar version in a virtual environment, and avoid auto-triggering the skill for casual date or weekday mentions.

## Reference(s):

- [Fcalendar package on PyPI](https://pypi.org/project/fcalendar/)
- [Fcalendar source repository](https://github.com/youngfreefjs/fcalendar)
- [Chinese Holidays and Solar Terms Reference](references/holidays.md)
- [Time Expression Types Reference](references/time-expressions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses derived from single-line JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to preserve fcalendar CLI result semantics and avoid paraphrasing resolved dates or holiday results.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
