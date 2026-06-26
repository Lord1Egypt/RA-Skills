## Description: <br>
Fetches historical prices, near-real-time quotes, and performance rankings for China A-share exchange-traded funds (ETFs and LOFs) through the Cifang Quant API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyuwu](https://clawhub.ai/user/tianyuwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to retrieve China ETF and LOF fund lists, historical market data, near-real-time quotes, and return rankings for financial analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Cifang Quant API key and sends it to the Cifang Quant API. <br>
Mitigation: Install only if the publisher and API provider are trusted, and prefer passing the key explicitly or through a short-lived environment variable. <br>
Risk: Generic finance prompts could trigger live API requests if the skill is automatically activated. <br>
Mitigation: Restrict automatic activation when live fund-data requests should require explicit user intent. <br>
Risk: Market data can be delayed, unavailable, or unsuitable as the sole basis for financial decisions. <br>
Mitigation: Review returned timestamps and data quality notes, and verify important results against authoritative financial sources before acting. <br>


## Reference(s): <br>
- [Cifang Quant Data API](https://www.cifangquant.com/tool/data-api) <br>
- [API reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API results and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can output raw API data, readable JSON objects, or summary statistics depending on the requested command and format.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
