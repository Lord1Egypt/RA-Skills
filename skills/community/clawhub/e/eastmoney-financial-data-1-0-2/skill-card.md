## Description: <br>
This skill queries Eastmoney financial data from natural-language prompts, covering real-time market data, fund flows, valuation data, company fundamentals, financial indicators, executive information, business lines, ownership relationships, and operating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to retrieve current Eastmoney financial data for securities, sectors, indices, funds, bonds, company fundamentals, relationships, and operating information. It is useful when model-only knowledge may be stale and a structured JSON response from a remote financial-data API is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query text and the API key are sent to Eastmoney's remote API. <br>
Mitigation: Use the skill only in trusted environments, keep EASTMONEY_APIKEY in environment variables, and avoid submitting confidential personal, account, or proprietary trading information. <br>
Risk: Large financial-data queries can return excessive data that may overwhelm the agent context. <br>
Mitigation: Ask for bounded securities, indicators, and date ranges, and narrow the request before retrying if the response is too large. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lean-zhouchao/eastmoney-financial-data-1-0-2) <br>
- [Eastmoney API key page](https://marketing.dfcfs.com/views/finskillshub/indexuNdYscEA?appfenxiang=1) <br>
- [Eastmoney query API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON responses from the Eastmoney API with Markdown usage guidance and shell or Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EASTMONEY_APIKEY and sends query text to Eastmoney's remote API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
