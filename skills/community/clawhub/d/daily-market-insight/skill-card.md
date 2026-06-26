## Description: <br>
Daily Market Insight gathers current macroeconomic, technology, geopolitical, and commodity news, analyzes sentiment and market impact, and drafts a market briefing for Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a851445115](https://clawhub.ai/user/a851445115) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Market analysts and teams that need a daily briefing can use this skill to collect market news, organize sentiment and impact analysis, forecast trends for A-shares, Hong Kong equities, and U.S. equities, and publish a report to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled Feishu publishing may send reports to an unintended account, document, or chat if destinations are not confirmed. <br>
Mitigation: Confirm the Feishu account, document location, and chat before enabling scheduled runs, and require manual approval for posts where possible. <br>
Risk: The workflow invokes local shell tooling and writes report and log files under local workspace paths. <br>
Mitigation: Run it in a dedicated project directory and confirm that opencode and any git initialization step are acceptable before execution. <br>
Risk: Generated market analysis can be incomplete or misleading. <br>
Mitigation: Treat reports as informational only and review all investment-related guidance before relying on it. <br>


## Reference(s): <br>
- [Daily Market Insight on ClawHub](https://clawhub.ai/a851445115/daily-market-insight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with structured analysis sections, optional tables, Feishu document content, and a short Feishu chat status message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled daily at 10:00; requires web_search, web_fetch, and feishu_doc.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
