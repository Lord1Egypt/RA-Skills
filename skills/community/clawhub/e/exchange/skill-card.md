## Description: <br>
Queries and converts currency exchange rates, including popular rates, supported currencies, bank foreign-exchange quotes, real-time market data, and historical exchange-rate trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer currency conversion and exchange-rate lookup questions by calling JisuAPI-backed commands. It supports current conversions, currency lists, bank quotes, real-time rates, and historical rate or price trend queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency, date, bank, and market query details are sent to JisuAPI. <br>
Mitigation: Use the skill only when this third-party data flow is acceptable, and avoid including sensitive personal or business context in lookup prompts. <br>
Risk: The skill requires a JISU_API_KEY to call the external API. <br>
Mitigation: Use a scoped key, provide it through the environment, and do not hard-code it in prompts or files. <br>
Risk: Exchange-rate results are reference data and may not be appropriate as the sole basis for financial decisions. <br>
Mitigation: Verify important rates against an authoritative financial source before relying on them for transactions or reporting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/exchange) <br>
- [JisuAPI exchange-rate API documentation](https://www.jisuapi.com/api/exchange/) <br>
- [JisuAPI publisher site](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; exchange-rate queries are sent to api.jisuapi.com.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
