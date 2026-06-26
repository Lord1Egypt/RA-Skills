## Description: <br>
Production-grade health monitoring, alerting, and service management for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrsmithai](https://clawhub.ai/user/mrsmithai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up health checks, uptime tracking, Telegram alerting, and service recovery workflows for OpenClaw agents and related production services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The monitoring loop can persist through cron, launchd, or systemd and run configurable restart commands, including privileged commands. <br>
Mitigation: Review scripts and services.json before installation, restrict write access to trusted admins, and prefer fixed least-privilege restart wrappers over broad sudo or arbitrary shell snippets. <br>
Risk: Telegram alerting can send operational details outside the host. <br>
Mitigation: Use a dedicated bot and restricted chat, avoid sensitive service names or secrets in alert text, and review alert content before enabling notifications. <br>
Risk: Automatic recovery can repeatedly restart unhealthy services if configuration is too broad or incorrect. <br>
Mitigation: Set conservative cooldowns and maximum restart attempts, test each restart command manually, and monitor recovery logs after enabling automation. <br>


## Reference(s): <br>
- [Agent Ops Kit ClawHub page](https://clawhub.ai/mrsmithai/agent-ops-kit) <br>
- [Sample configuration](artifact/references/sample-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell snippets, JSON configuration examples, and bash/Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an executable health-check script and a sample services.json configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
