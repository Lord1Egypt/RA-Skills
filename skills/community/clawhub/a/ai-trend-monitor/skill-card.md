## Description: <br>
AI Trend Monitor watches AI-related signals across GitHub, Reddit, Twitter/X, Xiaohongshu, and news sources, then sends major-news alerts and scheduled Feishu summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyuyang001-oss](https://clawhub.ai/user/wuyuyang001-oss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to monitor AI market and technical trends, push important updates quickly, and send scheduled digest cards to Feishu channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured Feishu webhooks can receive automated summaries and alerts. <br>
Mitigation: Use dedicated webhook URLs, keep them private, and rotate them if exposed. <br>
Risk: Realtime and cron modes can create recurring posts. <br>
Mitigation: Enable realtime or scheduled execution only for channels that should receive repeated AI trend updates. <br>
Risk: The skill depends on configured search behavior and source results for trend quality. <br>
Mitigation: Review source links and verify important claims before acting on market or technical summaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyuyang001-oss/ai-trend-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [Feishu interactive card JSON, console text, and Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports realtime, once, and scheduled run modes with Feishu webhook configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and artifact/SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
