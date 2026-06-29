## Description: <br>
Provides normalized company financial statements and computed ratios from SEC EDGAR via Edgrapi.com for US-listed tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill when a user explicitly asks for US-listed company fundamentals or ratios, such as revenue, assets, cash flow, margins, return, leverage, or liquidity. It is not intended for live stock prices or incidental ticker mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Edgrapi API key and sends requests to an external service. <br>
Mitigation: Configure EDGRAPI_KEY only in trusted environments and install the skill only when Edgrapi fundamentals data is intended. <br>
Risk: Each Edgrapi tool call may consume account credits. <br>
Mitigation: Use the skill only for deliberate financial-statement or ratio requests and avoid activating it for incidental ticker mentions. <br>
Risk: The skill provides filings-derived fundamentals and ratios, not live market prices or price-based multiples. <br>
Mitigation: Use a separate market data source for live prices, P/E, P/B, or other price-dependent analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paperandbeyond23-gif/skills/edgrapi-fundamentals) <br>
- [Server-resolved GitHub import](https://github.com/paperandbeyond23-gif/edgrapi-skills/tree/main/skills/edgrapi-fundamentals) <br>
- [Edgrapi homepage](https://edgrapi.com) <br>
- [Edgrapi pricing](https://edgrapi.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration guidance] <br>
**Output Format:** [Markdown responses with structured financial figures and ratio values; API helper results are dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDGRAPI_KEY; each Edgrapi tool call may consume one credit and should be used for deliberate fundamentals or ratio requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
