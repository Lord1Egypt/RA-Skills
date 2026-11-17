## Description:

Safe system changes with automatic baseline capture, canary testing, and rollback for critical infrastructure modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolaopenclaw](https://clawhub.ai/user/lolaopenclaw)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill when planning SSH, firewall, network, service, kernel, or package changes that could interrupt remote access. It guides baseline capture, validation, backup access, and rollback procedures for critical system modifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged rollback or update commands can affect critical system files.

Mitigation: Use the skill only with a trusted operator who understands the sudo impact and has reviewed the target files before execution.

Risk: Rollback may restore files based on backup directory and path metadata.

Mitigation: Run rollback only after confirming the backup directory and recorded original paths are trusted and match the intended system files.

Risk: Generated, remote, or partially trusted command text can be executed through update or validation arguments.

Mitigation: Do not pass untrusted text into command or validation arguments; review and quote commands explicitly before running them.

Risk: Automated validation and rollback are not reliable protection against remote lockout.

Mitigation: Keep an independent backup access method, such as a second SSH session or console access, before changing SSH, firewall, or network settings.

## Reference(s):

- [Incident Report: AllowTcpForwarding Lockout](references/incident-report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include privileged system change, validation, backup, and rollback commands.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
