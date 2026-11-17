## Description:

Use when buying or running a backup generator during outages — builds an appliance-by-appliance load sheet with starting-surge multipliers (fridge 3x, well pump 3x), picks the right generator class (2k/3.5k/7.5k/13kW) from real surge math, computes gasoline/propane burn and storm-duration fuel needs, and flags CO/transfer-switch/backfeed safety before the power dies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners and outage planners use the skill to estimate appliance loads, generator capacity, and fuel needs while preparing for backup power. Its outputs can inform planning, with startup compatibility checked against actual appliance and generator specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend an undersized generator because its sizing and fit checks ignore the starting power it calculates.

Mitigation: Treat sizing and positive fit results as unverified running-load estimates. Confirm startup compatibility against actual appliance and generator specifications before relying on recommendations, especially for medical equipment, heating, or pumps.

## Reference(s):

- [Load and Fuel Physics Reference](artifact/references/load-fuel-physics.md)
- [Honda Generator Sizing Guide](https://powerequipment.honda.com/generators/generator-how-much-power)
- [ClawHub Release](https://clawhub.ai/voronindenis5/skills/generator-sizer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text load sheet or JSON, with generator and fuel estimates and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on appliance inputs and model assumptions; verify starting compatibility against actual equipment specifications.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
