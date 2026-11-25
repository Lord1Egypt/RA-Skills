## Description:

Adversarially review a code change before it ships with a single-agent severity-graded review, an optional three-agent Writer/Breaker/Reviewer pipeline, or an optional five-agent pipeline with a fix loop and browser verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to find correctness, security, and complexity issues in code changes before merge. It supports a focused single-agent review as well as optional multi-agent workflows that produce findings and a human-readable verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two unresolved references in SKILL.md left some evidence incomplete in the partial security review.

Mitigation: Review the skill’s instructions and referenced material before relying on it.

## Reference(s):

- [Three-Agent Pipeline](artifact/references/three-agent-pipeline.md)
- [Five-Agent Pipeline](artifact/references/five-agent-pipeline.md)
- [Review Checklists](artifact/references/review-checklists.md)
- [Rails Review Checks](artifact/references/rails-review-checks.md)
- [Rails System Spec Review](artifact/references/rails-system-spec-review.md)
- [Rails Turbo and Controller Traps](artifact/references/rails-turbo-and-controller-traps.md)
- [Rails Money and State Checks](artifact/references/rails-money-and-state-checks.md)
- [ClawHub Skill Release](https://clawhub.ai/djc00p/skills/adversarial-review-pipeline)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown review reports with severity-graded findings, scope notes, and a verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report identifies verified areas and skipped areas when applicable.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
