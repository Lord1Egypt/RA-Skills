## Description:

Creates multi-week school and activity carpool schedules that account for driver availability, passenger and booster-seat capacity, absences, holidays, fairness tracking, and optional fuel splits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Families and carpool coordinators use this skill to plan school or activity rides across multiple weeks, balance driving by occupied seats, and optionally calculate fuel settlements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Schedules and fairness balances depend on accurate rider, availability, capacity, absence, and blackout details.

Mitigation: Check the registry and review the generated assignments and audit before sharing or relying on the schedule.

Risk: Fuel settlements are estimates based on the supplied mileage and per-kilometre rate.

Mitigation: Confirm the route distance, rate, and resulting amounts with the families before settling costs.

## Reference(s):

- [Carpool Rotation Coordinator on ClawHub](https://clawhub.ai/voronindenis5/skills/carpool-rotation-coordinator)
- [Fairness model and registry reference](references/fairness-model.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain-text schedule and tables with an optional fuel settlement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Week-by-week driver assignments, per-family seat-credit audit, and optional who-pays-whom cost split.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
