## Description:

Helps fountain pen users calculate ink dilutions and drying estimates, compare ink types, convert recipe units, and log custom batches while highlighting pen-safety precautions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Fountain pen users and ink mixers use this skill to plan and record ink adjustments, compare ink suitability for different nibs, and estimate drying and fill quantities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding a batch creates or updates a local JSON log containing recipe names and notes.

Mitigation: Keep the log in a workspace or dedicated data directory, especially when specifying --log.

Risk: Unverified estimates or unsuitable inks can cause smearing, clogging, or pen damage.

Mitigation: Swab-test mixtures on the intended paper and follow the ink compatibility guidance before filling a pen.

## Reference(s):

- [Ink Craft reference](references/ink-craft.md)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/fountain-pen-ink-alchemist)

## Skill Output:

**Output Type(s):** [Text, Guidance, JSON files]

**Output Format:** [Markdown or plain text; optional local JSON batch log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drying and fill estimates are planning heuristics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
