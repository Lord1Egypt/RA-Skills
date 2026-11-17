## Description:

Currency Exchange Rate helps agents convert currency amounts, check current exchange rates, view rate tables, and list supported currency codes using exchangerate-api.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyangabel](https://clawhub.ai/user/ouyangabel)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to answer currency conversion and exchange-rate questions, including amount conversion, major-currency rate tables, and supported currency-code lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency lookup requests are sent to the disclosed third-party exchangerate-api.com service.

Mitigation: Avoid including sensitive business context or identifying information in currency-code arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ouyangabel/skills/currency-exchange)
- [ExchangeRate-API latest rates endpoint](https://api.exchangerate-api.com/v4/latest)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-line output may appear mostly in Chinese and includes rate date information when returned by the API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
