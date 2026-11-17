## Description:

Helps agents assess generic vehicle maintenance status, identify overdue or upcoming service, and build a 24-month maintenance budget from odometer, vehicle age, driving conditions, and service history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to evaluate whether common vehicle maintenance tasks are overdue, due soon, or currently OK, and to estimate upcoming service timing and cost. It is useful for maintenance planning, used-car baseline checks, city-commuter severe-service adjustments, and sanity-checking dealer service recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic maintenance intervals can be mistaken for model-specific, warranty, or jurisdiction-specific requirements.

Mitigation: Treat the output as advisory and verify schedules against the owner's manual, documented service records, and local inspection rules.

Risk: Malformed or untrusted service-history JSON can affect the local advisory calculator.

Mitigation: Use trusted, well-formed history entries and validate task names, dates, and odometer values before passing history JSON to the skill.

## Reference(s):

- [The Maintenance Model](references/maintenance-model.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/car-maintenance-timeline)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local script can list maintenance tasks, report status, or project a 24-month timeline; JSON output is available for agent workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
