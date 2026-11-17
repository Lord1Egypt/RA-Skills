## Description:

Searches Douyin for trending videos by keyword or date range and presents engagement metrics in a structured table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand operators, and marketing teams use this skill to research Douyin trends and compare video engagement when planning topics or campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: When API credits are insufficient, the workflow can install payment software and initiate a recharge.

Mitigation: Require separate user approval before installing payment software and before each recharge; confirm the merchant and total amount, and validate the payment destination.

Risk: Search keywords are sent to RedFox and consume credits; daily subscriptions can create recurring searches.

Mitigation: Disclose the data sharing and credit use, and enable recurring searches only with explicit user opt-in.

## Reference(s):

- [Alipay recharge workflow](references/alipay-recharge.md)
- [ClawHub skill release](https://clawhub.ai/redfox-data/skills/douyin-search-redfox)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown table with linked video titles and engagement metrics; JSON search records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keyword and optional date range; results are ranked by likes, with up to 50 records per page.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
