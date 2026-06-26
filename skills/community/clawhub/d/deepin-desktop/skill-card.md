## Description: <br>
Control and manage Deepin/UOS desktop settings including power, display, Bluetooth, airplane mode, user accounts, time, boot settings, package management, and security-related services through D-Bus commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZaneNiu](https://clawhub.ai/user/ZaneNiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and desktop support agents use this skill to inspect or propose Deepin/UOS desktop administration commands for D-Bus services. It is most relevant when managing local desktop settings, accounts, networking, package services, boot configuration, and troubleshooting on Deepin-compatible systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact account, bootloader, package-management, time, network, and security-setting commands. <br>
Mitigation: Require explicit human confirmation before executing any command that changes users, groups, Grub settings, packages, time, network state, or security settings. <br>
Risk: Some D-Bus calls can alter privileged system or desktop state when run on a Deepin/UOS host. <br>
Mitigation: Use the skill only for Deepin/UOS desktop administration, inspect generated commands, and prefer read-only property queries before applying changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ZaneNiu/deepin-desktop) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Power D-Bus introspection](artifact/references/01_power1.txt) <br>
- [Display D-Bus introspection](artifact/references/02_display1.txt) <br>
- [Bluetooth D-Bus introspection](artifact/references/03_bluetooth1.txt) <br>
- [Accounts D-Bus introspection](artifact/references/06_accounts1.txt) <br>
- [Grub2 D-Bus introspection](artifact/references/15_grub2.txt) <br>
- [Linglong package manager introspection](artifact/references/16_linglong.txt) <br>
- [Defender service notes](artifact/references/24_defender.txt) <br>
- [Introspection helper script](artifact/scripts/introspect.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with D-Bus service tables and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are command references and operational guidance for an agent; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
