## Description:

为代理提供 A 股行情与财务数据读取指南，整合 Baostock/Akshare 数据源选择、代码格式、单位转换、缓存、错误处理、降级策略、研发费用和注册属地查询等实践。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoy168](https://clawhub.ai/user/zoy168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent workflows use this skill to choose and normalize A-share market and financial data sources, especially when working with Baostock and Akshare interfaces. It helps produce robust data retrieval guidance, code patterns, and fallback strategies for common A股 financial-data tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs the agent to persistently edit its own instruction file after trial-and-error.

Mitigation: Review or remove the self-update instruction before installation and keep the installed skill directory read-only during normal use.

Risk: The cache example may be reused without validating stock code, date, or frequency inputs.

Mitigation: Treat cache snippets as templates and validate stock-code, date, and frequency values before adapting them.

Risk: Financial-data interfaces and field names may change across Akshare/Baostock versions or become temporarily unavailable.

Mitigation: Validate columns and data-source availability before relying on generated retrieval guidance or code in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoy168/skills/astock-unified-financial)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include data-source selection advice, unit conversion rules, fallback chains, cache patterns, and validation reminders.]

## Skill Version(s):

2.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
