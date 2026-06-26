## Description: <br>
Interactive setup wizard that creates a multi-agent AI team on OpenClaw, including agents, workspace files, communication infrastructure, cron automation, a live operations dashboard, and optional GitHub bundle export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oabdelmaksoud](https://clawhub.ai/user/oabdelmaksoud) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to bootstrap and operate a configurable multi-agent workspace with specialist agents, shared state files, scheduled dispatch, and a browser dashboard. It is intended for teams that want repeatable multi-agent setup, status checks, rebuilds, exports, and task dispatch commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose and modify workspace and cron state through browser-accessible controls. <br>
Mitigation: Run the dashboard bound to localhost, place it behind authentication if remote access is needed, and review workspace changes before relying on them. <br>
Risk: Persistent OpenClaw automation and scheduled dispatch can continue acting on workspace files after setup. <br>
Mitigation: Review registered crons, monitor dispatch logs, and disable or remove scheduled jobs when the team should stop running. <br>
Risk: GitHub export can publish generated bundle contents. <br>
Mitigation: Inspect generated files and repository visibility before pushing or creating a public GitHub repository. <br>


## Reference(s): <br>
- [AGI Farm Dashboard Reference](references/dashboard.md) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [AGI Farm on ClawHub](https://clawhub.ai/oabdelmaksoud/agi-farm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration, shell commands, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw workspace state, agent configuration, cron registration, dashboard assets, and optional GitHub export instructions.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
