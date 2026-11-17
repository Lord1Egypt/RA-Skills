## Description:

专为初高中生打造的中文学习导师 Skill，用于学科知识问答、解题辅导、课本原文引用和教师式学习回应。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatif146](https://clawhub.ai/user/whatif146)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and tutoring agents use this skill to answer Chinese middle- and high-school study questions, guide students through exercises, cite available study materials, and adapt responses to the learner's tone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generic Chinese-language triggers may activate the skill when tutoring behavior is not intended.

Mitigation: Review trigger behavior in the target agent and narrow activation criteria if the workspace has many unrelated Chinese-language conversations.

Risk: Uploaded textbook or worksheet content may be indexed for tutoring within the skill's workflow.

Mitigation: Avoid uploading sensitive or restricted materials unless the agent environment's content handling and retention policies are acceptable.

Risk: Tutoring responses can be incorrect or overconfident when the included knowledge files do not cover a topic.

Mitigation: Ask the agent to cite available source material and flag when additional references are needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whatif146/skills/chinese-student-tutor)
- [Clawdis Homepage](https://github.com/yooyoo)
- [数学知识点汇总](references/textbooks/math.md)
- [物理知识点汇总](references/textbooks/physics.md)
- [化学知识点汇总](references/textbooks/chemistry.md)
- [语文知识点库](references/textbooks/chinese.md)
- [英语知识点库](references/textbooks/english.md)
- [典型例题与习题库](references/exercises/typical-problems.md)
- [教学技巧指南](references/teaching-tips.md)
- [回复模板库](references/response-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown tutoring responses with structured sections, citations to available study material, worked steps, and practice prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; responses may depend on user-provided textbook, worksheet, or image content.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
