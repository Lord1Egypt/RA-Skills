## Description:

Track OpenClaw agent costs. Check daily/weekly spending and model breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shallify](https://clawhub.ai/user/shallify)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use ClawCost to review local session spending, daily budget status, balance tracking, and model-level cost breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs to compute spending.

Mitigation: Install and run it only when local session-log cost analysis is intended.

Risk: The balance-setting command writes local settings under ~/.clawcost/config.json.

Mitigation: Use --set-balance only when you want ClawCost to store or update local budget and balance configuration.

Risk: The separate --format json path appears to contain a bug.

Mitigation: Prefer the default output path until the JSON-format path is fixed or reviewed.

## Reference(s):

- [Model Pricing Reference](references/pricing.md)
- [ClawHub Skill Page](https://clawhub.ai/shallify/skills/clawcost)
- [Publisher Profile](https://clawhub.ai/user/shallify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON data produced by the local Python helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include budget warnings, balance status, daily and weekly totals, all-time totals, model breakdowns, and setup commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
