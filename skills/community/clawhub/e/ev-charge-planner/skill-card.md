## Description:

Helps EV owners estimate home charging time and cost, schedule charging within off-peak windows, and compare EV and gasoline fuel costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

EV owners and home-charger shoppers use this skill to estimate charging duration, electricity costs, off-peak scheduling, and EV-versus-gas fuel costs using their own rates and driving patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Panel-load estimates could be mistaken for approval of an electrical installation.

Mitigation: Use the load check only for planning; consult a qualified electrician and local code requirements before selecting or installing charging equipment.

Risk: The documented --kwh100mi option is ignored, which can make cost comparisons rely on the wrong efficiency assumption.

Mitigation: Provide actual vehicle efficiency with --ev-mi-per-kwh and check the inputs before using the comparison.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/ev-charge-planner)
- [Charging physics](references/charging-physics.md)
- [Time-of-use rates playbook](references/tou-rates-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain-text calculations and Markdown guidance with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline estimates based on user-supplied rates, vehicle efficiency, charging power, and a 90% wall-to-battery efficiency assumption.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
