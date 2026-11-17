## Description:

Convene brings together ten trader-style analysis personas that vote independently on a symbol, then aggregates their ballots into one LONG, SHORT, or NO_TRADE verdict as analysis and a second opinion, not a trading signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxdavid-offbeatforex](https://clawhub.ai/user/fxdavid-offbeatforex)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and market-analysis users use Convene to request a structured second opinion on a symbol, timeframe, and platform. The skill coordinates data fetching, independent persona ballots, and deterministic aggregation into a concise council verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may download and run mutable external code from GitHub during setup.

Mitigation: Review the source before installation, run it in a contained environment, and pin reviewed code versions where possible.

Risk: Normal use may install Python dependencies and inspect local MetaTrader terminals.

Mitigation: Use an environment with only the intended trading terminal and dependency set available.

Risk: An optional TradingView API key can be stored in a plaintext .env file or requested through a remote channel.

Mitigation: Enter keys through a secure local secret mechanism when possible and avoid sending secrets in chat.

Risk: Market-analysis output could be mistaken for financial advice or a trading signal.

Mitigation: Present results as analysis and a second opinion, and keep the no-fabricated-data failure behavior intact.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/FXDavid-OffbeatForex/tlc-hermes-skills/tree/main/skills/convene)
- [TLC project homepage](https://github.com/FXDavid-OffbeatForex/TLC)
- [ClawHub skill page](https://clawhub.ai/fxdavid-offbeatforex/skills/convene)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tabular ballot summaries and a final council verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup status, data-fetch errors when applicable, and a finance-analysis disclaimer.]

## Skill Version(s):

0.1.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
