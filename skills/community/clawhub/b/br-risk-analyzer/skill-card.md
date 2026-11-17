## Description:

Analyzes code changes between commits against requirement documents to identify and prioritize risk points.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhijialin](https://clawhub.ai/user/zhijialin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare scoped code changes against requirement or design documents, produce prioritized P0-P3 risk findings, and suggest test scenarios for high-risk issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read the target repository and write persistent project analysis or report files.

Mitigation: Review proposed file changes before allowing persistence, and restrict report writes to a fixed, sanitized output path.

Risk: Generated risk findings can be incomplete, speculative, or misleading if requirements, scope, or repository access are unclear.

Mitigation: Require explicit requirements, scoped paths or branches, and human review of each finding before acting on recommendations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhijialin/skills/br-risk-analyzer)
- [README](README.md)
- [Project Understanding](resources/project-understanding.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown risk report with prioritized tables and optional testing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports as requirement-specific risk-analyzer Markdown files and update persistent project understanding when permitted.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
