## Description:

Use when controlling ASUS ROG laptop hardware after asusctl, asusd, and rog-control-center have been compiled and installed, covering runtime CLI commands, GUI usage, keybinds, verification, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex-ht](https://clawhub.ai/user/alex-ht)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Linux users, and support agents use this skill to operate supported ASUS ROG, TUF, and Zephyrus laptop hardware after asusctl is installed. It helps agents provide safe runtime commands for profiles, fan curves, RGB/AniMe features, battery charge limits, Armoury settings, health checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardware-control commands can affect thermals, battery life, display routing, or require a reboot.

Mitigation: Check current values and supported features with the listed info, list, and get commands before applying set commands.

Risk: Fan curves, charge limits, and Armoury/GPU MUX settings may be unsupported or inappropriate for a specific laptop model.

Mitigation: Use asusctl info --show-supported and model-specific list commands first, then apply only supported changes and keep reset/default commands available.

## Reference(s):

- [ClawHub Asusctl Usage skill page](https://clawhub.ai/alex-ht/skills/asusctl-usage)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be checked against the laptop's supported features before execution.]

## Skill Version(s):

0.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
