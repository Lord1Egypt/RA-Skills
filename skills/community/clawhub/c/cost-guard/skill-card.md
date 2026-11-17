## Description:

Cost Guard helps an agent optimize prompts, estimate credit cost, intercept high-cost patterns, and suggest lower-cost alternatives before expensive tasks are executed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenqi123123](https://clawhub.ai/user/liuwenqi123123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users can use this skill to add cost-aware checkpoints before file processing, batch generation, multi-step agent workflows, and other requests likely to consume many credits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may interrupt credit, file-processing, failed-task, or vague-task conversations more often than some users expect.

Mitigation: Narrow triggers or use the skill only for workflows where frequent cost checks and confirmation gates are desired.

Risk: Cost estimates and savings percentages are guidance, not guaranteed billing outcomes.

Mitigation: Review estimates before acting and confirm high-cost paths when the skill requests approval.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured diagnostics, cost estimates, risk gates, and recommended execution paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for confirmation before high-risk or ambiguous work proceeds.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
