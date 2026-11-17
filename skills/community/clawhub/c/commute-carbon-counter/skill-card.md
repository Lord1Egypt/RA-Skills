## Description:

Commute Carbon Counter helps users log trips across 14 transport modes, calculate kg CO2 per trip, week, and month with per-passenger-km factors, compare against a solo-car baseline, project annual emissions, and export commute data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and teams use this skill to compare commute modes, track personal or team mobility emissions, review weekly and monthly reports, and export local trip data for sustainability planning. It is planning-grade and not intended for certified carbon accounting, offset purchases, or regulatory reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trip dates, modes, distances, passenger counts, notes, and exports may reveal personal commuting patterns if local files are shared or stored insecurely.

Mitigation: Keep local JSON and CSV files in an appropriate user-controlled location, avoid adding sensitive notes, and review exports before sharing.

Risk: Emission factors are planning-grade averages and may be unsuitable for formal carbon accounting, regulatory reporting, certified offsets, or purchase decisions that require audited numbers.

Mitigation: Use the reports for personal planning and comparisons, and rely on certified or measured data for regulatory, financial, or offset-related use.

## Reference(s):

- [Emission Factors - Sources, Ranges, and Honesty](references/emission-factors.md)
- [ClawHub skill page](https://clawhub.ai/voronindenis5/skills/commute-carbon-counter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands, plain-text command output, local JSON storage, and optional CSV export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trip data is stored locally by default and can be redirected with a file path option.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
