## Description: <br>
Provides real-time or near-real-time currency exchange rate lookup and conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxsjlrwsj](https://clawhub.ai/user/wxsjlrwsj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to convert amounts between supported currencies or answer exchange-rate questions using normalized currency codes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts exchangerate-api.com when used, so results depend on external network availability and API responses. <br>
Mitigation: Use the returned success or error status, handle network/API failures clearly, and avoid presenting failed conversions as current rates. <br>
Risk: Untrusted raw text could lead to invalid amounts or currency codes being passed to the command. <br>
Mitigation: Parse numeric amounts and normalize supported ISO currency codes before invoking the script. <br>


## Reference(s): <br>
- [Currency Converter on ClawHub](https://clawhub.ai/wxsjlrwsj/currency-converter) <br>
- [ExchangeRate API endpoint used by the skill](https://api.exchangerate-api.com/v4/latest/{from_currency}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Natural-language response based on JSON returned by a Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns converted amount, exchange rate, source and target currency codes, and update time when the API call succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
