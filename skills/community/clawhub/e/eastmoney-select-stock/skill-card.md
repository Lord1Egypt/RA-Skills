## Description:

Screens and retrieves current stock, company, sector, and index information from East Money's Miaoxiang API based on natural-language selection criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqk000](https://clawhub.ai/user/qqk000)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and financial analysts can use this skill to turn natural-language stock-screening questions into current East Money results and saved CSV, text, and JSON artifacts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening queries and the MX_APIKEY credential are sent to the documented East Money endpoint.

Mitigation: Use the skill only in a trusted runtime, keep the API key in the MX_APIKEY environment variable, and avoid sending sensitive personal or proprietary strategy details.

Risk: Generated CSV files may be opened in spreadsheet software.

Mitigation: Open generated CSV files with spreadsheet formula protections enabled or inspect them as plain text first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qqk000/skills/eastmoney-select-stock)
- [East Money Miaoxiang skills page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA)
- [East Money stock screening API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with command examples; runtime output is CSV, description text, and raw JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY; writes generated stock-screening artifacts to /root/.openclaw/workspace/mx_data/output/ by default.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
