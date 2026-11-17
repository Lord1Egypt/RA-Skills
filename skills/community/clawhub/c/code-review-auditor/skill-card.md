## Description:

Review codebases for bugs, security issues, architecture/SOLID problems, code smells, justified design-pattern opportunities, anti-patterns, performance, observability, testability, hotspots, and planned refactors without changing code during analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbbathaglini](https://clawhub.ai/user/cbbathaglini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run structured reviews of repositories, diffs, architecture, security posture, tests, performance, maintainability, hotspots, and refactor plans. It helps produce evidence-led findings and review artifacts while keeping analysis modes read-only for project source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each run creates a local review/<timestamp>/ directory and records basic repository metadata.

Mitigation: Ignore, clean, or review generated report files before committing them.

Risk: Fix and refactor modes can lead to code changes when the user approves or already requested implementation.

Mitigation: Use those modes only when code changes are intended, and review the generated refactoring plan before implementation.

## Reference(s):

- [Code Review Auditor on ClawHub](https://clawhub.ai/cbbathaglini/skills/code-review-auditor)
- [Review Process Reference](references/review-process.md)
- [Refactor Planning Reference](references/refactor-planning.md)
- [Reporting Examples](references/reporting-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, guidance]

**Output Format:** [Markdown reports, JSON score and metadata files, code sketches, and shell commands when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped local review package with summaries, findings, category reports, hotspots, metrics, metadata, and refactoring plans.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
