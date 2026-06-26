## Description: <br>
Deploys a local operations dashboard for OpenClaw Coding Plan subscribers to monitor API quota, usage trends, token consumption, cron settings, agent status, and subscription timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumuli2021](https://clawhub.ai/user/mumuli2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw Coding Plan users and agent operators use this skill to deploy a local dashboard for quota monitoring, predictive usage tracking, token analysis, cron management, and multi-agent status review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated dashboard controls can change scheduled-task state or write local files. <br>
Mitigation: Keep the dashboard private, bind services to localhost or a trusted network, and add authentication before exposing mutation endpoints. <br>
Risk: Cron changes may affect recurring agent activity and API usage. <br>
Mitigation: Review pending cron changes before applying them and enable recurring cron writers only with clear opt-in and a known data path. <br>


## Reference(s): <br>
- [Cron Setup Guide](references/cron-setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/mumuli2021/claw-agent-cockpit) <br>
- [Publisher profile](https://clawhub.ai/user/mumuli2021) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, JavaScript dashboard files, JSON configuration, and local HTML dashboard assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local dashboard assets and operational guidance; users should configure quota cycle dates, PM2 services, and cron behavior for their workspace.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
