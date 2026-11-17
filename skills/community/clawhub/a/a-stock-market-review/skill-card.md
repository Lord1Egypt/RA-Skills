## Description:

Generates a China A-share market closing recap covering major indices, hot sectors, sector leaders, and stocks reaching new highs using public Eastmoney data without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill after the China A-share market close to generate a daily recap of indices, top concept sectors, sector leaders, and new-high stocks. The report is for market review only and should not be treated as trading or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake the generated market recap for investment advice.

Mitigation: Present the report as informational market review only and require human judgment before any financial decision.

Risk: Market data requests use HTTP Eastmoney endpoints, creating transport-security exposure.

Mitigation: Prefer a release that switches Eastmoney calls to HTTPS where supported, and run the skill in an isolated Python environment.

Risk: Market data may be incomplete or stale outside China A-share trading hours or before the daily close.

Mitigation: Use the skill after the 15:00 Asia/Shanghai market close and treat unavailable or partial data as a report limitation.

Risk: Unpinned Python dependencies can change runtime behavior over time.

Mitigation: Pin dependencies in a dedicated environment before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/a-stock-market-review)
- [Eastmoney quote API](http://push2.eastmoney.com/api/qt/stock/get)
- [Eastmoney list API](http://push2.eastmoney.com/api/qt/clist/get)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Plain text market recap, optionally presented in Markdown with shell commands or Python snippets for usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Eastmoney market data at run time; report contents depend on API availability and market update timing.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
