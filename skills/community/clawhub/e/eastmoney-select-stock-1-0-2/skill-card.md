## Description: <br>
Screens A-share, Hong Kong, and U.S. stocks through Eastmoney by sending natural-language stock-selection criteria and returning matching stocks, company lists, index constituents, and recommendation-style screening results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn natural-language stock-screening criteria into Eastmoney API calls for stock candidates, sector or industry company lists, index constituents, and screening-style recommendations. Treat the results as financial screening data, not standalone investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock-screening keywords are sent to Eastmoney's API. <br>
Mitigation: Use only if you trust the Eastmoney API integration and are comfortable with that data transfer; avoid including private or personal information in screening queries. <br>
Risk: The EASTMONEY_APIKEY can be exposed through logs, chats, or untrusted runtime environments. <br>
Mitigation: Store the key only in trusted environment variables and avoid printing, pasting, or logging it. <br>
Risk: Screening and recommendation-style outputs may be mistaken for financial advice. <br>
Mitigation: Treat results as screening output and verify securities decisions independently before acting on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lean-zhouchao/eastmoney-select-stock-1-0-2) <br>
- [Eastmoney Skills page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1) <br>
- [Eastmoney stock-screening API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/stock-screen) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python examples, plus stock-screening API results that can be exported to CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY and sends keyword, pageNo, and pageSize to Eastmoney's stock-screening API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog; artifact _meta reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
