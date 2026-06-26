## Description: <br>
Agent2Agent (A2A) Protocol implementation - communicate with other AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to discover A2A agent cards, register agents, send messages, and submit or monitor tasks against configured remote A2A endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, task data, and agent messages are sent to the configured remote A2A endpoint. <br>
Mitigation: Use only trusted endpoints and avoid sending secrets or sensitive files unless the endpoint's storage and processing practices are understood. <br>
Risk: Optional API keys or bearer tokens are used for authentication to remote services. <br>
Mitigation: Provide credentials only for trusted registries and rotate or revoke them if endpoint trust changes. <br>


## Reference(s): <br>
- [A2A Protocol Homepage](https://a2a-protocol.org) <br>
- [ClawHub Skill Page](https://clawhub.ai/nantes/a2a-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime client output is JSON responses and status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and requests; uses a configured A2A registry endpoint and optional bearer token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
