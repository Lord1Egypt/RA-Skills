## Description: <br>
Continuous financial news crawler for finviz.com with SQLite storage, article extraction, and a query tool for market monitoring and news digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and market-monitoring users use this skill to build a local financial news archive, track ticker-specific headlines, and query recent articles for summaries or digest workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker-removal and cleanup paths can delete local directories outside the intended article folder if unsafe ticker values are accepted. <br>
Mitigation: Review or patch deletion paths before installation, validate ticker names, enforce path containment, keep backups, and require confirmation or a dry run before remove-ticker or automatic cleanup actions. <br>


## Reference(s): <br>
- [Finviz](https://finviz.com) <br>
- [Finviz News](https://finviz.com/news.ashx) <br>
- [PrivateApp](https://github.com/camopel/PrivateApp) <br>
- [ClawHub Skill Page](https://clawhub.ai/camopel/finviz-crawler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, SQLite-backed query results, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local article archives and ticker-filtered market news outputs for agent summarization workflows.] <br>

## Skill Version(s): <br>
3.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
