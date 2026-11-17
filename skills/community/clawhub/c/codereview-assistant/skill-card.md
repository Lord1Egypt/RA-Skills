## Description:

Code review best practices and workflow skill for reviewing pull requests, setting review standards, improving code quality processes, and producing checklists, comment guidance, approval criteria, and severity classifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydpz](https://clawhub.ai/user/sydpz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to structure pull request reviews, classify findings by severity, write actionable review comments, and decide whether changes are ready to approve or should be revised.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad code-quality or linting discussions where a full pull request review workflow is not the user's intent.

Mitigation: Treat the output as an advisory checklist and confirm that the review workflow is relevant to the current task before applying it.

Risk: Review guidance can miss project-specific conventions, policies, or automated tool findings.

Mitigation: Use the checklist alongside repository standards, tests, linters, type checkers, SAST scanners, and reviewer judgment.

## Reference(s):

- [Code Review Checklist](references/review-checklist.md)
- [Severity Classification](references/severity-classification.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review checklists, severity labels, decision criteria, and reusable review comment templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; no code execution, persistent access, credential access, or destructive behavior is described in the security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
