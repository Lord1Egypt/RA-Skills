## Description: <br>
Provides A-share market data queries for stock lists, quotes, IPOs, block trades, margin trading details, and individual security valuation metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shawn92](https://clawhub.ai/user/Shawn92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and summarize public A-share market data, including all-stock lists, quote pages, IPO records, block trades, margin-trading details, and single-security valuation metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs bundled Python scripts and makes outbound requests to market.ft.tech and ftai.chat. <br>
Mitigation: Install only in environments that permit those scripts and domains; use network allowlisting where required. <br>
Risk: The dispatcher does not enforce a separate subskill whitelist. <br>
Mitigation: Keep invocations to documented subskills and parameters, or add command allowlisting in tightly governed deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shawn92/ftai-market-data) <br>
- [market.ft.tech API host](https://market.ft.tech) <br>
- [A-share quotes endpoint](https://market.ft.tech/app/api/v2/stocks) <br>
- [ftai.chat security info endpoint](https://ftai.chat/api/v1/market/security/{symbol}/info) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON] <br>
**Output Format:** [Markdown summaries or tables derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market data is fetched from market.ft.tech and ftai.chat through bundled Python scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
