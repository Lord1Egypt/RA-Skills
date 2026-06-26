## Description: <br>
Control Ecovacs robot vacuums (DEEBOT series) via the official Ecovacs MCP server: start, stop, pause, or resume cleaning; send the robot to its dock; check battery and cleaning status; and list devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users with Ecovacs DEEBOT robots use this skill to let an assistant configure and call the Ecovacs MCP server for vacuum control, docking, device listing, and real-time status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language triggers could cause an assistant to treat generic cleaning phrases as robot-vacuum control requests. <br>
Mitigation: Configure the assistant to ask for explicit confirmation before starting, stopping, pausing, resuming, or docking the robot. <br>
Risk: The Ecovacs API key grants access to robot-vacuum control through the MCP server. <br>
Mitigation: Protect ECO_API_KEY as a secret and avoid exposing it in prompts, logs, or shared configuration. <br>
Risk: The skill depends on the external ecovacs-robot-mcp package at runtime. <br>
Mitigation: Verify or pin the ecovacs-robot-mcp package where possible before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/f-liva/ecovacs-mcp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/f-liva) <br>
- [Official Ecovacs MCP server](https://github.com/ecovacs-ai/ecovacs-mcp) <br>
- [Ecovacs Open Platform](https://open.ecovacs.com) <br>
- [Ecovacs Open Platform China endpoint](https://open.ecovacs.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with MCP configuration JSON and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ECO_API_KEY and either uvx or python3 with ecovacs-robot-mcp available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
