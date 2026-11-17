## Description:

Get current weather, multi-day forecasts, clothing index, and feels-like temperature for cities worldwide, with SkillPay billing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kim1903](https://clawhub.ai/user/kim1903)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to fetch current weather, multi-day forecasts, feels-like temperature, comfort details, and clothing recommendations for a named city.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The billing script can initiate SkillPay charges and handles a billing API key.

Mitigation: Review before installing if automatic SkillPay charges are not acceptable, and keep SKILLPAY_API_KEY in a protected environment or secret store.

Risk: Passing the billing API key on the command line can expose the secret through shell history or process listings.

Mitigation: Prefer SKILLPAY_API_KEY from the environment instead of the --api-key argument.

Risk: City names are sent to wttr.in and billing identifiers are sent to SkillPay.

Mitigation: Confirm the user is comfortable with those external data transfers before running weather or billing commands.

## Reference(s):

- [Clothing Index Reference](references/clothing-index.md)
- [wttr.in weather data endpoint](https://wttr.in/{encoded}?format=j1)
- [SkillPay API endpoint](https://skillpay.me/api/v1)
- [ClawHub skill page](https://clawhub.ai/kim1903/skills/aaad123)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON from command-line scripts, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather and clothing outputs may include Chinese labels and emoji; forecast output is limited to 7 days.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
