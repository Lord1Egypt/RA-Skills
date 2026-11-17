## Description:

Generates Chinese-language A-share daily market reports from public Eastmoney index and sector data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsxink](https://clawhub.ai/user/zsxink)

### License/Terms of Use:

MIT-0

## Use Case:

Market watchers and agents use this skill to fetch public A-share index and sector data and produce a daily Markdown or JSON report summarizing market movement, hot sectors, unavailable capital-flow fields, risks, and heuristic strategy notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market data is retrieved over unencrypted HTTP, so responses could be stale or tampered with in transit.

Mitigation: Run in a trusted network, review generated reports before use, and do not treat the output as verified real-time market data.

Risk: The report includes heuristic strategy text and unavailable capital-flow fields rendered as "--".

Mitigation: Present outputs as informational summaries, verify figures against authoritative financial sources, and avoid using the report as investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zsxink/skills/a-stock-daily-report)
- [Eastmoney Quote Site](http://quote.eastmoney.com/)
- [Eastmoney Sector Data API](http://push2.eastmoney.com/api/qt/clist/get)
- [Eastmoney Stock Data API](http://push2.eastmoney.com/api/qt/stock/get)

## Skill Output:

**Output Type(s):** [markdown, json, text, guidance]

**Output Format:** [Markdown report by default; pretty-printed JSON when invoked with json or --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Unavailable fields are emitted as "--" and failed data fetches are noted in the report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
