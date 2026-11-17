## Description:

Civilization 6 district mechanics library. Use when working with district placement validation, adjacency bonus calculations, or understanding Civ6 game rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reason about Civilization 6 district placement, validate district constraints, and calculate adjacency bonuses for planning or rules-reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Canal placement validation has a documented accuracy bug and should not be treated as authoritative.

Mitigation: Review canal placement outputs against Civilization 6 rules and rely on them only after the flat-land check is fixed and tested.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wu-uk/skills/civ6-adjacency-optimizer-civ6lib)
- [Civilization Wiki: Adjacency Bonus (Civ6)](https://civilization.fandom.com/wiki/Adjacency_bonus_(Civ6))
- [Civilization Wiki: District (Civ6)](https://civilization.fandom.com/wiki/District_(Civ6))

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown prose with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Python modules for Civ6 district placement validation and adjacency calculations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
