## Description:

AI code generation and statistics tool for marking AI-authored and human-authored code, standardizing version commit messages, and reporting AI code ratios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgongrui](https://clawhub.ai/user/wgongrui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to mark generated and human-authored code with @ai/@human tags, calculate AI code ratios for changed files, generate standardized commit messages, and review historical contribution trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The commit workflow can stage and commit more repository files than it analyzes or shows to the user.

Mitigation: Use only in repositories where staging every eligible file is acceptable; inspect git status before confirming and avoid secrets, local config files, generated artifacts, or unrelated changes.

Risk: Git command failures may not be checked by the helper scripts before reporting a commit workflow result.

Mitigation: Review command output and verify the final repository state before relying on generated statistics or commit completion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wgongrui/skills/ai-code-stat-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown and text responses with inline code blocks, generated commit messages, and command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide Python and Git workflows that analyze changed files and create commits after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
