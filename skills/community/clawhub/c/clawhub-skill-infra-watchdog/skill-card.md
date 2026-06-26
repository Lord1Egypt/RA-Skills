## Description: <br>
Self-hosted infrastructure monitoring with local checks for HTTP, TCP, Docker, resources, SSL, DNS, Proxmox, and alerts via WhatsApp, Telegram, or Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariusfit](https://clawhub.ai/user/mariusfit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and homelab administrators use this skill to configure and run local uptime, service, resource, and certificate checks for self-hosted infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SSL validity and certificate-expiry results may be unreliable and could give false confidence. <br>
Mitigation: Review and fix the SSL-checking behavior before relying on this skill for security monitoring. <br>
Risk: Monitor names, targets, and alert messages may expose infrastructure details through selected alert channels. <br>
Mitigation: Avoid sensitive monitor names or targets and enable external alerts only for channels approved for infrastructure status. <br>
Risk: Scheduled checks can repeatedly probe configured services and generate recurring notifications. <br>
Mitigation: Confirm check intervals, alert cooldowns, and monitored targets before enabling scheduled runs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mariusfit/clawhub-skill-infra-watchdog) <br>
- [Publisher profile](https://clawhub.ai/user/mariusfit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local monitor configuration, SQLite state, and status summaries in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
