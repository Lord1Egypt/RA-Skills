## Description:

Dieser Skill ermöglicht die Abfrage von Statusinformationen und die Steuerung einer AVM FRITZ!Box über die TR-064 Schnittstelle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wolf128058](https://clawhub.ai/user/wolf128058)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network administrators, and FRITZ!Box owners use this skill to inspect router status, traffic, connected hosts, WLAN state, and call lists, and to run router control commands when explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Router control commands can reboot the FRITZ!Box, force a reconnect, or disable WLAN for all users on the network.

Mitigation: Require explicit user confirmation before running reboot, reconnect, wlan off, or other router-changing commands.

Risk: Router credentials and target host configuration are read from environment files with weak scoping.

Mitigation: Use a dedicated low-privilege FRITZ!Box account where possible, restrict permissions on the skill-specific environment file, and verify FRITZBOX_HOST points only to the intended router.

Risk: Host lists and call logs can expose network device details and communication metadata.

Mitigation: Run calls and verbose host-list commands only when needed and avoid sharing their output beyond trusted users.

Risk: Unpinned Python dependencies can change behavior across installs.

Mitigation: Pin dependencies or install the skill in an isolated virtual environment before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wolf128058/skills/fritz-connection)
- [fritzconnection library](https://github.com/kbr/fritzconnection)
- [fritzconnection documentation](https://fritzconnection.readthedocs.io/)
- [AVM TR-064 interfaces](https://avm.de/service/schnittstellen/)
- [AVM TR-064 service description](https://fritz.box:49000/tr64desc.xml)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Router commands depend on local FRITZ!Box TR-064 access and configured credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
