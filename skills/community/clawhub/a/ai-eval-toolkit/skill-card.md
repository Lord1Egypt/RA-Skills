## Description:

A local, zero-dependency LLM evaluation toolkit for creating JSONL evaluation sets, checking rule-based hallucination signals, computing simplified RAG metrics, comparing regressions, and producing launch-gate reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers, AI engineers, QA teams, and quality leads use this skill to run local evaluation workflows for LLM and RAG systems, including dataset checks, rule-based hallucination review, RAG scoring, regression comparison, and release gate reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the bundled security audit has copy-paste errors and should not be relied on as assurance for this package.

Mitigation: Use evidence.security as the authoritative security source and regenerate any security audit before relying on it for review or deployment.

Risk: The toolkit performs local file operations as part of evaluation workflows.

Mitigation: Run it on copies of evaluation data and provide explicit output paths, as recommended by the server security guidance.

Risk: The skill documentation and output are Chinese-first, which may affect review or operation in some environments.

Mitigation: Review the Chinese-first documentation and output before use in environments that require localized controls or English-only operational material.

Risk: Rule-based hallucination and simplified RAG metrics can miss issues or produce false positives.

Mitigation: Use results as a baseline quality signal and review flagged cases manually or upgrade to specialized evaluation frameworks for high-assurance production decisions.

## Reference(s):

- [01 工具链全景](references/01-工具链全景.md)
- [02 评测集管理](references/02-评测集管理.md)
- [03 幻觉检测引擎](references/03-幻觉检测引擎.md)
- [04 RAG 指标计算](references/04-RAG指标计算.md)
- [05 回归对比](references/05-回归对比.md)
- [06 报告与门禁](references/06-报告与门禁.md)
- [07 与平台工具衔接](references/07-与平台工具衔接.md)
- [08 常见问题 FAQ](references/08-FAQ.md)
- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-eval-toolkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSONL examples, and local tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline local execution; produces dataset templates, checks, scores, comparisons, and reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
