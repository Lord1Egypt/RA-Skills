## Description:

双语学习 Skill - CN → EN。当用户使用此 skill 时，agent 会在最终输出前强制进行双语学习处理，包括难度调整、考试检测和双语输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haodong-lei-ray](https://clawhub.ai/user/haodong-lei-ray)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add passive CN-to-EN vocabulary learning into agent conversations, including bilingual phrasing, vocabulary checks, spelling quizzes, and local word-list management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or clear local vocabulary records.

Mitigation: Back up word-list files before using delete, exchange, or clear operations.

Risk: The skill may mix bilingual learning content into responses where exact formatting or single-language output is required.

Mitigation: Do not enable the skill for tasks that require strict output formats or single-language responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haodong-lei-ray/skills/bilingual-learning)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with optional JSON-backed local vocabulary records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local new_words.json and known_words.json vocabulary files when word-management commands are used.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
