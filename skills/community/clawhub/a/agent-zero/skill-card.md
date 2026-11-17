## Description:

AgentZero helps an agent operate a local real estate listing tracker by adding and refreshing property listings, listing search profiles, triaging matches with Claude, and running an opt-in Redfin email scan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzhong52](https://clawhub.ai/user/yzhong52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers running OpenClaw use AgentZero to maintain a local real estate listing tracker, ingest supported listing URLs and Redfin alert emails, and surface profile-matched homes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation and email access for the Daily Email Scan workflow.

Mitigation: Run the scan only after explicit user consent, with reviewed himalaya and openclaw browser configuration, and keep it scoped to Redfin alert emails.

Risk: Startup scripts and local services may affect the trusted local workspace.

Mitigation: Inspect the backend and frontend startup scripts before use and run them only in a workspace where their local writes and process behavior are acceptable.

Risk: Anthropic and Gmail credentials are required for full functionality.

Mitigation: Protect or rotate credentials used with the skill and avoid exposing them in logs, shell history, or shared workspaces.

Risk: Persistent browser automation can carry sandbox or browser-profile risk.

Mitigation: Avoid the browser fallback unless the user accepts the browser profile risk, and prefer hardened host validation and sanitized logs before routine use.

## Reference(s):

- [AgentZero ClawHub listing](https://clawhub.ai/yzhong52/skills/agent-zero)
- [yzhong52 ClawHub publisher profile](https://clawhub.ai/user/yzhong52)
- [OpenClaw](https://openclaw.ai)
- [Anthropic Console](https://console.anthropic.com)
- [AgentZero backend local service](http://localhost:8000)
- [AgentZero frontend local service](http://localhost:5173)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local notes, processed-email state, a SQLite database, cached listing HTML snapshots, and local service logs as disclosed by ClawHub metadata.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
