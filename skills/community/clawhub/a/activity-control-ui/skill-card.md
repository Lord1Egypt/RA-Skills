## Description: <br>
Anime-style real-time activity dashboard with a virtual avatar for OpenClaw that displays agent activities, session status, token usage, and ongoing tasks in a local web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudagebil11-jpg](https://clawhub.ai/user/rudagebil11-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local OpenClaw activity dashboard that visualizes current work, token usage, task state, and live activity messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dashboard server exposes control and file access paths that need review before installation. <br>
Mitigation: Bind the server to localhost, avoid exposing it through tunnels or LAN interfaces, and review or restrict the static file handler before use. <br>
Risk: Control actions from the dashboard could be invoked by unintended clients if the server is exposed. <br>
Mitigation: Require a strong unguessable token for any control action and keep the dashboard reachable only from trusted local clients. <br>


## Reference(s): <br>
- [ClawHub Activity Control Ui Release Page](https://clawhub.ai/rudagebil11-jpg/activity-control-ui) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown usage guidance plus Node.js commands, local web UI files, JSON status responses, and WebSocket activity messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local HTTP and WebSocket dashboard server, with activity broadcasts accepted through the bundled Node.js helper.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
