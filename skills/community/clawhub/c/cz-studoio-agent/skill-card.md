## Description: <br>
Bridge OpenClaw to a remote Studio Agent over WebSocket using a local JSONL proxy CLI for streaming, stop, and multi-turn workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luketalent](https://clawhub.ai/user/luketalent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to a ClickZetta Studio Agent through a local Node.js proxy, run normal requests through the one-shot runner, and manage Studio Agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote action confirmations may be approved automatically by default. <br>
Mitigation: Set CZ_INTERRUPT_DECISION_MODE to auto_reject or off unless automatic approval is intentional for the deployment. <br>
Risk: The configured Studio WebSocket URL can contain a reusable ClickZetta token. <br>
Mitigation: Treat CZ_AGENT_WS_URL as secret material, avoid sharing logs or chat output that include it, and rotate the token if exposure is suspected. <br>
Risk: The bridge connects local agent execution to a remote Studio endpoint controlled by configuration. <br>
Mitigation: Install and run the skill only when the publisher and configured Studio endpoint are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luketalent/cz-studoio-agent) <br>
- [Publisher profile](https://clawhub.ai/user/luketalent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from the proxy runner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normal requests use a one-shot Node.js runner that returns a single JSON object containing success content or a structured error.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
