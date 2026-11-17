## Description:

生成专业的芯片（CPU/显卡/GPU）技术分析文档，包含架构解析、性能评测、功耗分析、性价比评估等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hwl1413520](https://clawhub.ai/user/hwl1413520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, hardware reviewers, and PC buyers use this skill to create Chinese-language CPU and GPU analysis reports covering specifications, architecture, benchmarks, power, thermals, value, and buying guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardware prices, availability, driver behavior, and benchmark results change over time, so generated recommendations can become stale or misleading.

Mitigation: Use current official specifications and reputable benchmark sources, and include the analysis date and source list in generated reports.

Risk: Running the included Python helper directly may create a local JSON analysis file in the working directory.

Mitigation: Run the helper only in an expected workspace and review generated files before sharing or committing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hwl1413520/skills/chip-tech-analyzer)
- [芯片规格数据库](references/CHIP_DATABASE.md)
- [芯片评测标准指南](references/BENCHMARK_GUIDE.md)
- [技术分析报告模板](assets/templates/analysis_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown report with optional JSON data export and document or table conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow; may rely on current public hardware data and can create a local JSON analysis file when the Python helper is run.]

## Skill Version(s):

1.0.0 (source: server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
