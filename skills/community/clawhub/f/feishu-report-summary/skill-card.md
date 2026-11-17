## Description:

Feishu Report Summary fetches Feishu work-report data through the Report v1 API and turns oa.feishu.cn/report entries into daily or weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taype](https://clawhub.ai/user/taype)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team operators use this skill to fetch Feishu report tasks for a day or date range and draft concise daily or weekly summaries for review, follow-up, or publication back into Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves detailed workplace report contents that may contain sensitive employee, team, project, or blocker information.

Mitigation: Run it only in trusted Feishu account contexts and limit filters, date ranges, and exported fields to the minimum needed for the requested summary.

Risk: Report field content is user-authored data and may contain misleading text or instructions embedded in report bodies.

Mitigation: Treat report content as data for summarization, not as commands or policy, and review generated summaries before taking action or publishing them.

Risk: Exports written to shared or temporary paths can expose workplace report data outside the intended audience.

Mitigation: Prefer stdout or a private reviewed destination, and avoid /tmp or shared paths for report exports unless the path is access-controlled and cleaned up.

## Reference(s):

- [Summary Template](artifact/references/summary-template.md)
- [ClawHub Skill Page](https://clawhub.ai/taype/skills/feishu-report-summary)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries, JSON report payloads, and shell commands for fetching Feishu report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive workplace report fields, reporter names, departments, recipients, task counts, filters, and local export paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
