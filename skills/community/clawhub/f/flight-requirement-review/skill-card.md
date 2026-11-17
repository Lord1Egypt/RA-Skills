## Description:

机票产品需求评审 Agent 对中文机票前端、后端、运营类需求文档进行结构化评审打分，并对流程图和逻辑建模给出独立评分、评语与改进建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[arisefx](https://clawhub.ai/user/arisefx)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, designers, QA reviewers, and engineering reviewers use this skill to assess Chinese-language flight PRDs, prototypes, flowcharts, and HTML or Markdown requirements for completeness, scoring, and actionable improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is specialized for Chinese-language flight product requirement reviews and may activate on broad Chinese requirement-review phrases.

Mitigation: Invoke it with explicit flight PRD context and confirm the reviewed document matches the skill's intended domain before relying on the output.

Risk: Review reports can be incomplete or misleading when the input PRD, prototype, image, or HTML omits business, security, compliance, or dependency details.

Mitigation: Have product, engineering, QA, and security or compliance reviewers validate scores and required changes before using the report for implementation decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arisefx/skills/flight-requirement-review)
- [Skill Definition](artifact/SKILL.md)
- [Review Standards](artifact/review-standards.md)
- [Technical Document Template](artifact/tech-doc-template.md)
- [Example Review](artifact/example-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown review report with scoring tables, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can also produce an AI-friendly technical document when the user requests conversion after review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
