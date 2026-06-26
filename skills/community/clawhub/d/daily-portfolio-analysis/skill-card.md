## Description: <br>
Daily Portfolio Analysis helps an agent combine holdings across brokerage accounts, fetch current prices and exchange rates, and produce a portfolio allocation and daily-change report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shengbinxu](https://clawhub.ai/user/shengbinxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize personal investment holdings, compare account allocation, and generate scheduled or conversational portfolio reports. It is intended for users who understand the sensitivity of their brokerage data and can review any report-push configuration before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process sensitive financial holdings and generated portfolio summaries. <br>
Mitigation: Store portfolio configuration and generated reports in a private workspace, avoid sharing brokerage screenshots unless necessary, and review outputs before forwarding them. <br>
Risk: Reports may be sent to Feishu without clear opt-in or prominent disclosure. <br>
Mitigation: Confirm the Feishu notification configuration before use, disable report push behavior if it is not required, and verify the destination before sending any report. <br>
Risk: Market prices and exchange rates are fetched from external services and may be unavailable or stale. <br>
Mitigation: Treat generated analysis as informational, check important values against authoritative brokerage or market data sources, and review cached or fallback exchange-rate behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shengbinxu/daily-portfolio-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/shengbinxu) <br>
- [Futu OpenD documentation](https://openapi.futunn.com/futu-api-doc/opend/opend-cmd.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown-style portfolio report text with tables, plus JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include sensitive holdings, market values, allocation percentages, and daily performance changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
