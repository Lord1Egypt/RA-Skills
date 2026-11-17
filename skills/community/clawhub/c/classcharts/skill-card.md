## Description:

Query and interact with ClassCharts (UK education classroom management) via the classcharts-api JS library for homework, behaviour points, timetable, detentions, attendance, rewards, and parent or student data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m0nkmaster](https://clawhub.ai/user/m0nkmaster)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized ClassCharts users use this skill to script or integrate access to school homework, behaviour, timetable, attendance, announcements, detentions, pupil records, and rewards workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive student, pupil, attendance, behaviour, and school account data.

Mitigation: Install and use it only when authorized for the relevant ClassCharts account and pupil records, and run it with only the required secrets exposed.

Risk: The skill can perform account-changing or value-changing actions such as password changes and rewards purchases.

Mitigation: Require explicit user confirmation before password changes, rewards purchases, or other account-changing actions.

Risk: The skill depends on an unofficial npm package for ClassCharts access.

Mitigation: Pin and review the npm dependency before use, and run it in a constrained environment.

## Reference(s):

- [ClassCharts skill page](https://clawhub.ai/m0nkmaster/skills/classcharts)
- [classcharts-api library docs](https://classchartsapi.github.io/classcharts-api-js)
- [Unofficial ClassCharts API docs](https://classchartsapi.github.io/api-docs/)
- [classcharts-api-js GitHub repository](https://github.com/classchartsapi/classcharts-api-js)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CLASSCHARTS_EMAIL, CLASSCHARTS_PASSWORD, and CLASSCHARTS_CODE environment variables when credentials are needed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
