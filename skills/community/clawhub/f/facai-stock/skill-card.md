## Description:

Queries real-time A-share stock quotes, manages a local watchlist, and starts price monitoring with OpenClaw alert messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwenchang](https://clawhub.ai/user/liuwenchang)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up A-share market data by code or name, manage a persistent watchlist, and receive price movement alerts during trading hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The background stock monitor persists locally and can continue running after the initial agent task.

Mitigation: Review monitor start, stop, interval, threshold, and recipient settings before deployment; confirm the process is intentionally running and stop it when monitoring is no longer needed.

Risk: The skill sends outbound OpenClaw alert messages and stores watchlists, recipient IDs, and session cookies locally.

Mitigation: Use only approved message targets, protect the local data directory, and avoid using shared or untrusted workspaces for monitored accounts.

Risk: The security summary flags unsafe PID-based stop behavior that can kill an unchecked process ID.

Mitigation: Validate that a stored PID belongs to this monitor before stopping it, or fix PID validation before broad deployment.

Risk: The security guidance recommends dependency pinning review before broad deployment.

Mitigation: Pin and review Python dependencies before installing the skill in production or managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwenchang/skills/facai-stock)
- [Xueqiu](https://xueqiu.com/)
- [Xueqiu stock quote JSON API](https://stock.xueqiu.com/v5/stock/quote.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands, plus JSON-like stock quote and watchlist data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration, watchlist, token cache, PID, and log files when executed by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
