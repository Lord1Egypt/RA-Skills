## Description: <br>
Spawns a new OpenClaw agent through a short conversation, carrying over provider settings, API keys, tools, plugins, and workspace skills from the current agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AustinEral](https://clawhub.ai/user/AustinEral) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to provision a new OpenClaw agent on Docker or bare metal while preserving relevant current-agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can gather and copy broad API keys, tokens, plugins, and skills into another persistent OpenClaw agent. <br>
Mitigation: Review each credential, plugin, and skill before copying, and avoid broad TOKEN/API_KEY environment harvesting unless the operator explicitly intends it. <br>
Risk: The generated agent may be LAN-accessible and retain copied access after setup. <br>
Mitigation: Prefer local-only binding unless LAN exposure is needed, confirm the deployment plan before execution, and revoke copied credentials or stop the new agent if access should be removed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AustinEral/agent-spawner) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw.git) <br>
- [OpenClaw installer](https://openclaw.ai/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment plans, command sequences, copied configuration guidance, and final access details for the new agent.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
