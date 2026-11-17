## Description:

Trade prediction markets with natural language via Foreseek.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypegamer007](https://clawhub.ai/user/hypegamer007)

### License/Terms of Use:


## Use Case:

External users use this skill to ask an agent to find Kalshi prediction markets, inspect account and portfolio state, and prepare or execute market operations through Foreseek.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place or cancel prediction-market orders through a connected Kalshi account.

Mitigation: Require explicit user approval for every trade or cancellation, including ticker, side, action, contract count, order type, and live-versus-demo account status.

Risk: Account status, balances, positions, orders, and watchlists may be sent to an external Foreseek endpoint.

Mitigation: Use a scoped, revocable FORESEEK_API_KEY and install the skill only for agents that are allowed to access the user's Foreseek and Kalshi trading workflow.

Risk: The skill evidence does not include a license identifier.

Mitigation: Confirm license and terms before redistribution or deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hypegamer007/skills/foreseekai)
- [ClawHub Publisher Profile](https://clawhub.ai/user/hypegamer007)
- [Foreseek Website](https://foreseek.ai)
- [Foreseek Dashboard](https://foreseek.ai/dashboard)
- [Foreseek Documentation](https://foreseek.ai/docs)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FORESEEK_API_KEY and may operate on a connected Kalshi account.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
