## Description:

Query empty classrooms at BUPT (Beijing University of Posts and Telecommunications) Xitucheng campus for a selected building and time period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlcle](https://clawhub.ai/user/hlcle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check BUPT Xitucheng campus classroom availability for a selected building and class period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Classroom availability may be unavailable or inaccurate if the external classroom-query website changes or is down.

Mitigation: Verify important room decisions against the university's authoritative scheduling or academic system before relying on the result.

Risk: Browser element references and enabled time periods can change after each page interaction.

Mitigation: Refresh the browser snapshot after selecting a building or time period and avoid clicking disabled time-period controls.

## Reference(s):

- [BUPT Empty Classroom web app](https://ec.jray.xyz/)
- [ClawHub skill page](https://clawhub.ai/hlcle/skills/bupt-empty-classroom)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with browser command examples and tabular classroom availability results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the external classroom-query website, current date defaults, selected building, and selected time period.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
