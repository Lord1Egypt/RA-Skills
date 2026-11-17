## Description:

Monitors Binance announcements and the @binance and @binancezh X accounts, then queues Feishu notifications when new content appears.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhaoting](https://clawhub.ai/user/xuhaoting)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operations teams use this skill to monitor Binance exchange announcements and official X account updates, then route newly detected items into Feishu notifications for timely review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hard-coded Feishu targetUser values may send alerts to an unintended recipient.

Mitigation: Replace targetUser in monitor.js, x-monitor.js, config.json, and config.example.json with a recipient you control, or require the scripts to load and validate config.json before sending notifications.

Risk: The documented cron pkill restart pattern can stop unrelated Node.js monitor processes.

Mitigation: Use one clearly scoped lifecycle manager such as systemd, screen, or a process supervisor, and document exact stop and removal commands.

Risk: Monitored Binance and X content is handled through Jina AI and Feishu-related notification workflows.

Mitigation: Confirm that this routing is acceptable for the deployment environment before running the monitor.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuhaoting/skills/binance-announce-monitor)
- [Publisher Profile](https://clawhub.ai/user/xuhaoting)
- [Binance Public Announcement API](https://www.binance.com/bapi/composite/v1/public/cms/article/list/query)
- [Jina AI Reader for @binance](https://r.jina.ai/twitter/binance)
- [Jina AI Reader for @binancezh](https://r.jina.ai/twitter/binancezh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notification text, JSON queue and state files, and shell command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and network access to Binance, Jina AI Reader, and Feishu-related notification handling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
