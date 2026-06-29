## Description: <br>
Converts an amount from one currency to another using live exchange rates from Open Exchange Rates API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sha-data](https://clawhub.ai/user/sha-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to convert currency amounts in chat with current exchange rates and clear result formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires exec access and runs a local Python script. <br>
Mitigation: Review the packaged script before enabling the skill and run it only in an environment where exec use is expected. <br>
Risk: The Open Exchange Rates App ID and requested currency pairs are sent to the external exchange-rate provider. <br>
Mitigation: Use an API key intended for this purpose, avoid entering sensitive context in conversion requests, and do not expose OXR_APP_ID in agent responses or logs. <br>
Risk: Broad trigger phrases may activate the skill for ambiguous non-currency questions. <br>
Mitigation: Confirm the amount, source currency, and target currency before running the conversion when a user request is unclear. <br>
Risk: The skill instructions reference a scripts/convert.py path, while the artifact contains convert.py at the artifact root. <br>
Mitigation: Confirm the installed script path before use or adjust packaging so the runtime path matches the skill instructions. <br>


## Reference(s): <br>
- [Open Exchange Rates](https://openexchangerates.org) <br>
- [Open Exchange Rates Currency Codes](https://openexchangerates.org/currencies) <br>
- [ClawHub Skill Page](https://clawhub.ai/sha-data/currency-convert) <br>
- [Publisher Profile](https://clawhub.ai/user/sha-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-formatted currency conversion result with exchange rate and update timestamp] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, exec access, network access to Open Exchange Rates, and OXR_APP_ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
