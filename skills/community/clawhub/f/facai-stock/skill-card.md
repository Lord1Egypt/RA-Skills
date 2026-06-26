## Description: <br>
Queries real-time A-share stock quotes, searches stocks by code or name, manages a local watchlist, and can start a background price monitor that sends OpenClaw alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwenchang](https://clawhub.ai/user/liuwenchang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External ClawHub users and agent operators use this skill to retrieve mainland China A-share quote details, search candidate stocks, maintain a watchlist, and configure price-change alerts. It supports stock-code and stock-name workflows with local persistence for watchlists, configuration, cached quote-service cookies, and monitor logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local watchlist and configuration files, stores a notification target, caches quote-service cookies, and writes monitor logs. <br>
Mitigation: Review and periodically clear the skill's data and log files, and avoid storing unnecessary sensitive values in the monitor target configuration. <br>
Risk: The background monitor can continue polling external quote services and send alerts after it is started. <br>
Mitigation: Require explicit confirmation before starting or restarting monitoring, verify monitor status, and stop the monitor when alerts are no longer needed. <br>
Risk: The skill contacts external services for quote lookup and alert delivery. <br>
Mitigation: Install only in environments where outbound access to the quote service and OpenClaw alert delivery is acceptable. <br>
Risk: Clearing the watchlist removes locally persisted stocks. <br>
Mitigation: Require explicit confirmation before clearing the watchlist. <br>


## Reference(s): <br>
- [ClawHub release: facai-stock](https://clawhub.ai/liuwenchang/facai-stock) <br>
- [Xueqiu](https://xueqiu.com/) <br>
- [Xueqiu quote API endpoint](https://stock.xueqiu.com/v5/stock/quote.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets plus JSON-style quote, watchlist, status, and alert results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local data, cache, PID, and log files, and may send OpenClaw alert messages when monitoring is started.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
