## Description:

Daily Hot Aggregator collects cross-platform trending topics from Bilibili, Douyin, Weibo, and Toutiao, then helps agents summarize, analyze, alert on, and push daily hot-list reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkt-agents](https://clawhub.ai/user/mkt-agents)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and operators use this skill to collect daily hot-list data across Chinese content platforms, generate reports and topic recommendations, and send configured hot-topic alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships credential-like secrets and an enabled external messaging configuration.

Mitigation: Before installation or execution, remove and rotate the bundled Weibo cookie and WeCom webhook key, and replace the push configuration with a disabled-by-default template using user-owned credentials.

Risk: Generated HTML reports can contain platform-sourced content.

Mitigation: Treat generated HTML reports as untrusted content and review them before opening in privileged contexts or sharing externally.

Risk: Installing with a moving package tag can change installer behavior over time.

Mitigation: Pin the ClawHub installer version when deploying this skill in repeatable or production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mkt-agents/skills/daily-hot-aggregator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, HTML]

**Output Format:** [Markdown guidance with shell commands, JSON configuration and reports, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; generated reports may include platform-sourced content.]

## Skill Version(s):

7.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
