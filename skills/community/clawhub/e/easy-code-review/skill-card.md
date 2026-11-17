## Description:

Reviews AI-generated code changes for requirement alignment, unnecessary file modifications, code quality issues, and change impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanghao-smile](https://clawhub.ai/user/yanghao-smile)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review AI-modified code against the original requirement, identify unnecessary file changes, assess code quality, and understand likely change impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags review-worthy risk around unverified CI installation examples and broad write or process authority.

Mitigation: Install only when repository read and git inspection access are acceptable, and pin and verify any installer used in CI before execution.

Risk: The skill declares file.write even though the current evidence indicates report-writing authority may be broader than needed.

Mitigation: Prefer a version that removes file.write or clearly scopes report-writing behavior; otherwise run it in repositories where report output writes are expected.

Risk: Review findings are advisory and can misclassify requirement alignment, security, dependency, or configuration risk.

Mitigation: Require maintainer review before applying recommendations, especially for dependency, configuration, security, or broad refactoring findings.

## Reference(s):

- [Review Guidelines](references/review-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/yanghao-smile/skills/easy-code-review)
- [Publisher Profile](https://clawhub.ai/user/yanghao-smile)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Markdown reports by default, with documented JSON and HTML report options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect git diffs and repository files to produce review findings, risk levels, and improvement suggestions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
