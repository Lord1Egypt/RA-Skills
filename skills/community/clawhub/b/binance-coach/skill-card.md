## Description:

Binance Coach helps agents analyze Binance portfolios, market context, DCA signals, trading behavior, alerts, news, and optional Claude or Telegram coaching using user-provided read-only credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unrealbnb](https://clawhub.ai/user/unrealbnb)

### License/Terms of Use:

MIT-0

## Use Case:

External Binance users and agents use this skill to review portfolio health, market conditions, behavioral trading patterns, DCA guidance, alerts, Binance announcements, and educational crypto concepts. Optional modes add Claude-based coaching, Telegram delivery, scheduled analyses, and background announcement watching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets and portfolio data are stored locally and the security evidence flags disclosure risk around credentials and persistent financial data.

Mitigation: Use read-only, IP-restricted Binance keys, restrict .env permissions, and review local data retention before routine use.

Risk: Optional crons, background announcement watchers, Telegram delivery, and USER.md default handling can create persistent behavior.

Mitigation: Enable those modes only when desired, review configured schedules and background processes, and keep USER.md changes opt-in and removable.

Risk: AI coaching can share portfolio and behavior details with Anthropic when configured.

Mitigation: Treat Claude coaching as third-party data sharing and use it only with data the user is comfortable sending to Anthropic.

Risk: The security guidance calls out .env sourcing, eval, and dependency concerns.

Mitigation: Review and harden environment loading, avoid unsafe eval patterns, and inspect PyPI dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unrealbnb/skills/binance-coach)
- [Publisher Profile](https://clawhub.ai/user/unrealbnb)
- [Security & Privacy](SECURITY.md)
- [Agent Guide](references/agent-guide.md)
- [Command Reference](references/commands.md)
- [Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market metrics, portfolio summaries, alert status, educational explanations, and AI coaching summaries when configured.]

## Skill Version(s):

2.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
