## Description:

データ分析プロジェクトのためのOpenClawワークスペース設定テンプレート。データ駆動の意思決定、探索的データ分析（EDA）、モデル開発の原則。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hirofumiko](https://clawhub.ai/user/hirofumiko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill as an OpenClaw workspace starter template for data-analysis agents. It provides reusable SOUL, IDENTITY, AGENTS, USER, and HEARTBEAT templates for EDA, model development, experiment tracking, reporting, and reproducible analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workspace template grants broad persistent memory and bootstrap authority.

Mitigation: Review and edit AGENTS.md before use; constrain the BOOTSTRAP.md rule, require confirmation for memory-derived actions and cleanup, avoid storing secrets in TOOLS.md, and periodically review persistent memory files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hirofumiko/skills/fumi-data-analysis-workflow)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown templates with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace setup templates and guidance; users customize the generated markdown files before relying on them.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog released 2026-03-19, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
