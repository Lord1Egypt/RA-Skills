## Description:

Agent Stock Pro helps agents screen Chinese stock candidates, analyze holdings, make short-term trading decisions, generate PDF reports, and track a simulated portfolio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tompchen](https://clawhub.ai/user/tompchen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen A-share stock candidates, evaluate individual stocks and holdings, produce short-term trading guidance, generate PDF reports, and maintain a simulated portfolio for strategy tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install package dependencies in the agent environment.

Mitigation: Review installation steps and require explicit user confirmation before running package installs.

Risk: The skill stores financial analysis outputs and simulated portfolio state locally.

Mitigation: Run it only in workspaces where local financial record retention is acceptable, and review generated dist/ files before sharing.

Risk: The strategy tracking workflow mutates simulated portfolio state and records simulated buy or sell activity.

Mitigation: Require confirmation before scheduled runs, simulated trades, or portfolio state updates.

Risk: The workflow can send generated PDF financial reports externally.

Mitigation: Require explicit confirmation before sending PDFs or other report artifacts through messaging tools.

## Reference(s):

- [Agent Stock Pro ClawHub page](https://clawhub.ai/tompchen/skills/agent-stock-pro)
- [Original Agent Stock skill](https://clawhub.ai/anoyix/agent-stock)
- [Holdings analysis workflow](references/holdings.md)
- [Quantitative trading decision workflow](references/quant.md)
- [Quantitative scoring rules](references/quant_rule.md)
- [Stock screening workflow](references/screen.md)
- [Strategy tracking workflow](references/strategy-track.md)
- [Trade decision workflow](references/trade.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON portfolio state, PDF report artifacts, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write analysis reports under dist/, update simulated portfolio JSON, and send generated PDF reports when the host provides a messaging tool.]

## Skill Version(s):

0.4.0 (source: server evidence, SKILL.md frontmatter, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
