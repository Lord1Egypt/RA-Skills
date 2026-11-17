## Description:

Provides Eastmoney MX finance capabilities for agents, including market and financial data lookup, finance news search, stock screening, watchlist management, and simulated portfolio operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kooui](https://clawhub.ai/user/kooui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent access to Eastmoney MX financial data, search, stock selection, watchlist, and simulated trading workflows through natural-language requests and helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change account or portfolio-adjacent state through watchlist add/delete actions and simulated buy, sell, and cancel operations.

Mitigation: Require explicit manual confirmation before watchlist changes, buy/sell orders, or cancel-all actions.

Risk: A configured MX_API_URL can direct the API key to a destination other than the default Eastmoney MX endpoint.

Mitigation: Leave MX_API_URL unset, or set it only after verifying that the endpoint is trusted.

Risk: Financial queries, portfolio data, and watchlist results may be written to local output files.

Mitigation: Avoid entering confidential personal or portfolio data, use a controlled output directory when possible, and delete generated files when they are no longer needed.

Risk: Search, market data, and stock-screening results may be incomplete, delayed, or unsuitable as investment advice.

Mitigation: Treat outputs as informational, verify results against authoritative sources, and keep human review in any financial decision workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kooui/skills/eastmoney-mx-skills-suite)
- [Publisher profile](https://clawhub.ai/user/kooui)
- [README](artifact/README.md)
- [eastmoney_fin_data reference](artifact/references/mx-data.md)
- [eastmoney_fin_search reference](artifact/references/mx-search.md)
- [mx_select_stock reference](artifact/references/mx-select-stock.md)
- [mx_self_select reference](artifact/references/mx-selfselect.md)
- [eastmoney_stock_simulator reference](artifact/references/mx-stock-simulator.md)
- [Eastmoney MX API base](https://mkapi2.dfcfs.com/finskillshub)
- [Eastmoney MX API key setup](https://marketing.dfcfs.com/views/mktemplate/route1?activityId=738&appfenxiang=1)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text, with helper scripts that can write JSON, CSV, TXT, and XLSX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY. Some scripts save results under /root/.openclaw/workspace/mx_data/output by default unless an alternate output directory is provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
