## Description: <br>
OpenClaw Agent Dashboard - A Bloomberg Terminal-style web interface for real-time monitoring of all Agent status, session history, and session file sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dyh](https://clawhub.ai/user/dyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy a local OpenClaw dashboard for monitoring agent status, recent session history, heartbeat information, selected agent files, and session file sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default deployment can expose agent sessions, local agent files, and gateway access more broadly than users are told. <br>
Mitigation: Bind the server to 127.0.0.1, restrict CORS, add authentication before exposing the dashboard, and avoid running it on shared or untrusted networks. <br>
Risk: A committed or reused gateway token can allow unintended access to OpenClaw Gateway APIs. <br>
Mitigation: Remove the default token, rotate any exposed credential, and keep credentials in an untracked local secret or environment variable. <br>


## Reference(s): <br>
- [Agent Kanban Reference README](references/README.md) <br>
- [ClawHub release page](https://clawhub.ai/dyh/agent-kanban) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and bundled Node.js, HTML, CSS, and JavaScript project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local dashboard assets under assets/agent-kanban and configuration guidance for OpenClaw Gateway access.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
