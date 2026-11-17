## Description:

分析用户指定的普通方法、HTTP 接口方法或 RPC 方法，说明用途与流程、涉及的数据库表及引用它的服务。默认使用当前仓库范围的快速模式；用户明确要求标准模式时才展开下游链路和跨服务搜索。

This skill is ready for commercial/non-commercial use.

## Publisher:

[extraskittles](https://clawhub.ai/user/extraskittles)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this Chinese-language skill to perform read-only analysis of a specified function, HTTP API method, or RPC method. It summarizes the method purpose and flow, involved database tables, and direct service or module references from code evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may summarize proprietary local code because it is intended to analyze user-specified repository methods.

Mitigation: Review generated reports before sharing them outside the intended audience.

Risk: Implicit invocation is enabled, so an agent may select the skill for code-analysis requests without an explicit skill name.

Mitigation: Confirm the selected analysis scope and mode before relying on or distributing the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/extraskittles/skills/analyze-code)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Chinese Markdown report with code file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis; quick mode is the default and standard mode is used only when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
