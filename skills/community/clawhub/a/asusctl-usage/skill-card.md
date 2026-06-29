## Description: <br>
Use when controlling ASUS ROG laptop hardware after asusctl / asusd / rog-control-center have been compiled and installed. Covers the asusctl CLI command tree, common tasks (profiles, fan curves, aura LEDs, battery charge limit, armoury BIOS settings), GUI, user-daemon custom effects, keybinds, verification, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-ht](https://clawhub.ai/user/alex-ht) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, Linux users, and support agents use this skill to guide post-install runtime control of compatible ASUS ROG, TUF, and Zephyrus laptop hardware. It helps users discover supported features, choose safe asusctl commands, configure profiles, fan curves, lighting, battery limits, and troubleshoot daemon or feature availability issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardware control commands can change fan curves, charge limits, lighting behavior, or firmware-style Armoury settings on compatible ASUS laptops. <br>
Mitigation: Run discovery commands first, avoid applying fan curves or Armoury settings blindly, save work before GPU or firmware-style changes, and keep reset or default commands available. <br>
Risk: The guide contains user-run shell commands for system and user daemons. <br>
Mitigation: Review commands before execution and confirm the installed asusctl tools, daemon status, D-Bus policy, and hardware support match the target machine. <br>


## Reference(s): <br>
- [ClawHub release: Asusctl Usage](https://clawhub.ai/alex-ht/asusctl-usage) <br>
- [Publisher profile: alex-ht](https://clawhub.ai/user/alex-ht) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only guidance; commands are visible and intended for review before execution.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
