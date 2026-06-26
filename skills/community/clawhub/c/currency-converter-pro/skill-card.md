## Description: <br>
Currency Converter Pro helps agents look up current exchange rates, convert amounts, compare common currencies, and request historical rates using a public exchange-rate API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer currency exchange questions by running conversion, rate listing, multi-currency comparison, and historical lookup commands. Returned exchange-rate data is informational and should be checked against official sources for important financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts open.er-api.com to retrieve exchange-rate data. <br>
Mitigation: Use it only in environments where outbound requests to that public exchange-rate service are acceptable. <br>
Risk: Exchange-rate responses are informational and may be inaccurate or unsuitable for financial decisions. <br>
Mitigation: Verify important conversions with official or authoritative financial sources before acting on them. <br>
Risk: Broad trigger language may cause the skill to answer general currency-exchange questions. <br>
Mitigation: Review the generated command or response for relevance before relying on it in user-facing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/darbling/currency-converter-pro) <br>
- [Open ER API endpoint](https://open.er-api.com/v6) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, guidance] <br>
**Output Format:** [JSON responses with concise text or Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls open.er-api.com for exchange-rate data and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
