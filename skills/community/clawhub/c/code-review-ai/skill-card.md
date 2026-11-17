## Description:

代码审查助手 - 自动分析代码，提供审查意见、性能优化建议、安全漏洞检测。支持多种编程语言，生成详细的代码审查报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to request automated code review, performance suggestions, security issue detection, and Markdown review reports across supported programming languages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact references node scripts/review.mjs, but the inspected release does not include that script, so the skill may be incomplete or nonfunctional.

Mitigation: Confirm the installer supplies scripts/review.mjs or add the script before relying on the review commands.

Risk: The documentation and examples are primarily in Chinese.

Mitigation: Install only where Chinese-language documentation is acceptable for reviewers and operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-wuxl/skills/code-review-ai)
- [Publisher profile](https://clawhub.ai/user/ryan-wuxl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node; the referenced review script is not included in the inspected artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
