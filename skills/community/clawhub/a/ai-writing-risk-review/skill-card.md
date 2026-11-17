## Description:

评估文章、作业、公众号稿、报告、评论、邮件或任意文本的 AI 写作、AI 辅助润色、人机混写或模板化写作风险，并输出证据化、克制、非定罪式判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacktian89](https://clawhub.ai/user/zacktian89)

### License/Terms of Use:

MIT-0

## Use Case:

External users, reviewers, educators, editors, and developers can use this skill to assess whether supplied text shows AI-generated, AI-assisted, mixed-authorship, or template-like writing risk. It supports evidence-based reports with risk level, evidence strength, sample limits, counter-explanations, and follow-up evidence or revision suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a heuristic AI-writing risk assessment as proof of authorship, misconduct, or intent.

Mitigation: Present results as evidence-weighted risk signals and require additional evidence such as drafts, sources, revision history, or human review for high-stakes decisions.

Risk: Short, translated, heavily edited, collaborative, or highly templated text can make AI-writing assessment unreliable.

Mitigation: State sample limits, evidence strength, and counter-explanations in the report before assigning a risk level.

Risk: Revision guidance could be misused as advice to evade AI detectors.

Mitigation: Frame suggestions around clearer expression, stronger sources, revision records, author judgment, and higher information density rather than detector evasion.

## Reference(s):

- [AI 写稿检测方法速览](artifact/references/ai-detection-methods.md)
- [AI 写稿评估报告模板](artifact/references/evaluation-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown risk assessment report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs heuristic risk levels, evidence strength, sample limitations, supporting evidence, counter-explanations, and follow-up guidance; scores are not probabilities.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
