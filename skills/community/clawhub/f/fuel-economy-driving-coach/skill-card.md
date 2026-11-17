## Description:

Use when you want to spend less on fuel — turns driving-style talk into numbers: computes your engine's BSFC-based theoretical floor, prices each habit (idling, aggressive acceleration, 75 vs 60 mph, roof box, underinflated tires, AC vs windows) in real $/yr for YOUR mileage and gas price, and ranks fixes by payback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Drivers and commuters use the skill to estimate how driving habits, trip choices, and vehicle conditions affect fuel costs, then compare potential changes using their mileage and fuel price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fuel-cost and efficiency results are rough estimates, not engine-specific analysis or verified payback.

Mitigation: Treat results as directional estimates and check vehicle-specific guidance with the manufacturer.

Risk: The documented `--frontal 24` example conflicts with the script's square-metre input and 2.2 default.

Mitigation: Check input units and use a frontal area in square metres; the documented sedan example is approximately 2.2.

Risk: Driving-speed comparisons could encourage unsafe or unlawful speed choices.

Mitigation: Keep speed choices within safe, legal limits and follow vehicle-manufacturer guidance.

## Reference(s):

- [Fuel Economy — Reference & Sources](references/fuel-reference.md)
- [Fuel Economy Driving Coach on ClawHub](https://clawhub.ai/voronindenis5/skills/fuel-economy-driving-coach)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Console text with ranked estimates, summaries, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Estimates depend on user-provided vehicle, mileage, trip, and fuel-price inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
