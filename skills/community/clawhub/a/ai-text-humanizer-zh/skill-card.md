## Description:

中文AI文本检测与改写工具。当用户需要检测AI生成文本、优化AI文本使其更自然、降低AI痕迹、文本去重、论文降重时使用。支持检测16+类AI特征，自动改写冗余表达，清理Markdown格式，移除chatbot痕迹，输出详细报告和AI概率分数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[runze123](https://clawhub.ai/user/runze123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, editors, and Chinese-language content reviewers use this skill to detect rule-based AI-writing signals, clean Markdown and chatbot artifacts, and rewrite text for more natural wording. It is most appropriate as an editing aid where users will review the transformed text before publication or submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is explicitly designed to reduce AI-detection signals and remove AI-origin traces, which can support misrepresentation of authorship or policy evasion.

Mitigation: Use it for transparent editing and proofreading only; preserve required authorship and provenance disclosures and follow applicable academic, workplace, and platform rules.

Risk: Rule-based detection and rewriting may miss complex AI-writing patterns or remove meaningful content during transformation.

Mitigation: Treat reports and rewritten text as review aids; manually review outputs before publication or submission, especially for academic, legal, or professional content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/runze123/skills/ai-text-humanizer-zh)
- [Publisher profile](https://clawhub.ai/user/runze123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, rewritten text, JSON-compatible detection reports, and file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python standard-library scripts can read from files or stdin, write transformed text to files, and accept custom JSON rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
