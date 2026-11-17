## Description:

Connects OpenClaw to Ekybot for remote agent control, Companion machine health, project memory sync, connector setup, connectivity validation, and onboarding to a successful live test.

This skill is ready for commercial/non-commercial use.

## Publisher:

[regiomag](https://clawhub.ai/user/regiomag)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to install and configure the Ekybot connector, enroll a local machine, validate connectivity, and operate remote agent control, machine health, and project memory sync through Ekybot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connector gives Ekybot broad background access to manage local OpenClaw agents and relay prompts into them.

Mitigation: Use a low-privilege account, avoid running the daemon with sudo, and restrict tools available to remotely reachable agents.

Risk: Project memory sync can upload selected local memory files to Ekybot cloud.

Mitigation: Review memory files before enabling sync and disable memory sync with EKYBOT_COMPANION_MEMORY_SYNC=false when those files should stay local.

Risk: Background service operation and deletion-safety concerns require review before use.

Mitigation: Back up OpenClaw workspaces before setup and verify or disable installed background services after configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/regiomag/skills/ekybot-connector)
- [Ekybot Homepage](https://www.ekybot.com)
- [EkyBot Workspace API Reference](artifact/references/api.md)
- [EkyBot Connector Security Model](artifact/references/security.md)
- [Ekybot Connector Troubleshooting](artifact/references/troubleshooting.md)
- [Inter-Agent Communication Protocol](artifact/templates/INTER-AGENT-PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=18 and an Ekybot enrollment token; setup may install a background daemon.]

## Skill Version(s):

6.1.0 (source: server release metadata; artifact package metadata reports 6.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
