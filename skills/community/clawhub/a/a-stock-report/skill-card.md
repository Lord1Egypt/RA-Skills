## Description: <br>
A-stock-report generates and schedules A-share market reports, including morning reports, close summaries, evening reports, intraday alerts, IPO weekly reports, and weekend finance digests with investor-sentiment scoring and market outlook guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cookfish1979](https://clawhub.ai/user/cookfish1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-operations agents use this skill to collect A-share market data, generate scheduled finance reports and alerts, and push the resulting summaries to a configured WeCom webhook. The reports are informational and include built-in no-investment-advice disclaimers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches finance data on a schedule and can send generated reports or alerts automatically to WeCom. <br>
Mitigation: Install it only for this workflow, verify the configured webhook destination, and use dry-run or manual review paths before enabling unattended delivery. <br>
Risk: Credentials may be exposed or over-scoped if unrelated secrets are placed in the environment file used by the scripts. <br>
Mitigation: Keep the environment file limited to the documented WeCom and iWencai keys, and remove broader fallback secret sources in stricter environments. <br>
Risk: Market reports can be affected by data-source outages, stale search results, or provider field changes. <br>
Mitigation: Monitor scheduled runs, preserve the built-in data-missing markers and source labels, and treat generated market commentary as informational rather than investment advice. <br>
Risk: The skill writes intermediate and report files under /tmp and the workspace reports directory. <br>
Mitigation: Run it in an isolated workspace with expected write permissions and review generated files before sharing them beyond the configured audience. <br>


## Reference(s): <br>
- [A-stock-report ClawHub page](https://clawhub.ai/cookfish1979/a-stock-report) <br>
- [cron_jobs README](cron_jobs/README.md) <br>
- [Fallback Chain Validation Log](references/fallback-chain-validation.md) <br>
- [Weekend 4KB Budget Record](references/weekend-4kb-budget.md) <br>
- [Eastmoney finance news](https://finance.eastmoney.com/news/cywjh.html) <br>
- [Sina Finance](https://finance.sina.com.cn/) <br>
- [21st Century Business Herald](https://www.21jingji.com/) <br>
- [CNFIN](https://www.cnfin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, JSON data files, shell commands, and WeCom text messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled jobs may write report files under the workspace and send generated reports or alerts to a configured WeCom webhook.] <br>

## Skill Version(s): <br>
3.5.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
