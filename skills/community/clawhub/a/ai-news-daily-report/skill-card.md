## Description:

Daily report generation with timeliness verification for news and content freshness checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgugeng](https://clawhub.ai/user/lgugeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to generate AI or technology daily reports that include explicit publication dates, source cross-checks, freshness categories, and a verification summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report templates are mostly oriented toward Chinese-language AI and technology reporting.

Mitigation: Review and adapt the language, audience, and source list before using the skill in a different reporting workflow.

Risk: The artifact includes a cron scheduling example that could run reports automatically if configured.

Mitigation: Configure schedules deliberately and review timing, timezone, and payload before deployment.

Risk: Daily news reports can become inaccurate if dates or sources are stale.

Mitigation: Use explicit publication dates, cross-reference multiple reliable sources, and include the verification summary described by the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lgugeng/skills/ai-news-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown daily report with verification checklist and optional cron scheduling JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3 when the workflow uses the declared command-line dependencies.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
