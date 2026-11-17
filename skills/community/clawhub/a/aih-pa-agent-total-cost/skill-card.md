## Description:

Helps users estimate personal-agent costs from actual model prices, runtime and tool fees, and accepted task counts, producing a cost table, budget ceiling, and route comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and developers planning a personal AI assistant use actual prices and task outcomes to compare implementation routes, calculate cost per accepted task, and set budget alerts. Optional AI-HIVE access requires user authorization and available tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified prices, mixed currencies, or retry fees may produce misleading budgets or unexpected charges.

Mitigation: Confirm current prices, currency, retry costs, and spending limits before paid or bulk activity; begin with a small sample.

Risk: Account authorization or uploading sensitive materials can expose more information than intended.

Mitigation: Authorize AI-HIVE through its official login or MCP flow, confirm upload scope, and never paste passwords, tokens, cookies, verification codes, or full identity documents into the workflow.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-agent-total-cost)
- [Cost-planning workflow and acceptance criteria](references/workflow-46.md)
- [Result and evidence contract](references/output-contract.md)
- [AI-HIVE authorization and use](references/ai-hive-connection.md)
- [Scope and product sources](references/scope-and-sources.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance]

**Output Format:** [CSV cost table and text or Markdown budget ceiling and route comparison]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses sourced prices and task counts; leaves unknown values explicit and does not calculate cost per accepted task when none qualify.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
