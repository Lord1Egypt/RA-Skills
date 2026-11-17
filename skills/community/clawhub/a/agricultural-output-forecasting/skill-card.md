## Description:

Agricultural Output Forecasting helps generate crop yield and agricultural production estimates from crop, area, region, season, weather-factor, and market-factor inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andyxcg](https://clawhub.ai/user/andyxcg)

### License/Terms of Use:

MIT-0

## Use Case:

Farmers, agronomists, agricultural businesses, and agents assisting them use this skill to estimate crop yield, compare forecast factors, export forecast records, and produce planning recommendations. Outputs should be treated as decision-support estimates rather than agronomic or financial guarantees.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid billing and local trial-state tracking are part of the skill behavior.

Mitigation: Review the payment flow and local trial-state file before installation, keep billing keys out of command lines, and avoid passing real customer identifiers.

Risk: Forecasting claims may overstate reliability, while the implementation uses simulated weather, market, and historical factors.

Mitigation: Treat results as simulated decision-support estimates and do not rely on them as agronomic, financial, insurance, or operational guarantees.

Risk: The artifact includes an auto-evolution daemon that can run as a long-lived background process.

Mitigation: Do not run the daemon unless that background behavior is explicitly desired and has been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andyxcg/skills/agricultural-output-forecasting)
- [Forecast methodology](references/forecast-methodology.md)
- [SkillPay billing API reference](references/skillpay-billing.md)
- [Security policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [JSON forecast responses, optional CSV exports, Markdown guidance, Python examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Forecast responses may include yield estimates, confidence intervals, weather and market factors, risk assessment, recommendations, billing status, trial status, and remaining balance.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
