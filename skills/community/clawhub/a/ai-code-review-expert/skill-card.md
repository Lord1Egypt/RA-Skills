## Description:

Reviews submitted code snippets and diffs for defects, security issues, performance, and style, then drafts actionable feedback and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Software engineers, technical leads, and maintainers use the skill to review submitted code snippets or diffs, identify issues, and prepare draft review comments and fix suggestions for human assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A partial scan reported a possible mismatch between the code-review purpose and database access, and left some local references unresolved.

Mitigation: Before installing, confirm whether the reported database access fits your intended use; treat the benign verdict as medium-confidence and incomplete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gechengling/skills/ai-code-review-expert)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Code]

**Output Format:** [Markdown review comments with severity, explanations, suggested code snippets, and quality scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory drafts for human review; does not execute code, modify repositories, run CI, or connect to code hosting platforms.]

## Skill Version(s):

3.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
