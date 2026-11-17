## Description:

自动生成工作日报和周报，分析 git 提交记录、TODO 注释和工作日志来生成结构化 Markdown 工作报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[flonerze](https://clawhub.ai/user/flonerze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare daily, weekly, or custom-range work reports from repository activity, TODOs, and work notes for standups, manager updates, and progress reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include sensitive project details from git commit messages, TODO comments, task files, or work notes.

Mitigation: Review the local report before sharing and redact confidential project, customer, credential, or planning details.

Risk: Intermediate local files or report outputs may remain on shared machines.

Mitigation: Use a private temporary directory for report generation on shared systems and delete intermediate files after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flonerze/skills/daily-report-and-weekly-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown report files and optional HTML conversions; users should review generated reports before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
