## Description:

Control NGBS iCON Smart Home thermostats through the enzoldhazam.hu service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniel-laszlo](https://clawhub.ai/user/daniel-laszlo)

### License/Terms of Use:

MIT

## Use Case:

External users and home automation operators use this skill to check thermostat status, inspect room and device readings, and prepare commands that adjust target temperatures for NGBS iCON Smart Home devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact does not include the full installable CLI while setup instructions build mutable external code.

Mitigation: Use a pinned, reviewed release and verify its checksum or signature before installation.

Risk: System-wide installation can require elevated privileges and expands local impact if the built binary is untrusted.

Mitigation: Install into a user-owned bin directory instead of using sudo or writing to /usr/local/bin.

Risk: Long-lived shell environment variables can expose thermostat account credentials.

Mitigation: Prefer macOS Keychain login and avoid storing credentials in shell startup files.

Risk: Thermostat set commands can change a home's physical environment.

Mitigation: Require explicit user confirmation before every temperature change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daniel-laszlo/skills/enzoldhazam)
- [enzoldhazam.hu service](https://www.enzoldhazam.hu)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an enzoldhazam.hu account with registered NGBS iCON devices; temperature changes require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
