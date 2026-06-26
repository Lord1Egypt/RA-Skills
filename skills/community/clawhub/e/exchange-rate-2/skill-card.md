## Description: <br>
Use when users need to query daily currency exchange rates between two currencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JaceyMarvin99](https://clawhub.ai/user/JaceyMarvin99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to fetch daily currency exchange rates, either for a specific base and target currency pair or for all available rates for a base currency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes a bundled shell script and makes network requests to a fixed public exchange-rate API. <br>
Mitigation: Review the script before installation and allow the API request only in environments where outbound access to the service is acceptable. <br>
Risk: Currency lookup depends on valid currency codes and local availability of curl and jq. <br>
Mitigation: Use ordinary ISO 4217 currency codes and confirm curl and jq are installed before running the skill. <br>
Risk: Exchange-rate output depends on a third-party API response and may be unavailable or incomplete. <br>
Mitigation: Handle script errors and verify rates against an authoritative financial source before using them for high-impact decisions. <br>


## Reference(s): <br>
- [Exchange Rate API endpoint](https://60s.viki.moe/v2/exchange-rate?currency=${CURRENCY}) <br>
- [ClawHub skill page](https://clawhub.ai/JaceyMarvin99/exchange-rate-2) <br>
- [Publisher profile](https://clawhub.ai/user/JaceyMarvin99) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text exchange-rate value, JSON for all rates, and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses ISO 4217-style currency code inputs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
