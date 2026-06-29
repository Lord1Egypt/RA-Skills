## Description: <br>
Clean company financials from SEC EDGAR via Edgrapi.com, including normalized fundamentals, computed ratios, company profiles, and recent SEC filings for US-listed tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to retrieve SEC EDGAR-derived fundamentals, ratios, company profile data, or recent filing metadata for a specific US-listed company through Edgrapi. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Edgrapi API key and sends requests to a third-party service. <br>
Mitigation: Configure EDGRAPI_KEY only in environments where the Edgrapi provider is trusted and the key can be protected. <br>
Risk: Each tool call may spend Edgrapi credits. <br>
Mitigation: Use the skill only for explicit company financial-data requests and confirm the ticker when intent is ambiguous. <br>
Risk: The skill provides SEC-derived fundamentals and filings, not live market prices or investment advice. <br>
Mitigation: Use another trusted source for live market data and review outputs before relying on them for financial decisions. <br>


## Reference(s): <br>
- [Server-resolved source import](https://github.com/paperandbeyond23-gif/edgrapi-skills/tree/main/skills/edgrapi-full) <br>
- [Edgrapi homepage](https://edgrapi.com) <br>
- [Edgrapi docs](https://edgrapi.com/docs) <br>
- [Edgrapi OpenAPI spec](https://edgrapi.com/openapi.json) <br>
- [Edgrapi pricing](https://edgrapi.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses with text guidance for when to call each tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDGRAPI_KEY; each Edgrapi request may consume credits.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
