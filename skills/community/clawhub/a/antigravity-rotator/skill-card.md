## Description: <br>
Automates Google Antigravity account rotation, quota monitoring, model priority scheduling, live session updates, and dashboard monitoring for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChocomintX](https://clawhub.ai/user/ChocomintX) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage multiple Google Antigravity accounts in OpenClaw, monitor quota status, rotate accounts or models, and keep active sessions updated without restarting work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports powerful account and session controls exposed through an unauthenticated network dashboard. <br>
Mitigation: Bind the dashboard to localhost or place it behind authentication, and do not expose port 18090 to a LAN or the internet. <br>
Risk: The security scan reports under-disclosed credential handling and account token refresh behavior. <br>
Mitigation: Treat config.json and OpenClaw auth profile files as sensitive, back up auth profiles before use, and prefer low-risk dedicated accounts. <br>
Risk: The skill can run scheduled rotations that rewrite active account and model state. <br>
Mitigation: Review the cron entry and rotation configuration before enabling automation, especially account lists, model priority, and quota thresholds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChocomintX/antigravity-rotator) <br>
- [Publisher profile](https://clawhub.ai/user/ChocomintX) <br>
- [Configuration example](assets/config.example.json) <br>
- [Cron sample](assets/crontab.sample.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Execution may update local configuration, OpenClaw auth profile state, model status data, rotation state, and logs.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
