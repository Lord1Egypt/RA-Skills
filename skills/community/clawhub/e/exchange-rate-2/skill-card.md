## Description:

Use when users need to query daily currency exchange rates between two currencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaceymarvin99](https://clawhub.ai/user/jaceymarvin99)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch current exchange rates for a base and target ISO 4217 currency code, or to retrieve all available rates for a base currency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local shell script that contacts the external 60s exchange-rate API.

Mitigation: Run it only in environments where outbound network requests to that API are permitted.

Risk: The script depends on curl, jq, network availability, and the API response shape.

Mitigation: Confirm curl and jq are installed and handle unavailable or malformed API responses before relying on the output.

## Reference(s):

- [60s exchange-rate API endpoint](https://60s.viki.moe/v2/exchange-rate?currency=CNY)
- [ClawHub skill page](https://clawhub.ai/jaceymarvin99/skills/exchange-rate-2)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text exchange-rate value, JSON for all-rate responses, or concise error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on curl, jq, outbound network access, and the 60s exchange-rate API.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
