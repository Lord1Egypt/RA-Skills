## Description: <br>
Generates concise, user-friendly flight price summaries with buy/wait recommendations for chat interfaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyikoi](https://clawhub.ai/user/keyikoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and chat product agents use this skill to turn current and historical flight price data into plain-language buy/wait recommendations, price-level summaries, and caveats when data is limited. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A shared SerpAPI key or unclear local config location could expose operational credentials. <br>
Mitigation: Use a dedicated SerpAPI key and confirm where price/config.json is stored before deployment. <br>
Risk: Price history may contain traveler-identifying or route preference details. <br>
Mitigation: Avoid storing traveler-identifying details in price/data/ and retain only the minimum data needed for price analysis. <br>
Risk: Broad trigger wording may activate the skill for non-flight price questions. <br>
Mitigation: Configure the host router to require flight context before invoking the skill. <br>


## Reference(s): <br>
- [Flight Price Advisor ClawHub page](https://clawhub.ai/keyikoi/flight-price-advisor) <br>
- [SerpAPI signup](https://serpapi.com/users/sign_up) <br>
- [Copywriting Templates](artifact/references/copywriting-templates.md) <br>
- [Price Analysis Algorithm](artifact/references/price-analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with concise tables and buy/wait recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires current price and historical price data; can include setup guidance when SerpAPI or price history is unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
