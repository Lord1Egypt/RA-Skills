## Description: <br>
Fetches live exchange rates between currency pairs from XE.com, with a fallback exchange-rate API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrInvincible29](https://clawhub.ai/user/mrInvincible29) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill when a user asks for currency conversion or live exchange rates between standard currency codes. It returns a rate and converted amount for presentation to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts XE.com and exchangerate-api.com to obtain live exchange-rate data. <br>
Mitigation: Use it only in environments where outbound requests to those services are acceptable. <br>
Risk: The skill connects to a local Browserless service on localhost:7002 using an embedded CDP token. <br>
Mitigation: Verify that the local Browserless service and token are intended for the deployment, and prefer moving the token into user-controlled configuration. <br>
Risk: The fallback source may return rates that differ from XE.com mid-market rates. <br>
Mitigation: Show the returned source with the result so users know which rate provider was used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrInvincible29/exchange-rates) <br>
- [XE currency converter](https://www.xe.com/currencyconverter/) <br>
- [ExchangeRate API fallback](https://open.er-api.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON from the helper script, summarized as concise user-facing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes amount, source currency, target currency, rate, converted amount, source, and timestamp when lookup succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
