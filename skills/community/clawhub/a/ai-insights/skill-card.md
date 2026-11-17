## Description:

AI Insights searches recent AI news, analyzes major events across industry, technology, companies, and policy, and produces a structured Markdown insight report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverland83](https://clawhub.ai/user/neverland83)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to generate concise Chinese-language AI industry reports for a user-selected recent time window. It is intended for tracking major AI news, industry trends, leading company updates, policy changes, and other high-impact events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Web search results can include incomplete, low-quality, outdated, or duplicated AI news.

Mitigation: Review generated reports before relying on them, prefer authoritative sources, preserve source links, and mark uncertain claims clearly.

Risk: The skill writes Markdown reports to a fixed local artifacts directory.

Mitigation: Run it in an expected workspace and review generated files before sharing or committing them.

Risk: Optional cron-based daily push can create recurring searches and reports.

Mitigation: Enable scheduled execution only when recurring report generation is intended and the destination channel is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neverland83/skills/ai-insights)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown report file with a brief text summary and optional cron-style scheduling configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ./artifacts/ai-insights-report/ using timestamped Markdown filenames.]

## Skill Version(s):

1.1.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
