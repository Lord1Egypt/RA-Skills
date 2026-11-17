## Description:

Retired signal. No longer sold.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators can use this guidance to recognize that the cross-exchange spread signal is retired, avoid calling its unavailable endpoint, and find the listed arb-spread alternative.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may try to call the retired endpoint, which responds with HTTP 410 Gone.

Mitigation: Do not configure an agent to call this signal; the artifact says no payment is requested or available.

Risk: A benign scan does not guarantee zero risk.

Mitigation: Review the skill against its documented behavior before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kynto2001-ctrl/skills/cross-exchange-spread)
- [Retired cross-exchange-spread signal](https://apexrunner.ai/signals/cross-exchange-spread)
- [arb-spread signal](https://apexrunner.ai/signals/arb-spread)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documents a retired signal; it does not provide live exchange data.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
