## Description:

Helps size and place room air purifiers, assess existing units and DIY filters, track PM2.5 readings, and estimate filter replacement timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households and their advisors use this skill to choose an appropriately sized clean-air room purifier, evaluate DIY filtration, interpret PM2.5 logs, and track filter use during smoke or allergy events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional PM2.5 logs can retain timestamps, notes, purifier state, and filter-use history on the local device.

Mitigation: Avoid sensitive household details in notes; delete artifact/scripts/air_data.json to clear stored history.

## Reference(s):

- [Clean Air Science & References](references/air-science.md)
- [Clean Air Room Planner on ClawHub](https://clawhub.ai/voronindenis5/skills/clean-air-room-planner)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain-text estimates and recommendations with example shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional PM2.5 diary and filter records are stored locally as JSON.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
