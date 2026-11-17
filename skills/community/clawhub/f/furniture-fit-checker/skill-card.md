## Description:

Check if furniture fits a room and the delivery path before buying or moving: computes doorway/hallway/stair clearance with diagonal-tilt geometry, room layout fit with walkway widths, and draws an ASCII floorplan preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to check whether sofas, desks, beds, mattresses, and similar furniture can pass through doors, hallways, stairs, corners, elevators, and fit in rooms before buying or moving them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fit results are approximate and depend on accurate measurements.

Mitigation: Use explicit units, measure the narrowest real route points, and treat passing results as planning guidance rather than a guarantee for heavy or risky moves.

Risk: Very large or unrealistic dimensions may make floorplan output unwieldy.

Mitigation: Use realistic room and furniture dimensions when requesting floorplan output.

## Reference(s):

- [Furniture Fit Geometry Reference](references/fit-geometry.md)
- [ClawHub Skill Page](https://clawhub.ai/voronindenis5/skills/furniture-fit-checker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional ASCII floorplan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces approximate fit assessments from user-supplied measurements; the helper runs locally and uses no network access according to security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
