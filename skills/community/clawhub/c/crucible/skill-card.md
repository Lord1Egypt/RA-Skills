## Description:

Crucible orchestrates a configurable product delivery pipeline from PM and UX through development, testing, and acceptance gates, with implement-review-fix loops for staged quality control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yvancheng](https://clawhub.ai/user/yvancheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and product teams use Crucible to turn raw product requests into staged deliverables through PM, UX, development, test, and acceptance gates. It also supports narrower development, review-only, and parallel API-contract-check workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad development automation that creates or changes code, documentation, tests, and review reports.

Mitigation: Review proposed file changes, generated commands, and gate reports before accepting or executing them in a project.

Risk: Reference guidance includes optional unpinned global npm installation.

Mitigation: Skip optional global installs unless needed, and pin or review packages before installing them.

Risk: Workflow guidance may lead to dependency installs, git merges, pushes, or pull-request creation.

Mitigation: Require explicit user confirmation before dependency installation or any git operation that publishes, merges, or opens a pull request.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yvancheng/skills/crucible)
- [README](README.md)
- [Methodology](skill/references/methodology.md)
- [Verification](skill/references/verification.md)
- [Security Checklist](skill/references/security-checklist.md)
- [Tooling](skill/references/tooling.md)
- [Lessons](skill/references/lessons.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and generated project artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify project documentation, source code, tests, and review reports depending on the selected pipeline mode.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
