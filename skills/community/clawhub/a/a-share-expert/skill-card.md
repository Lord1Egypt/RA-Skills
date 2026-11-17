## Description:

A-share China stock trading decision expert that integrates stock-data MCP servers and structured workflows for Shanghai and Shenzhen main-board analysis, screening, portfolio review, intraday scanning, theme-launch hunting, and stop-loss discipline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoze-hub](https://clawhub.ai/user/xiaoze-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for Chinese A-share trading decision support. It routes stock questions through data-source selection, current-price checks, scenario-specific analysis, and risk-discipline checklists for Shanghai and Shenzhen main-board positions and candidates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading suggestions could be mistaken for automatic trade instructions.

Mitigation: Do not allow the skill to place trades automatically; require user review for buy/sell decisions and position sizing.

Risk: Scheduled checks, IM pushes, or online documents may expose holdings or trade plans if enabled without consent.

Mitigation: Require explicit approval before enabling scheduled checks, IM pushes, or online documents containing holdings or trade plans.

Risk: Market data can be stale, unavailable, or inconsistent across trading windows.

Mitigation: Use real-time tick checks for current-price decisions, follow the documented fallback order, and disclose data unavailability rather than fabricating values.

Risk: Generated numeric analysis may be misleading if figures are invented or altered.

Mitigation: Base numeric conclusions on verified data snapshots and keep reported figures aligned with tool outputs.

## Reference(s):

- [Discipline Execution Framework](references/discipline-execution.md)
- [MCP Coordination Strategy](references/mcp-coordination-strategy.md)
- [MCP Fallback Matrix](references/mcp-fallback-matrix.md)
- [Multi-Agent Decision Framework](references/multi-agent-decision-framework.md)
- [Seven Scenario Workflow](references/scenarios-7-flow.md)
- [Theme-Launch Hunting Framework](references/theme-launch-hunting.md)
- [Trading Rules Essentials](references/trading-rules-essentials.md)
- [TradingAgents GitHub](https://github.com/TauricResearch/TradingAgents)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with tables, checklists, tool-call plans, code snippets, and shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trading guidance should remain decision support, with user review required before buy/sell, position-sizing, scheduled checks, IM pushes, or online documents.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
