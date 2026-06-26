## Description: <br>
China Stock Toolkit gives agents market dashboard commands for China A-shares and related global markets, including index quotes, watchlists, stock details, tax and fee calculations, and news sentiment summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darbling](https://clawhub.ai/user/darbling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to ask an agent for market snapshots, stock details, watchlist updates, transaction cost estimates, and news sentiment summaries. Outputs are informational and should be checked against authoritative financial sources before trading or investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, stock names, sector terms, and news queries may be sent to public financial and news services or user-configured data sources. <br>
Mitigation: Use only trusted API keys, proxies, and custom endpoints, and avoid sending confidential portfolio or business-sensitive queries. <br>
Risk: Quote data, fee calculations, and keyword-based sentiment labels may be delayed, incomplete, or misleading if used as trading signals. <br>
Mitigation: Treat all results as informational, verify against authoritative market or brokerage data, and do not rely on the skill as investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/darbling/china-stock-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with command examples and market/news summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use public or user-configured market and news data sources, optional API keys, proxies, and a local HTML dashboard.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata; artifact changelog also lists v3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
