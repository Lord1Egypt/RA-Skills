## Description: <br>
Control USB relay modules with on/off switching, state tracking, and automation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LJ-Hao](https://clawhub.ai/user/LJ-Hao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent control a connected USB relay for on/off switching, toggling, status tracking, and simple hardware automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can switch real connected hardware through a USB relay. <br>
Mitigation: Install and use it only for intended devices, test first with no load or a harmless load, and confirm each on/off action before execution. <br>
Risk: Cached relay state may not prove the physical relay position after manual override or device drift. <br>
Mitigation: Do not rely on cached status as the sole proof of physical state; verify the relay or attached device directly for safety-critical decisions. <br>
Risk: Setup may involve privileged serial-port changes or shell commands. <br>
Mitigation: Review commands such as dialout membership changes and curl-to-sudo setup before running them. <br>
Risk: Unattended automation could operate hazardous equipment. <br>
Mitigation: Avoid unattended automation for hazardous loads and keep a human approval step for physical actuation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/LJ-Hao/control-usb-relay) <br>
- [README.md](README.md) <br>
- [setup.md](setup.md) <br>
- [USAGE-GUIDE.md](USAGE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce relay-control instructions and code that interact with local serial hardware.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
