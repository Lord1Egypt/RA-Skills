## Description:

Agent Insight helps collect customer-facing agent observations about pain points, service improvements, revenue opportunities, churn risk, and field insights, then produce a consolidated insight report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Customer success and account-management teams can use this skill to ask deployed agents for recurring customer insights and summarize the responses into a monthly or on-demand report. It is intended for authorized customer review workflows where churn risk, product gaps, and upsell opportunities need to be surfaced.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly collects and stores customer-specific conversation-derived insights without clear privacy limits or user controls.

Mitigation: Use only in an authorized customer-success or account-management context, restrict report access, and redact personal data, secrets, and unnecessary customer identifiers before saving reports.

Risk: Channel-wide prompts or scheduled runs could request responses from more participants than intended.

Mitigation: Require explicit confirmation before channel-wide prompts or scheduled runs, and restrict who can respond to the insight request.

## Reference(s):

- [Sample Insight Report](references/sample-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report and concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include customer-specific operational observations and should be reviewed for privacy before storage or sharing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
