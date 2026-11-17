## Description:

Summarize audit findings into a structured multi-dimensional scorecard for UI/UX, feedback, mechanics, scope completeness, maintainability, and live risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike007jd](https://clawhub.ai/user/mike007jd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to convert game audit findings into consistent scorecards and summaries. It is intended for assessing browser or project-based games across UX, feedback, mechanics, production readiness, maintainability, and live risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated audit scores or summaries may be incomplete or misleading if runtime evidence is limited.

Mitigation: Review the generated audit files before relying on them, and require clear evidence and confidence notes for important findings.

Risk: Using shell or build access to gather evidence can broaden what the agent can inspect or change in a project.

Mitigation: Install and run the skill only in the game project being assessed, with access limited to the intended workspace.

## Reference(s):

- [Game Audit Scorecard on ClawHub](https://clawhub.ai/mike007jd/skills/game-audit-scorecard)
- [Audit Scorecard Schema](schemas/audit-scorecard.schema.json)
- [Audit Confidence and Evidence](shared/reference/audit-confidence-and-evidence.md)
- [Audit Scorecard Template](shared/templates/audit-scorecard.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON scorecard and Markdown audit summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates docs/game-studio/audit/scorecard.json and docs/game-studio/audit/audit-summary.md when used in a project.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
