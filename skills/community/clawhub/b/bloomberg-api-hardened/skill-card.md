## Description: <br>
Query the OFR (Office of Financial Research) Hedge Fund Monitor API for hedge fund data including SEC Form PF aggregated statistics, CFTC Traders in Financial Futures, FICC Sponsored Repo volumes, and FRB SCOOS dealer financing terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and financial researchers use this skill to discover and query public OFR Hedge Fund Monitor time series for hedge fund leverage, counterparties, liquidity, size, complexity, and risk-management analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary marks the release suspicious because package identity, capability tags, and safety documentation are inconsistent. <br>
Mitigation: Review the skill before installing and use it only for the intended public OFR Hedge Fund Monitor API workflow. <br>
Risk: The server security guidance warns against providing wallet access, API keys, passwords, or local secrets. <br>
Mitigation: Do not provide credentials or secrets to this skill; the documented OFR API access requires no API key or registration. <br>
Risk: Requests outside the documented OFR API base URL could expose users to unintended network access or data exfiltration. <br>
Mitigation: Keep network requests limited to https://data.financialresearch.gov/hf/v1 and return retrieved data directly to the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/bloomberg-api-hardened) <br>
- [OFR Hedge Fund Monitor API](https://data.financialresearch.gov/hf/v1) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/bloomberg-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, API calls, markdown] <br>
**Output Format:** [Markdown with inline Python examples, endpoint guidance, and structured API response descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON or CSV-shaped data returned from the public OFR API when the user requests specific series or datasets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
