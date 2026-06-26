## Description: <br>
Deploy the Agent HQ mission-control stack with an Express and React board, Telegram notifications, Jarvis summaries, setup guidance, telemetry, and automation hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thibautrey](https://clawhub.ai/user/thibautrey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to install and run a local Agent HQ mission-control board, configure Telegram alerts, and operate summary and notification automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on a referenced GitHub repository and npm dependencies. <br>
Mitigation: Inspect the repository and dependency lockfiles before installing, and prefer pinning a trusted commit or release. <br>
Risk: Telegram bot credentials and the Agent HQ API token can grant access to notifications or mutating endpoints. <br>
Mitigation: Use a dedicated low-privilege Telegram bot, keep tokens out of source control, and set AGENT_HQ_API_TOKEN before exposing the service. <br>
Risk: Optional cron jobs keep alert automation running in the background. <br>
Mitigation: Install cron jobs only when persistent alerts are intended, and run them with the least privilege needed. <br>


## Reference(s): <br>
- [Agent HQ on ClawHub](https://clawhub.ai/thibautrey/agent-hq) <br>
- [Agent HQ repository referenced by setup instructions](https://github.com/thibautrey/agent-hq.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and curl code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, runtime commands, configuration notes, and operational tips for local deployment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
