## Description: <br>
AC-Nexus helps agents install and use a Python smart air-conditioner controller for Broadlink RM and Xiaomi MIoT IR devices, including weather-aware automation, scheduling, logging, and storm shutdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oywq00008-cell](https://clawhub.ai/user/oywq00008-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up and control supported air conditioners through Broadlink or Xiaomi MIoT infrared devices, including local scheduling, weather-based adjustment, and storm-related shutdown workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create durable local configuration and background schedules that continue after the agent task ends. <br>
Mitigation: Confirm with the user before enabling or changing schedules, auto-adjust, or storm shutdown, and disable schedule_enabled and auto_adjust when automation is no longer wanted. <br>
Risk: Device tokens, weather API keys, and local device settings may be stored in persistent configuration. <br>
Mitigation: Use the skill only with devices and accounts the user controls, avoid exposing stored config, and review dependency and repository trust before installation. <br>
Risk: Commands can affect real air-conditioning devices and may change home or facility conditions. <br>
Mitigation: Ask for explicit confirmation before sending device-control commands or changing device configuration such as brand, temperature rules, or location. <br>


## Reference(s): <br>
- [ClawHub listing for AC-Nexus](https://clawhub.ai/oywq00008-cell/acnexus) <br>
- [AC-Nexus repository link mentioned in artifact](https://github.com/oywq00008-cell/AC-Nexus.git) <br>
- [AC-Nexus releases link mentioned in artifact](https://github.com/oywq00008-cell/AC-Nexus/releases/latest) <br>
- [AC-Nexus OpenWRT companion link mentioned in artifact](https://github.com/oywq00008-cell/AC-Nexus-OpenWRT) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent local configuration and device-control commands that require user confirmation before execution.] <br>

## Skill Version(s): <br>
5.3.1 (source: server release metadata; artifact frontmatter reports 5.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
