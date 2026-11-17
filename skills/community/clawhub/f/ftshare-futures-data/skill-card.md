## Description:

FTShare Futures Data routes agent requests to market.ft.tech futures endpoints for contract lists, contract reference data, and k-line price history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and market-data agents use this skill to look up A-share futures contract symbols, static contract attributes, and historical or aggregated k-line data. It is suited for data retrieval and presentation workflows, not automated trading decisions without independent review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network requests may follow redirects outside the disclosed market.ft.tech destination.

Mitigation: Review the package before deployment and disable redirects or validate the final response URL after redirects.

Risk: HTTP reads do not have explicit timeouts or response-size limits.

Mitigation: Run the skill with network controls and add timeouts and response-size limits before relying on it in production workflows.

Risk: The skill returns live third-party futures data that may be unavailable, incomplete, or unsuitable for high-stakes decisions.

Mitigation: Treat outputs as data-retrieval results and verify them against an authoritative source before trading, compliance, or financial decision-making.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-futures-data)
- [Publisher profile](https://clawhub.ai/user/shawn92)
- [market.ft.tech futures data host](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [json, shell commands, guidance]

**Output Format:** [JSON from command-line handlers, with agent-facing summaries usually rendered as text or Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live market.ft.tech responses and may be limited by request parameters such as trade date, symbol, interval, start, end, and limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
