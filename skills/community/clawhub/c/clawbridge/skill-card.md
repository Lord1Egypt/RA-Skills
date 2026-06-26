## Description: <br>
ClawBridge is a mobile-first dashboard for OpenClaw agents that monitors real-time activity, tracks token costs, and lets users control cron tasks from a phone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dreamwing](https://clawhub.ai/user/dreamwing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use ClawBridge to install and operate a local mobile dashboard for agent monitoring, token cost visibility, and cron task control. The skill supports optional remote access through a Cloudflare tunnel when users need dashboard access away from the local network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install and update flow executes shell code retrieved from GitHub. <br>
Mitigation: Review the remote installer and source before running it, and use trusted release versions where possible. <br>
Risk: The optional Cloudflare tunnel can expose the dashboard beyond localhost. <br>
Mitigation: Treat the generated ACCESS_KEY like a password, avoid sharing tunnel URLs publicly, and disable the tunnel when remote access is not needed. <br>
Risk: ClawBridge installs a persistent user-level service and stores local configuration and analytics data. <br>
Mitigation: Stop or disable the service when it is not needed, and protect the generated .env file and local data directory. <br>


## Reference(s): <br>
- [ClawBridge ClawHub release](https://clawhub.ai/dreamwing/clawbridge) <br>
- [dreamwing publisher profile](https://clawhub.ai/user/dreamwing) <br>
- [ClawBridge homepage](https://clawbridge.app) <br>
- [ClawBridge README](https://github.com/dreamwing/clawbridge/blob/master/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include service-management steps, local dashboard access details, and optional tunnel setup guidance.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
