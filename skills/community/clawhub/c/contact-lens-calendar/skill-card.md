## Description:

Use when tracking open contact lenses, deciding replacement dates, planning a lens stock-up, or comparing daily vs monthly lens cost — computes exact do-not-exceed replacement dates from the day the foil was peeled, flags overdue lenses, counts days of wear left in unopened boxes, and prices each wear modality per day and per year.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Contact lens wearers use this skill to calculate replacement dates from when lenses are opened, track open lenses and unopened supplies, and compare estimated costs across lens schedules. It provides calendar and inventory support, not diagnosis or medical advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lens history is stored unencrypted in the skill folder.

Mitigation: Restrict access to the folder and avoid recording unnecessary personal details.

Risk: Preset replacement periods may differ from lens-specific instructions.

Mitigation: Check the schedule against the lens packaging and eye-care professional instructions.

Risk: Cost figures are estimates, and the skill does not schedule reminders.

Mitigation: Treat cost results as estimates and arrange replacement reminders separately.

## Reference(s):

- [Wear Life Reference](references/wear-life.md)
- [Contact Lens Calendar on ClawHub](https://clawhub.ai/voronindenis5/skills/contact-lens-calendar)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text calendar, inventory, and cost reports; JSON tracking file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores tracking history in contacts.json in the skill folder; does not schedule notifications.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
