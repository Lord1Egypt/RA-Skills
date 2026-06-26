## Description: <br>
Agent Interconnect helps agents discover and invoke other AI agents for cross-platform collaboration, task delegation, and multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HuaiBuer](https://clawhub.ai/user/HuaiBuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or call lightweight WebSocket-based agent endpoints, delegate work to specialized agents, and maintain a small registry of available capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Delegated prompts, parameters, or task data may be visible to the operator of a remote agent endpoint. <br>
Mitigation: Use only trusted endpoints, prefer wss://, and do not send secrets, private files, credentials, or sensitive personal data to unknown agents. <br>
Risk: Live WebSocket calls depend on the Python websockets package even though the release metadata only declares python3 as a binary requirement. <br>
Mitigation: Confirm required Python dependencies are installed in the agent environment before relying on live agent-to-agent calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HuaiBuer/a2a-waai) <br>
- [Publisher profile](https://clawhub.ai/user/HuaiBuer) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WebSocket endpoint URLs, action names, and JSON-style message parameters supplied by the user.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence; artifact frontmatter metadata.version is 1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
