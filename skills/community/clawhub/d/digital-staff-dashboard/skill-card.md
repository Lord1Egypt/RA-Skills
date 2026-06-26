## Description: <br>
A modern web-based dashboard for managing OpenClaw agents with real-time monitoring, token usage tracking, skill management, and multi-language support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikezhuyan](https://clawhub.ai/user/mikezhuyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run a local dashboard for monitoring agents, reviewing token usage, managing skills, configuring subagent dispatch, and creating or updating OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can modify OpenClaw agents, skills, configuration, and local model credential copies. <br>
Mitigation: Run it only in trusted local environments and review configuration or skill changes before relying on them. <br>
Risk: The dashboard exposes powerful local administration endpoints without clear access protection. <br>
Mitigation: Keep the service bound to localhost and avoid exposing it to a LAN or public network. <br>
Risk: The artifact includes a helper for opening network access. <br>
Mitigation: Do not run the firewall-opening helper unless the network exposure is intentional and separately controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikezhuyan/digital-staff-dashboard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/mikezhuyan) <br>
- [OpenClaw schema validation guide](artifact/OPENCLAW_SCHEMA_README.md) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, shell commands, guidance, JSON API responses] <br>
**Output Format:** [Markdown instructions with inline shell commands; the running dashboard serves HTML and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can modify local OpenClaw agent, skill, model, session, and dashboard configuration files when run.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
