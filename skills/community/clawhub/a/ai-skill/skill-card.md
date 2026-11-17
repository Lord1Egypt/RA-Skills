## Description:

Enables agents to create and trade prediction-market shares, query positions and trade history, and generate automated trading signals for ClawMarkets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[watchmer20-ctrl](https://clawhub.ai/user/watchmer20-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to a configured ClawMarkets API, create prediction markets, place buy and sell orders, inspect positions and trades, and evaluate momentum, value, and arbitrage strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create prediction markets and place buy or sell orders through a configured API.

Mitigation: Use a sandbox or paper-trading endpoint first, require human approval for live orders, and enforce spending and position limits outside the skill.

Risk: API-key handling and endpoint configuration can expose credentials or route orders to untrusted services.

Mitigation: Restrict API-key permissions, store credentials outside prompts and source files, and allow only trusted HTTPS endpoints for live use.

Risk: Automated trading loops and strategy signals may execute incorrect or unwanted trades if used without oversight.

Mitigation: Keep unattended loops disabled for live trading unless external monitoring, limits, audit logging, and approval gates are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/watchmer20-ctrl/skills/ai-skill)
- [Publisher profile](https://clawhub.ai/user/watchmer20-ctrl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose API calls, trading actions, strategy signals, and unattended trading loops; live execution should require external controls and approval.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
