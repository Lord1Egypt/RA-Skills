## Description:

财务分析入门工具 helps agents perform single-company valuation modeling, financial ratio analysis, cash-flow review, peer comparison, and financial risk assessment from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as individual investors, junior analysts, and finance students use this skill to analyze one company at a time, build basic DCF and comparable-valuation views, assess ratios, and summarize financial risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial conclusions may be misleading when source data is incomplete, stale, unaudited, or poorly formatted.

Mitigation: Use official filings or trusted financial data, check assumptions, and review generated ratios, valuation ranges, and risk ratings before relying on them.

Risk: The skill discloses local read, write, and command execution capabilities when those tools are enabled.

Mitigation: Limit the workspace to financial data intended for analysis and approve generated scripts, commands, and file writes deliberately.

Risk: Optional external financial data APIs may require credentials.

Mitigation: Provide credentials through environment variables only when needed and avoid placing secrets in prompts, generated files, or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/accounting-finance-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with structured tables, text summaries, YAML configuration examples, and command examples when local execution is enabled]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or write local analysis files and execute approved local commands when the agent enables those tools.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
