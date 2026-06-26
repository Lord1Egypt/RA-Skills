## Description: <br>
Automates setup and configuration of multiple Feishu/Lark bots with OpenClaw, including independent workspaces, dedicated agents, credential-backed Feishu channels, routing bindings, customizable personalities, and WebSocket or webhook connection modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcz5221-svg](https://clawhub.ai/user/lcz5221-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create and configure multiple Feishu/Lark bots for OpenClaw, including independent workspaces, agent identity files, Feishu channel settings, and routing bindings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can run local shell commands using values from the bot configuration. <br>
Mitigation: Review or patch scripts/setup_bots.py before running it, and only use configuration files you created and validated yourself. <br>
Risk: Feishu credentials are written into persistent OpenClaw configuration. <br>
Mitigation: Protect or remove JSON files that contain Feishu secrets, restrict bot permissions where possible, and back up ~/.openclaw/openclaw.json before setup. <br>
Risk: Restarting the OpenClaw gateway can affect active bots. <br>
Mitigation: Plan gateway restarts during an appropriate maintenance window and verify active bot bindings afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lcz5221-svg/feishu-duoge) <br>
- [Example configuration](references/example-config.json) <br>
- [Setup script](scripts/setup_bots.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and configuration artifacts for OpenClaw Feishu bot workspaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
