## Description:

Generates precise static or interactive GeoGebra geometry diagrams using a single Execute({...}) script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gallexy-liu](https://clawhub.ai/user/gallexy-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and students use this skill to turn geometry problems into accurate GeoGebra constructions that preserve relationships such as perpendiculars, tangencies, rotations, intersections, and constrained movable points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated geometry scripts can contain construction or syntax errors that produce an inaccurate diagram.

Mitigation: Review the Execute({...}) command, verify expected objects or measured values in GeoGebra's Algebra panel, and capture a screenshot when evidence is needed.

Risk: Browser-based verification may open GeoGebra, use clipboard paste, and capture screenshots.

Mitigation: Use the skill only when that visible browser workflow is acceptable, and review screenshots before sharing them.

## Reference(s):

- [GeoGebra Execute Examples](references/examples.md)
- [Project homepage](https://github.com/gallexy-liu/geogebra-diagram-generator)
- [GeoGebra Geometry](https://www.geogebra.org/geometry)
- [GeoGebra Classic](https://www.geogebra.org/classic)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with a fenced geogebra Execute({...}) code block and brief verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify movable points, sliders, guaranteed geometric relationships, and browser verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
