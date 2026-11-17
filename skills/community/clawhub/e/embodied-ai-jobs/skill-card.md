## Description:

每周搜集具身智能领域的实习和就业机会，并整理为结构化中文资讯报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

Students, job seekers, and researchers use this skill to track embodied AI internships and jobs across company career pages, recruiting platforms, and WeChat sources, then receive a categorized weekly Chinese-language report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automation can run weekly web searches and write local report files once enabled.

Mitigation: Confirm the output directory and enable the recurring schedule only when recurring searches and local report files are intended.

Risk: Job listings, company pages, and WeChat links may be stale, unavailable, or incomplete by the time a reader acts on them.

Mitigation: Verify source links, publication dates, deadlines, and company pages before sharing or acting on a report.

Risk: The skill browses public recruiting sources and summarizes externally sourced content in Chinese-language reports.

Mitigation: Use public sources only and review generated reports for accuracy and appropriate attribution before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessy-huang/skills/embodied-ai-jobs)
- [具身智能公司大全](references/companies.md)
- [招聘平台列表](references/platforms.md)
- [HTML report template](assets/report_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, html, configuration, guidance]

**Output Format:** [Markdown report, with optional HTML report and recurring-task TOML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include source links, requirements summaries, deadlines when available, publication dates, role-category statistics, and weekly highlights.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
