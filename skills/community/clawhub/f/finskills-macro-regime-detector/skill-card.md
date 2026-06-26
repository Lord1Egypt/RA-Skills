## Description: <br>
Classify the current macroeconomic regime across six states using GDP, CPI, Fed Funds rate, yield curve, and credit spread data from the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to classify the current U.S. macroeconomic regime from Finskills API data and translate the result into portfolio-positioning context. It is intended for macro analysis and education, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and makes external API requests for macroeconomic data. <br>
Mitigation: Configure only the required FINSKILLS_API_KEY and avoid sharing credentials or sensitive account details in prompts. <br>
Risk: Macro regime and allocation outputs may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as educational macro analysis and review them with qualified judgment before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/finskills-macro-regime-detector) <br>
- [Publisher profile](https://clawhub.ai/user/finskills) <br>
- [Source homepage](https://github.com/finskills/macro-regime-detector) <br>
- [Finskills API](https://finskills.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with macro dashboard, regime classification, rationale, and asset allocation implications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and calls Finskills API endpoints for macroeconomic and market data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
