## Description:

Currency Converter Pro helps agents look up current and historical exchange rates, convert amounts across 150+ currencies, and compare common currency values using open.er-api.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darbling](https://clawhub.ai/user/darbling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to answer currency conversion, exchange-rate lookup, multi-currency comparison, and historical-rate questions in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exchange rates from open.er-api.com are informational and may be inaccurate, delayed, or unavailable.

Mitigation: Verify critical conversions against official financial sources and do not treat the output as financial, legal, or professional advice.

Risk: Currency codes, dates, and requested amounts may be sent to open.er-api.com for rate lookup.

Mitigation: Avoid submitting sensitive transaction context and use only the minimum amount, currency code, and date needed.

Risk: The artifact imports subprocess even though the security evidence says it is unused.

Mitigation: Remove the unused import when maintaining the skill and review any future change that begins executing subprocesses.

## Reference(s):

- [open.er-api.com exchange rate API](https://open.er-api.com/v6)
- [ClawHub skill page](https://clawhub.ai/darbling/skills/currency-converter-pro)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls open.er-api.com over HTTPS; returned exchange rates are informational and not financial advice.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
