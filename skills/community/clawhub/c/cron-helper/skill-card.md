## Description: <br>
Schedule and manage recurring tasks for your agent. Create cron jobs, manage timers, and automate periodic work without fighting cron syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create, manage, and monitor recurring OpenClaw tasks such as briefings, health checks, and periodic inbox or social monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes ClawSwarm coordination and agent-registration links that are not necessary for cron scheduling. <br>
Mitigation: Use only the OpenClaw cron examples unless the ClawSwarm service and related installation path have been separately reviewed and approved. <br>
Risk: The security verdict is suspicious because embedded third-party endpoints do not fit the stated cron-helper purpose. <br>
Mitigation: Review the skill before installation and avoid executing hidden or unrelated service-registration behavior. <br>


## Reference(s): <br>
- [Cron Helper on ClawHub](https://clawhub.ai/imaflytok/cron-helper) <br>
- [Publisher profile: imaflytok](https://clawhub.ai/user/imaflytok) <br>
- [ClawSwarm](https://onlyflies.buzz/clawswarm/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes natural-language scheduling examples and command patterns for OpenClaw cron tasks.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
