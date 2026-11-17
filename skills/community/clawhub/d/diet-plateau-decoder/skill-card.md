## Description:

Use when the scale hasn't moved in 2+ weeks: separates TRUE plateaus (real energy-balance stalls) from water-retention masks (sodium, cortisol, menstrual phase, new training damage) and logging drift, using 7-day rolling averages, trend-vs-noise statistics, and expected-rate physics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

People tracking weight loss and coaches reviewing a client's stalled scale trend use the skill to compare weight data with expected loss and logged water-retention factors before deciding what to review next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool's labels are rough estimates rather than validated diagnoses, and expected-loss and reported-noise inputs do not control its conclusions.

Mitigation: Treat the output as a prompt for review, not a diagnosis or the sole basis for changing calorie intake; check the underlying trend and context.

Risk: The skill explicitly excludes eating-disorder contexts and suspected medical edema.

Mitigation: Do not use it for eating-disorder-related monitoring or suspected medical edema; seek appropriate qualified support for those concerns.

## Reference(s):

- [Diet Plateau Decoder science reference](references/plateau-science.md)
- [Diet Plateau Decoder on ClawHub](https://clawhub.ai/voronindenis5/skills/diet-plateau-decoder)
- [Publisher profile: voronindenis5](https://clawhub.ai/user/voronindenis5)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, JSON]

**Output Format:** [Plain-text trend report or JSON]

**Output Parameters:** [1D daily weight series with expected-loss rate and optional context flags]

**Other Properties Related to Output:** [Includes trend estimates, a verdict, and an action plan; outputs are rough estimates, not validated diagnoses.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
