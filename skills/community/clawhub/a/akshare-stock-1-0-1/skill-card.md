## Description:

Provides agent-facing guidance and a small CLI for retrieving China A-share market data, historical K-lines, financial indicators, sector data, fund flow data, IPO data, and margin trading data through AkShare.

This skill is for research and development only.

## Publisher:

[kenswj](https://clawhub.ai/user/kenswj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external agents use this skill to query A-share quotes, historical price data, financial indicators, board and concept data, fund flows, and stock search results. Outputs should be treated as research market data and not as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AkShare and Baostock dependencies may change behavior or fail to install consistently.

Mitigation: Install the skill in a dedicated virtual environment and pin AkShare or Baostock versions before operational use.

Risk: Market data may be delayed, unavailable, or affected by upstream website changes.

Mitigation: Treat returned data as research input, add retry and exception handling, and validate important results against authoritative data sources.

Risk: Some advertised or scripted actions may require fixes or direct AkShare calls before working reliably.

Mitigation: Review and test the specific CLI actions locally before relying on them in an agent workflow.

Risk: Financial outputs could be mistaken for investment recommendations.

Mitigation: Label outputs as market data for research only and keep investment decisions outside the skill workflow.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/kenswj/skills/akshare-stock-1-0-1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; the bundled CLI emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on AkShare availability and upstream market-data sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
