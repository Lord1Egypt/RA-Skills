## Description:

全流程指导高考作文写作，覆盖审题立意、结构搭建、素材推荐、语言润色、评分预测与诊断改进。

This skill is ready for commercial/non-commercial use.

## Publisher:

[njuxumq](https://clawhub.ai/user/njuxumq)

### License/Terms of Use:

MIT-0

## Use Case:

External students, repeat test takers, and Chinese language teachers use this skill to plan Gaokao essays, refine structures and materials, generate study examples, and diagnose existing drafts against Gaokao scoring criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnosis workflow can read an essay file supplied through --file, so an unintended sensitive file could be processed if the user points to the wrong path.

Mitigation: Use --essay for pasted drafts when possible, or point --file only at the intended essay document.

Risk: Broad trigger terms may activate the skill during general Chinese writing conversations.

Mitigation: Confirm the user is asking for Gaokao essay coaching before applying the specialized scoring, structure, and material guidance.

Risk: Generated model essays are for study; direct reuse can create plagiarism or template-writing concerns.

Mitigation: Use generated examples to learn structure and technique, then revise with the student's own argument, language, and materials.

## Reference(s):

- [Gaokao Essay Guide on ClawHub](https://clawhub.ai/njuxumq/skills/gaokao-essay-guide)
- [Server-Resolved GitHub Repository](https://github.com/njuxumq/gaokao-essay-guide)
- [高考作文评分标准与阅卷细则](references/scoring-criteria.md)
- [高考作文写作方法论](references/writing-methodology.md)
- [高考作文素材库](references/essay-materials.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown prose with optional JSON script output and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; local Python scripts can process essay text from --essay or an essay file from --file.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
