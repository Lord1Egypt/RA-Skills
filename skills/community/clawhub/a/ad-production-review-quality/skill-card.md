## Description:

审核质检技能 - 自动化质量评估和人工审核工作流

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Ad operations teams and developers use this skill to track automated quality checks, submit human review decisions, manage batches, resolve issues, and view review statistics for advertising materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated review scores and checks are mock/random and do not actually inspect advertising materials.

Mitigation: Use the skill as a prototype until real deterministic material checks are integrated and validated against the review criteria.

Risk: Large or malformed review submissions could corrupt statistics or exhaust the skill process because batch state changes are weakly validated.

Mitigation: Add input validation, score bounds, authorization checks, and batch-size limits before using it in production approval or compliance workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeyeshield/skills/ad-production-review-quality)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON command responses with human-readable status messages and review events]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains in-process review state; automated scores are mock/random according to security evidence.]

## Skill Version(s):

1.0.0 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
