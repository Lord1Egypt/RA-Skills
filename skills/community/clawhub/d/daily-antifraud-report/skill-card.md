## Description:

Generates a daily anti-fraud briefing about Chinese domestic banks and payment institutions, focused on recent cases, involved institutions, amounts, and related details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdl2005](https://clawhub.ai/user/wdl2005)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or operators responsible for fraud-monitoring briefings use this skill to collect recent China-focused anti-fraud news and summarize relevant cases for daily distribution.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Scheduled execution and automatic Feishu distribution can send unreviewed reports to unintended recipients.

Mitigation: Enable scheduled posting only where Feishu distribution is intended, confirm the destination, and review report content before broader circulation.

Risk: The helper script uses the result-count argument in a shell command without validation or quoting.

Mitigation: Validate the result count as a positive integer and quote shell variables before using the helper script in automated workflows.

Risk: Public search results may produce incomplete or stale case details.

Mitigation: Check material case facts against authoritative financial institution, regulator, or reputable news sources before relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wdl2005/skills/daily-antifraud-report)
- [Baidu search endpoint used by helper script](https://www.baidu.com/s?wd=${QUERY}&rn=${NUM})

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured Markdown list of anti-fraud case summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each item is expected to include case date, case process, bank or payment institution, amount involved, and other relevant details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
