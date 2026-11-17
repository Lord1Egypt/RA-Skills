## Description:

Code Reviewer helps agents review code conventions, potential bugs, performance issues, and security vulnerabilities, then produce prioritized improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiyan521](https://clawhub.ai/user/shiyan521)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to request structured code reviews before release, with P0/P1/P2 findings and remediation suggestions for quality, performance, and security issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad review requests may expose or inspect sensitive repository areas beyond the user's intent.

Mitigation: Scope reviews to explicit files or modules for sensitive repositories, and exclude secrets or private data from the review set.

Risk: Review findings and remediation advice may be incomplete or incorrect.

Mitigation: Treat the report as reviewer guidance and verify proposed fixes with maintainers, tests, and security checks before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiyan521/skills/07-code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown code review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prioritized P0/P1/P2 findings with required remediation for P0 issues.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
