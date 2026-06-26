## Description: <br>
Configures new OpenClaw agent bindings for Feishu groups and installs required skills into each new agent workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywewanhuang](https://clawhub.ai/user/ywewanhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw administrators and developers use this skill to identify agents without Feishu group bindings, propose binding configuration for review, restart the gateway after confirmation, and install a standard set of skills into the new agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw routing, installs multiple skills, and enables a persistent self-improving agent. <br>
Mitigation: Verify the agent ID and Feishu group ID, review the full openclaw.json diff, back up the configuration, approve each additional skill installation, and confirm how to stop the persistent agent and remove its stored state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ywewanhuang/config-new-agent) <br>
- [Publisher profile](https://clawhub.ai/user/ywewanhuang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before changing OpenClaw bindings or restarting the gateway.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
