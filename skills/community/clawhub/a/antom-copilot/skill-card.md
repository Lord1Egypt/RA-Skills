## Description:

Antom Copilot is an Antom intelligent assistant that analyzes user intent and delegates payment success rate data retrieval, analysis, report generation, and report sending to a payment success rate expert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jewellzhu](https://clawhub.ai/user/jewellzhu)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants and operators use this skill to retrieve Antom payment success rate data, generate PDF and text reports with charts and executive summaries, and send those reports to selected recipients by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores and uses merchant and SMTP credentials.

Mitigation: Use scoped and revocable merchant tokens, an app-specific SMTP password, restrictive permissions on ~/antom/conf.json, and TLS-only SMTP.

Risk: Payment success rate reports can be sent by email to user-supplied recipients.

Mitigation: Review recipient addresses and report contents before sending reports.

Risk: The merchant token is sent to an API host that differs from the endpoint named in the documentation.

Mitigation: Install and run the skill only after verifying that the actual Antom API host used by the code is trusted for the merchant account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jewellzhu/skills/antom-copilot)
- [Antom Portal](https://dashboard.antom.com/)
- [Documented Antom API endpoint](https://ibotservice.alipayplus.com/almpapi/v1/message/chat)
- [Antom Copilot API host used by query script](https://antomaplusai.antom.com/antomcopilotai/mcp/api/v1/antomcopilot/RECALL_data)
- [Antom support](https://global.alipay.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated JSON data, PDF reports, text executive summaries, chart images, and email messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Antom configuration file with merchant and SMTP credentials; report generation depends on date input and prior workflow steps.]

## Skill Version(s):

2.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
