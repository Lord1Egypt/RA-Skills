## Description:

Provides Chinese-language A-share stock sentiment analysis and report-generation helpers for stock names and related news text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, advisors, and developers can use this skill to score Chinese stock-related text and generate local sentiment reports as decision-support material. It should be reviewed as auxiliary sentiment context, not relied on as live market analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may be mistaken for live market analysis even when report data is mocked or incomplete.

Mitigation: Confirm data sources before relying on results and treat the output as decision-support context rather than trading advice.

Risk: Locally saved reports may expose sensitive financial-interest data and the report command can write outside its intended folder.

Mitigation: Run the skill in a restricted workspace, review output paths before execution, and handle saved reports as sensitive user data.

## Reference(s):

- [China Stock Sentiment ClawHub listing](https://clawhub.ai/daimingvip-a11y/skills/china-stock-sentiment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese-language Markdown reports and plain-text sentiment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save local stock sentiment reports; generated report examples use mock news inputs unless the publisher fixes live-data behavior.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
