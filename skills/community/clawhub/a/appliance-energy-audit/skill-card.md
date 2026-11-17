## Description:

Use when you want to know which appliances actually drive your electric bill, whether a bill spike is explained by your usage, if standby/vampire draw is worth addressing, whether replacing an old fridge/dryer/AC pays back, or when modeling tiered utility rates - builds a ranked cost-per-appliance table from watts, duty cycle, and usage hours, reconciles it against your real bill, and computes replacement payback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to estimate per-appliance electricity costs, reconcile modeled usage against utility bills, identify standby draw, and evaluate appliance replacement payback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inventory files may contain household appliance and utility usage details.

Mitigation: Keep inventory JSON limited to appliance details and utility usage numbers; do not include secrets, account credentials, or unrelated personal files.

Risk: Model-based estimates can mislead appliance purchase decisions when appliance duty cycles or usage hours are inaccurate.

Mitigation: Calibrate the audit against the real monthly bill before relying on per-appliance rankings or replacement payback results.

## Reference(s):

- [The Energy Model](references/energy-model.md)
- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/appliance-energy-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with command examples and tabular audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python CLI output; no network access or credential handling indicated by server security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
