## Description:

A web-based dashboard for managing OpenClaw agents with real-time monitoring, token usage tracking, skill management, subagent dispatch management, and multi-language support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikezhuyan](https://clawhub.ai/user/mikezhuyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a local dashboard for viewing OpenClaw agent status, reviewing token and cost statistics, creating agents, managing subagent dispatch, and enabling or disabling skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard exposes administrative OpenClaw controls over a network service without visible authentication.

Mitigation: Run it only in a controlled local environment, bind the service to 127.0.0.1, and add authentication before exposing any API endpoints.

Risk: Agent, subagent, skill, model, avatar, and dashboard configuration endpoints can modify local OpenClaw state.

Mitigation: Back up OpenClaw configuration before use and review changes made through the dashboard before relying on updated agents or prompts.

Risk: The bundled LAN port-opening helper can make the dashboard reachable from other machines on the network.

Mitigation: Do not use the port-opening helper unless network exposure has been explicitly approved and protected by firewall rules and authentication.

Risk: The skill-installation endpoint invokes the OpenClaw CLI to install requested skills.

Mitigation: Restrict dashboard access and install only trusted skill identifiers from expected publishers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikezhuyan/skills/digital-staff-dashboard)
- [Publisher profile](https://clawhub.ai/user/mikezhuyan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown instructions, shell commands, local web UI, JSON API responses, and OpenClaw configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a Flask dashboard that reads and modifies local OpenClaw agent, skill, session, avatar, and dashboard configuration state.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
