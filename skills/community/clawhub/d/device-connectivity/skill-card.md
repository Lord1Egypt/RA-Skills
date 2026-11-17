## Description:

Use when pairing a phone with Linux via KDE Connect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mina-atef-00](https://clawhub.ai/user/mina-atef-00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux desktop users use this skill to pair Android or iOS phones with Linux desktops for file sharing, notification sync, clipboard sync, media control, and related KDE Connect protocol features.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone-to-desktop integration can expose notifications, clipboard content, files, media controls, and related device features to paired devices.

Mitigation: Pair only trusted devices, enable only needed features, and use the integration on trusted local networks.

Risk: Firewall changes can open KDE Connect or Valent ports on networks where device discovery is not desired.

Mitigation: Check the active firewall zone before changing rules, open only the documented ports when required, and avoid opening them on untrusted networks.

Risk: The Valent Flatpak install uses an external Flatpak reference and permissions for desktop integration services.

Mitigation: Review the Flatpak source and permissions before installing or running Valent.

Risk: Running KDE Connect and Valent together can cause a port conflict on port 1716.

Mitigation: Run only one KDE Connect protocol implementation at a time.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mina-atef-00/skills/device-connectivity)
- [OpenClaw homepage](https://github.com/mina-atef-00/agent-skills)
- [Valent Flatpak reference](https://valent.andyholmes.ca/valent.flatpakref)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Linux-focused setup guidance for KDE Connect, Valent, and GSConnect; includes firewall and Flatpak notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
