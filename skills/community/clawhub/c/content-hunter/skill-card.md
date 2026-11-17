## Description:

Content Hunter helps agents scrape trending content from Xiaohongshu, Douyin, and Bilibili, save platform records, and generate scheduled trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[judefluen-coder](https://clawhub.ai/user/judefluen-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to collect hot content from supported short-video platforms, persist per-run Markdown records, and generate trend summaries or scheduled daily reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved scraped content and raw-data links may expose collected platform data beyond the intended audience.

Mitigation: Confirm recipients before sending reports, limit access to generated task folders, and set retention limits for saved data.

Risk: The skill includes a fixed group-sharing rule for reports and raw-data links.

Mitigation: Remove or change the fixed group rule before use and require explicit confirmation before sharing raw-data links.

Risk: Broad scheduled-job cleanup by name matching could delete unrelated cron jobs.

Mitigation: Delete only reviewed, exact scheduled job IDs instead of broad name matches.

Risk: Scraping logged-in or third-party platform pages can collect sensitive or policy-restricted content.

Mitigation: Use authorized accounts, respect platform rules, and review collected records before redistributing summaries or source links.

## Reference(s):

- [Content Hunter ClawHub skill page](https://clawhub.ai/judefluen-coder/skills/content-hunter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown records and reports with occasional shell command and scheduling guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped task folders for scraped platform data and summary reports.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
