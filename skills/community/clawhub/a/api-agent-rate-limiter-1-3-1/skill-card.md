## Description: <br>
Prevents AI agents from hitting 429 rate limits with local tier-based throttling, rolling-window usage tracking, and exponential backoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kakaxiazai](https://clawhub.ai/user/kakaxiazai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a local gate around expensive agent work, record usage, and reduce or pause activity before and after rate-limit responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can pause or reduce agent activity when its local tier reaches throttled, critical, or paused states. <br>
Mitigation: Review agent prompt, heartbeat, and cron integrations before enabling them, and tune the provider, plan, and estimated limit for the account. <br>
Risk: Shared or lingering state and timer setup can affect future agent runs after configuration changes or uninstall. <br>
Mitigation: Keep RATE_LIMIT_STATE in a known per-instance JSON path and remove any related timer or cron entry when disabling the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kakaxiazai/api-agent-rate-limiter-1-3-1) <br>
- [The Agent Wire](https://theagentwire.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON status/state output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local JSON state file and standard Python library behavior; no API keys or external services are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports upstream skill version 1.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
