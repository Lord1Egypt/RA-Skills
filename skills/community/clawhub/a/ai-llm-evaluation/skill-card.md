## Description:

A hands-on guide and local toolkit for defining LLM quality metrics, building evaluation sets, assessing RAG and hallucination behavior, running prompt regression checks, comparing models, and preparing evaluation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers, QA engineers, product owners, and quality leaders use this skill to design repeatable quality evaluation and regression gates for LLM applications, including RAG systems, prompt updates, hallucination checks, and model selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real customer logs or production conversations used for evaluation sets may contain sensitive or unauthorized data.

Mitigation: Sanitize and de-identify source data before use, and confirm authorization for any production-derived evaluation samples.

Risk: Evaluation guidance can be misapplied as a substitute for actual model or application testing.

Mitigation: Connect the recommended metrics and templates to a real evaluation pipeline, calibrate any LLM-as-judge workflow, and keep human review for critical or ambiguous samples.

Risk: Evaluation set leakage or prompt overfitting can make regression scores misleading.

Mitigation: Keep evaluation sets separate from training, fine-tuning, and prompt tuning data; version datasets and refresh them with controlled production samples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-llm-evaluation)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)
- [01 评测全景与指标](references/01-评测全景与指标.md)
- [02 评测集构建](references/02-评测集构建.md)
- [03 RAG 系统评测](references/03-RAG系统评测.md)
- [04 幻觉检测与度量](references/04-幻觉检测与度量.md)
- [05 Prompt 回归测试](references/05-Prompt回归测试.md)
- [06 模型对比选型](references/06-模型对比选型.md)
- [07 评测流程与报告](references/07-评测流程与报告.md)
- [08 FAQ](references/08-FAQ.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python CLI output and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled toolkit is zero-dependency and local; evidence.security reports no hidden network access, credential access, persistence, or destructive behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
