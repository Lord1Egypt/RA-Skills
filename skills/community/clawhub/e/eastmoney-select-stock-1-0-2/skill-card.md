## Description:

Eastmoney Select Stock screens A-share, Hong Kong, and U.S. equities from natural-language stock-selection criteria and can return matching stocks, companies, sector constituents, index constituents, and CSV exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen stocks across A-share, Hong Kong, and U.S. markets with natural-language criteria, including market indicators, financial indicators, industry or sector membership, and index constituents. It supports stock research workflows by returning current provider data and optional CSV exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening queries and the Eastmoney API key are sent to the documented Eastmoney endpoint.

Mitigation: Install and run the skill only in environments where sending those queries and credentials to Eastmoney is acceptable.

Risk: The setup instructions include printing the EASTMONEY_APIKEY value.

Mitigation: Check only whether the environment variable is set and avoid displaying or logging the key value.

Risk: Generated CSV files contain remote provider data that may be unsafe in spreadsheet tools.

Mitigation: Treat CSV exports as untrusted data and open them only in viewers that do not evaluate spreadsheet formulas unless the output is sanitized first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/skills/eastmoney-select-stock-1-0-2)
- [Eastmoney Skills API key page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1)
- [Eastmoney stock-screen API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, JSON API responses, tabular text previews, and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY and sends stock-screening keywords to the documented Eastmoney endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and auto changelog; artifact _meta.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
