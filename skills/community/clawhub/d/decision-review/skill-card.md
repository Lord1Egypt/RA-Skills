## Description:

Helps users review decisions or events with a structured retrospective covering background, expectations, actions, outcomes, lessons, root causes, improvements, and reusable principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn a completed project, failed decision, incident, or regular review into an actionable AAR-style retrospective. It guides the user from facts and expectations through root-cause analysis, concrete improvements, and reusable decision principles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrospectives may contain confidential work, personal, or business details.

Mitigation: Review sensitive inputs before use and write retrospective output only to an explicit, intended local path.

Risk: The learner feature can retain notes, errors, and preferences in local learned_patterns.json files.

Mitigation: Avoid learner and preference commands unless local retention is acceptable, and periodically review or remove learned_patterns.json where retention is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/decision-review)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and generated retrospective files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write retrospective Markdown to a user-specified output path and can store local learned_patterns.json data when learner features are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
