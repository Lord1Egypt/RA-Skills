## Description: <br>
Queries Eastmoney financial data for market prices, company financials, and entity relationships from natural-language prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-analysis agents use this skill to ask natural-language questions against Eastmoney data and retrieve structured market, financial, and relationship data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial query text is sent to Eastmoney's API and returned data is saved in local output files. <br>
Mitigation: Keep MX_APIKEY in a trusted environment, avoid sending secrets or confidential internal details in queries, and periodically remove generated JSON or Excel files that contain sensitive data. <br>
Risk: Large financial-data queries can produce oversized outputs that are difficult for an agent to inspect reliably. <br>
Mitigation: Use narrow securities, metrics, and date ranges when querying, then expand only after confirming the returned structure is useful. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QQK000/eastmoney-fin-data) <br>
- [Eastmoney MiaoXiang Skills homepage](https://marketing.dfcfs.com/views/finskillshub/indexIoMv0EzE) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, json, configuration] <br>
**Output Format:** [Markdown terminal preview plus Excel workbook, description text file, and raw JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MX_APIKEY; writes query outputs to a local mx_data output directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
