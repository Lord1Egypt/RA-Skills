## Description:

Code Review Gate runs a seven-category static review over git diffs and emits severity-ranked findings with a blocking result when Critical issues are found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill before merge or in CI/CD to pre-review code changes for functional correctness, security, performance, readability, maintainability, test coverage, and documentation consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed changes can be allowed when diff collection fails or the diff exceeds the configured line limit.

Mitigation: Treat the skill as advisory until git diff failures and oversized diffs fail closed in CI.

Risk: Skipped analysis or invalid line-limit settings can make the merge-blocking exit code unreliable.

Mitigation: Validate max-lines as a positive value and require explicit approval before skipped analysis is treated as passing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terr123123/skills/code-review-gate)
- [Project homepage](https://github.com/Terr123123/code-review-gate)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Guidance]

**Output Format:** [Terminal text, Markdown, or JSON report with an exit code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Severity-ranked findings across functional, security, performance, readability, maintainability, testing, and documentation checks; Critical findings produce a blocking gate result.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter version: 0.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
