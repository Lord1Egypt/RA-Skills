## Description: <br>
Use the `clawmonitor` CLI/TUI to inspect OpenClaw sessions, model health, token usage, and gateway service health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawq](https://clawhub.ai/user/openclawq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local OpenClaw sessions, diagnose stalled or failed delivery, check model/provider health, review token usage, and summarize service-level issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local ClawMonitor commands that read OpenClaw state from the host. <br>
Mitigation: Install and run it only on hosts where ClawMonitor access to local OpenClaw state is intended. <br>
Risk: `clawmonitor init` writes configuration, and `clawmonitor nudge` sends a message into a selected session. <br>
Mitigation: Treat initialization as a setup action and use nudge only when intentionally requesting progress from that session. <br>


## Reference(s): <br>
- [Claw Monitor skill page](https://clawhub.ai/openclawq/claw-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands and diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers redacted Markdown reports and avoids raw gateway logs unless requested.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
