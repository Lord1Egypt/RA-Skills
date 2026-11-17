## Description:

帮0编程基础的同学分析代码错误，支持查阅本地代码文件，追踪连锁错误。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuxin-bit](https://clawhub.ai/user/qiuxin-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, students, and beginners use this skill to understand code errors in plain Chinese, locate likely causes, identify chain-reaction failures, and receive copy-ready corrected code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask to read or receive local code files while debugging.

Mitigation: Only provide file paths or pasted code that the user is comfortable sharing with the agent.

Risk: Generated fixes or explanations could be incomplete or incorrect for the user's project.

Mitigation: Review the explanation and corrected code before applying it, especially when the affected code is business-critical.

## Reference(s):

- [Common errors reference](artifact/references/common_errors.md)
- [Chain reaction patterns reference](artifact/references/chain_reaction_patterns.md)
- [ClawHub skill page](https://clawhub.ai/qiuxin-bit/skills/code-error-explainer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with plain-language analysis and corrected code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language beginner-focused explanations; may include file locations, root-cause classification, prevention advice, and complete replacement code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
