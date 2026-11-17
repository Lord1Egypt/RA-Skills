## Description:

金融数据终端 helps agents aggregate and analyze multi-asset financial data, produce structured finance reports, and support data visualization workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance teams use this skill for financial data analysis, report generation, statistical insight, visualization, and structured outputs across assets such as stocks, bonds, funds, futures, and foreign exchange.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill suspicious because the documentation expands from finance analysis into account access and transaction submission without clear scoping or user-control warnings.

Mitigation: Review before installing as a high-impact finance skill; use least-privilege, read-only credentials unless account access or transaction capability is explicitly intended.

Risk: Account-linked or money-moving actions could be triggered if an agent follows the transaction examples too broadly.

Mitigation: Require explicit user confirmation before any account-linked, alert-setting, or transaction-related action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/fin-terminal)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured finance-analysis results, configuration guidance, troubleshooting steps, and examples for API- or command-capable agents.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
