## Description: <br>
Creates and wires a new Feishu-only OpenClaw agent by guiding routing selection, adding the agent runtime, updating OpenClaw configuration, restarting the gateway, and verifying bindings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meichuanyi](https://clawhub.ai/user/meichuanyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create Feishu-only OpenClaw agents, choose account or peer routing, update OpenClaw configuration, and verify gateway bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change OpenClaw routing and session configuration. <br>
Mitigation: Back up and review ~/.openclaw/openclaw.json before execution, confirm the intended account or peer route, and verify bindings after gateway restart. <br>
Risk: Feishu app secrets may be exposed through command arguments or command output. <br>
Mitigation: Avoid entering app secrets directly in command lines where shell history is retained, and redact appSecret values from shared logs or outputs. <br>
Risk: A mistaken account or peer route can bind traffic to the wrong agent. <br>
Mitigation: Use the required scenario-alignment step, follow the guided group confirmation gates for peer routing, and reject route conflicts before writing configuration. <br>


## Reference(s): <br>
- [Routing Modes Reference](references/routing-modes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and configuration summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON summaries from the bundled upsert script and verification command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
