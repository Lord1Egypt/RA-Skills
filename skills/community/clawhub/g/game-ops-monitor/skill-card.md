## Description:

Game server real-time monitoring for checking game server health, querying TPS, online users, and JVM heap from Scouter Collector, detecting alerts, sending notifications, and generating reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Game operations engineers use this skill to inspect JVM-based game server health, including TPS, online-user counters, heap usage, and alert-oriented performance reports from Scouter Collector telemetry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad game-server telemetry to an agent through Scouter Collector queries.

Mitigation: Install only where that telemetry access is intended, and limit Collector access to the server scope needed for operations.

Risk: Persistent alerting can run on an under-scoped schedule or send notifications to the wrong destination.

Mitigation: Confirm the alert schedule, server scope, webhook destination, cooldown behavior, and disable path before enabling cron-based monitoring.

Risk: Setup examples include Collector transport and release download steps that need operational hardening.

Mitigation: Prefer HTTPS or authenticated Collector access, protect webhook URLs as secrets, and verify downloaded Scouter releases before extracting or running them.

## Reference(s):

- [Game Ops Monitor skill page](https://clawhub.ai/freepengyang/skills/game-ops-monitor)
- [OpenClaw homepage](https://github.com/openclaw/openclaw)
- [Scouter project](https://github.com/scouter-project/scouter)
- [Scouter releases](https://github.com/scouter-project/scouter/releases)
- [Port Notes](references/PORT_NOTES.md)
- [Quick Start](references/quickstart.md)
- [Alert Workflow](references/alert-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, tabular status summaries, and alert/report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Scouter Collector API calls, metric calculations, threshold classifications, and webhook-alert setup guidance.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
