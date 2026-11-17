## Description:

Assesses code migration and refactoring risks, maps affected components, and produces practical action plans for developers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to assess PR, repository, or release migration risks, understand impacted modules, and plan refactoring work before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis may require access to private or sensitive code through GitHub credentials.

Mitigation: Use a least-privilege GitHub token scoped only to the repositories needed for the assessment.

Risk: Generated refactoring plans or diffs may be incomplete or unsuitable for the target codebase.

Mitigation: Review the generated plan or diff before applying changes and validate it with the project's normal tests and code review process.

Risk: The workflow and primary artifact text are in Chinese, which may affect operator understanding.

Mitigation: Install and use it only when the operator is comfortable with a Chinese-language workflow or has the output reviewed by someone who is.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-code-migration-risk-assessor)
- [Publisher profile](https://clawhub.ai/user/zlszhonglongshen)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown risk report with prioritized findings, affected-module list, and refactoring action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference GitHub PRs, repositories, diffs, P0-P3 risk levels, suggested code changes, and GITHUB_TOKEN access.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
