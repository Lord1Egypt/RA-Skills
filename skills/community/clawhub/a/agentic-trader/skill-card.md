## Description:

Consent-gated autonomous trading agent for Robinhood agentic accounts with pluggable signal sources, long-options execution, and user-configured sizing; not investment advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[traderhc123](https://clawhub.ai/user/traderhc123)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to configure and run an autonomous options-trading agent connected to their own Robinhood agentic account, using manual commands, a JSON feed, or AgentHC signal sources. Users remain responsible for consent, position sizing, broker permissions, and stopping the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path uses a one-line curl-to-bash installer that can execute mutable remote shell code before the trading consent gate protects the user.

Mitigation: Inspect the installer first, prefer a pinned release or commit, and run only code from a publisher and repository contents the user has explicitly decided to trust.

Risk: The skill operates real-money autonomous trading software that can place orders in the user's brokerage account.

Mitigation: Keep the agent in dry-run until broker permissions, position caps, notifications, and stop procedures are personally verified; require the human to complete the consent gate themselves.

Risk: Position sizing or trade execution guidance could be mistaken for investment advice.

Mitigation: Do not advise position sizing; remind the user that contract sizing and account risk decisions are theirs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/traderhc123/skills/agentic-trader)
- [Project homepage](https://github.com/traderhc123/agentic-trader)
- [BOOT.md assistant instructions](https://github.com/traderhc123/agentic-trader/blob/main/BOOT.md)
- [Installer script referenced by setup instructions](https://raw.githubusercontent.com/traderhc123/agentic-trader/main/install.sh)
- [AgentHC day-trade ideas track record](https://api.traderhc.com/api/v1/trading/day-trade-ideas/track-record)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes consent, sizing, broker-permission, notification, and stop-procedure reminders for real-money trading.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
