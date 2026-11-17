## Description:

FootyClaw helps users fetch football odds, analyze markets with expected value and Kelly-style stake sizing, produce betting recommendations, track a bankroll ledger, and generate bankroll charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[botaocai](https://clawhub.ai/user/botaocai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to evaluate football betting opportunities by combining odds data, fundamental checks, EV calculations, Kelly-style stake sizing, and bankroll tracking. Outputs are informational and should be used only where sports betting is legal.

### Deployment Geography for Use:

Global, where sports betting use is legal

## Known Risks and Mitigations:

Risk: The skill recommends wager amounts and may be mistaken for reliable financial advice.

Mitigation: Treat recommendations as informational, review each wager independently, use the skill only where sports betting is legal, and set personal betting limits.

Risk: Bankroll and shareholder ledger details may include sensitive personal finance information.

Mitigation: Avoid storing sensitive personal finance details unless the user is comfortable keeping them in session memory.

Risk: The Odds API key is used for live odds requests and could be exposed through request or URL logs.

Mitigation: Configure a narrowly scoped ODDS_API_KEY when possible and rotate it if exposure is suspected.

## Reference(s):

- [Betting Rules](references/betting-rules.md)
- [Fundamental Analysis Framework](references/fundamental-analysis.md)
- [The Odds API](https://the-odds-api.com)
- [ClawHub Skill Page](https://clawhub.ai/botaocai/skills/footyclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text betting summaries, inline shell commands, JSON from helper scripts, and Base64-encoded SVG image tags for ledger charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ODDS_API_KEY for The Odds API requests and keeps ledger output in conversation rather than writing local files.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
