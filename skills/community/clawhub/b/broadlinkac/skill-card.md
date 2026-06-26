## Description: <br>
BroadlinkAC For Agent helps agents install and use a Python Broadlink RM air-conditioner controller with weather-aware automation, IR learning, scheduling, logging, and diagnostic workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oywq00008-cell](https://clawhub.ai/user/oywq00008-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Broadlink RM infrared control for air conditioners, query weather and storm data, learn custom IR codes, and manage persistent schedules or automation from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real air conditioner through a Broadlink infrared device. <br>
Mitigation: Confirm the target device, location, and requested action with the user before sending control commands. <br>
Risk: Initialization and learned IR workflows can persist API keys, device settings, custom codes, schedules, and logs under the user's home directory. <br>
Mitigation: Disclose the local persistence path before setup and avoid storing credentials or schedules unless the user has approved them. <br>
Risk: Schedules, auto-adjustment, and storm shutdown can continue autonomously after the immediate agent task finishes. <br>
Mitigation: Enable autonomous behavior only after explicit approval and provide a disable path for schedules and auto-adjustment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oywq00008-cell/broadlinkac) <br>
- [BroadlinkAC For Agent Repository](https://github.com/oywq00008-cell/BroadlinkAC-For-Agent.git) <br>
- [BroadlinkAC For Agent Releases](https://github.com/oywq00008-cell/BroadlinkAC-For-Agent/releases/latest) <br>
- [BroadlinkAC OpenWRT](https://github.com/oywq00008-cell/BroadlinkAC-OpenWRT) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create persistent local configuration and enable device automation after user confirmation.] <br>

## Skill Version(s): <br>
5.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
