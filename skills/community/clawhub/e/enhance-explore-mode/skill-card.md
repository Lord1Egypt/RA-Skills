## Description:

深度探索模式 - 系统性调研代码库、系统或话题，只读不改，借鉴 Claude Code 的 Explore Agent。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to investigate unfamiliar codebases, systems, or implementation questions before answering. It guides a read-only exploration workflow that scans broadly, follows relevant details, and returns a structured exploration report with file references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect repository files and git history that contain sensitive material.

Mitigation: Use it only in workspaces where read-only code and history review is appropriate, and give the agent a clear exploration scope.

Risk: Exploration reports can include mistaken conclusions if the agent reviews too narrow a slice of the system.

Mitigation: Require cross-checking across relevant files, tests, and call paths, and distinguish observed facts from inference in the report.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jobzhao15/skills/enhance-explore-mode)
- [Skill Homepage](https://github.com/jobzhao15/openclaw-enhance)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown exploration report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include concise findings, direct answers, recommendations, and file paths or line references when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
