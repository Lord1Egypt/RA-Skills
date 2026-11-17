## Description:

Queries China Merchants Bank foreign exchange quote data and explains how to calculate HKD-CNY mid-rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horsley](https://clawhub.ai/user/horsley)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query China Merchants Bank FX rate data and calculate a midpoint price for HKD-CNY exchange-rate workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live network requests to China Merchants Bank's FX API when used.

Mitigation: Review the target API URL before execution and use the skill only in environments where outbound requests to fx.cmbchina.com are allowed.

Risk: The documented filtering example uses jq, but the metadata declares only curl as required.

Mitigation: Install jq or adapt the JSON parsing step to an available tool before relying on the example command.

Risk: Live FX quote data can change or become unavailable if the external API changes or is unreachable.

Mitigation: Check the response timestamp and handle failed or stale responses before using calculated mid-rates.

## Reference(s):

- [China Merchants Bank FX rate API](https://fx.cmbchina.com/api/v1/fx/rate)
- [ClawHub skill page](https://clawhub.ai/horsley/skills/cmb-fx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and exchange-rate calculation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make network requests to the CMB FX API; the documented filtering example uses jq although only curl is declared as required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
