## Description:

FindData lets agents query public financial, economic, company, market, development, central-bank, and trade data sources with natural-language questions in English or Chinese using a FindData API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamkonggh](https://clawhub.ai/user/williamkonggh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask data questions and retrieve structured public data from FindData-supported sources such as Yahoo Finance, FRED, World Bank, SEC EDGAR, BIS, Eurostat, BOJ, Our World in Data, and UN Comtrade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if pasted into chat or stored in an untrusted place.

Mitigation: Provide the FindData API key through a trusted environment variable or secret manager instead of chat.

Risk: The FindData API key and user data questions may be sent to a configurable API origin.

Mitigation: Use the default FindData endpoint unless FINDDATA_BASE_URL points to a destination you fully trust.

Risk: Queries and returned data may involve financial, economic, or market information that could be incomplete, delayed, or unavailable.

Mitigation: Check the API response success flag, issues array, source details, and data quality fields before relying on results.

## Reference(s):

- [FindData](https://finddata.ai)
- [FindData API Query Endpoint](https://finddata.ai/api/query)
- [ClawHub Skill Page](https://clawhub.ai/williamkonggh/skills/finddata)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code examples, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the user's natural-language query and the FindData API response, including data records, sources, execution details, issues, and usage information.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
