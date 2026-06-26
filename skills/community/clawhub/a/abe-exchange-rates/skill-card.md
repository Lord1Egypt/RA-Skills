## Description: <br>
Fetches live fiat currency exchange rates between currency pairs and returns the rate, converted amount, source, and timestamp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up live fiat currency exchange rates and convert amounts between ISO 4217 currency pairs. It is for informational currency conversion, not stock prices, crypto prices, trading, compliance, or accounting decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The provider may differ when the primary XE lookup fails and the fallback exchange-rate source is used. <br>
Mitigation: Check the source field before relying on a result, and avoid source-specific pricing decisions unless the expected provider is reported. <br>
Risk: Exchange-rate output is informational and may not satisfy compliance, accounting, trading, or regulated pricing requirements. <br>
Mitigation: Use the skill for general fiat conversion only; verify critical financial decisions against an approved rate source. <br>
Risk: The primary lookup requires a SkillBoss API key. <br>
Mitigation: Provide SKILLBOSS_API_KEY through the agent environment or secret manager and avoid pasting credentials into prompts, command arguments, or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-exchange-rates) <br>
- [XE currency converter](https://www.xe.com/currencyconverter/) <br>
- [ExchangeRate-API latest rates endpoint](https://open.er-api.com/v6/latest/USD) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON response with amount, source and timestamp, suitable for a concise human-readable currency conversion summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for the primary XE lookup; may fall back to exchangerate-api.com and reports the provider in the source field.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
