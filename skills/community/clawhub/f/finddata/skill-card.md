## Description: <br>
FindData lets an agent query public financial, economic, market, filings, development, and trade data across 10 sources using natural language in English or Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[williamkongGH](https://clawhub.ai/user/williamkongGH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to ask natural-language questions about public market, macroeconomic, company filing, development, central bank, and trade datasets and receive structured data responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FindData queries and the required API key are sent to the FindData service. <br>
Mitigation: Use an environment variable or managed secret for FINDDATA_API_KEY, avoid private business or personal data in queries, and rotate the key if it is exposed. <br>
Risk: Data responses can be missing, partial, stale, or unsuccessful. <br>
Mitigation: Check the success field and review issues before using returned records in analysis or downstream decisions. <br>


## Reference(s): <br>
- [FindData API query endpoint](https://finddata.ai/api/query) <br>
- [FindData API](https://finddata.ai/api) <br>
- [FindData](https://finddata.ai) <br>
- [ClawHub skill page](https://clawhub.ai/williamkongGH/finddata) <br>
- [Publisher profile](https://clawhub.ai/user/williamkongGH) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with curl and Python examples plus structured JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FindData API key. API responses include success, data, execution, issues, and usage fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
