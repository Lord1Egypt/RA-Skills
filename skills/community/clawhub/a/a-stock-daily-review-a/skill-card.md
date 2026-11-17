## Description:

Generates a structured Markdown daily review for China's A-share market using TDX market data, westock-data, and web checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlfan966-tech](https://clawhub.ai/user/jlfan966-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill after A-share trading days to compile a Markdown market recap with index performance, limit-up/down statistics, sector rotation, high-turnover stocks, market news, and beginner-oriented next-day notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill calls market-data and web tools to assemble a financial market review.

Mitigation: Use it only with intended A-share market-data connectors and review source labels before relying on the report.

Risk: The skill writes reports under E:/文件/workbody/ and may target an existing same-day filename.

Mitigation: Ask for confirmation before overwriting an existing report for the same date.

Risk: TDX, westock-data, and web sources may disagree or become unavailable.

Mitigation: Preserve the skill's source-priority labels and fallback notices in the generated Markdown.

## Reference(s):

- [Server-resolved source repository](https://github.com/jlfan966-tech/a-stock-daily-review-a-)
- [ClawHub skill page](https://clawhub.ai/jlfan966-tech/skills/a-stock-daily-review-a)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown report plus a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes an A-share daily review Markdown file to E:/文件/workbody/ when a trading day is selected.]

## Skill Version(s):

0.1.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
