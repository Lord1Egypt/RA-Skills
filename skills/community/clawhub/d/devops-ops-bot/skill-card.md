## Description: <br>
DevOps Ops Bot provides server health monitoring with configurable CPU, memory, disk, and uptime checks, Slack or Discord alerts, and optional auto-recovery for critical conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gruted](https://clawhub.ai/user/gruted) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations engineers use this skill to check server health, configure alert thresholds, send Slack or Discord notifications, and optionally recover critical services with restart commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented curl-to-bash install path can execute remote code without review. <br>
Mitigation: Prefer a pinned npm package version or pinned container digest and review the package before installation. <br>
Risk: Auto-restart commands can affect production services when critical thresholds are reached. <br>
Mitigation: Enable restart behavior only for specific services with tightly scoped permissions and reviewed commands. <br>
Risk: Slack or Discord webhook URLs can expose alert channels if handled as plain text. <br>
Mitigation: Store webhook URLs as secrets and avoid committing them to configuration, logs, or shared prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gruted/devops-ops-bot) <br>
- [Project repository](https://github.com/gruted/devops-ops-bot) <br>
- [Landing page](https://gruted.github.io/devops-ops-bot/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include threshold values, webhook configuration, cron examples, and restart command guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
