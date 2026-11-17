## Description:

AI测试工程师全生命周期技能集合，覆盖需求分析、测试设计、AI协作、自动化、执行监控、质量度量和专项测试7大阶段共48个测试技能模块，帮助测试人员生成和评审专家级测试用例、策略、报告和质量度量产物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, test leads, developers, and delivery teams use this skill to analyze requirements, design test strategies and test cases, plan automation, monitor execution, manage defects, and summarize quality metrics. It is especially suited to Chinese-language testing workflows that need structured templates and method-driven guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing outputs may be incomplete or misleading if used as final quality artifacts without review.

Mitigation: Treat generated test cases, strategies, scripts, and reports as templates and require qualified human review before relying on them.

Risk: Project requirements, defects, logs, or quality metrics may contain confidential data.

Mitigation: Avoid pasting confidential project data unless the deployment context and data handling controls are appropriate.

Risk: The dashboard template should be hardened before connecting it to live systems or imported data.

Mitigation: Render dynamic dashboard values as text or sanitize them before insertion, and review any data-source integration before production use.

## Reference(s):

- [Phase 1: 需求分析与测试策略](references/phase1-requirements.md)
- [Phase 2: 测试设计方法](references/phase2-design-methods.md)
- [Phase 3: 测试用例工程](references/phase3-testcase-engineering.md)
- [Phase 4: AI协作测试](references/phase4-ai-collaboration.md)
- [Phase 5: 自动化测试](references/phase5-automation.md)
- [Phase 6: 测试执行与监控](references/phase6-execution.md)
- [Phase 7: 质量度量与分析](references/phase7-quality-metrics.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, structured tables, templates, code snippets, shell commands, CSV, and HTML template files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be treated as reviewable templates; generated testing recommendations, scripts, and dashboards require human validation before production use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
