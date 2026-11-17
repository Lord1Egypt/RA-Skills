## Description:

Use when planning a long EV road trip — which chargers, how many stops, how long each. Physics-based consumption model (speed, temperature, cargo, elevation), a leg-by-leg stop solver with arrival buffers and charge-window taper math, pre-departure checklist (preconditioning, adapters, network accounts), and etiquette rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External EV drivers, including renters and families planning winter trips, use this skill to estimate highway energy use, plan charger stops and charging time, and prepare for charging networks and hotel charging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Estimated energy use, charge time, or charger conditions may differ from the trip plan.

Mitigation: Treat the plan as an estimate; independently check each leg's required charge and arrival reserve, especially when charging above 80%, and confirm current charger status before departure.

## Reference(s):

- [Charging model and field notes](references/charging-model.md)
- [EV Road-Trip Charger Planner on ClawHub](https://clawhub.ai/voronindenis5/skills/ev-road-trip-charger-planner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-text trip summaries and checklists, with Markdown guidance and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates based on vehicle, route, weather, and charger details supplied by the user]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
