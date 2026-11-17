## Description:

A Chinese-language electrical machinery course assistant for answering course questions, generating practice exercises with explanations, and recommending teaching videos across DC machines, transformers, AC windings, induction machines, and synchronous machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External students and learners use this skill as a course assistant for electrical machinery study, including concept explanations, formula walkthroughs, chapter-based practice, mock quizzes, and video-resource recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Undisclosed web assets can load remotely changeable HTML.

Mitigation: Remove the remote loader or replace it with the packaged local UI; if remote loading remains necessary, pin the asset, add integrity checks, sandbox it, and disclose the behavior.

Risk: Learners may rely on incorrect or misleading educational answers or exercise explanations.

Mitigation: Review course content and generated responses before using them for graded work, exams, or official instruction.

Risk: The web UI may receive sensitive learner input while remote asset behavior is unresolved.

Mitigation: Avoid entering sensitive information into the UI until the remote-loading issue is fixed and reviewed.

## Reference(s):

- [Skill release page](https://clawhub.ai/smallkeyboy/skills/electrical-machinery-course)
- [电机学课程知识体系](references/knowledge-base.md)
- [电机学题库](references/question-bank.md)
- [电机学题库（548题）](references/question-bank-500.md)
- [电机学教学视频资源索引](references/video-resources.md)
- [中国大学MOOC](https://www.icourse163.org)
- [Bilibili](https://www.bilibili.com)
- [网易公开课](https://open.163.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown conversational responses with formulas, tables, quiz questions, answers, explanations, and video recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use bundled course notes, question banks, and video index files as grounding material.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
