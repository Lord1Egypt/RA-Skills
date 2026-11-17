## Description:

OpenClaw Agent Clone exports and imports OpenClaw agent configuration packages for sharing, cloning, backup, and restoration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anwhere](https://clawhub.ai/user/anwhere)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to export an agent's identity, configuration, installed skill list, and optional memory into a shareable package, or import such a package to clone an agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Importing a package can overwrite agent identity and configuration files.

Mitigation: Review the package contents before import, keep the generated backups, and test imports in a disposable workspace when possible.

Risk: Imported packages can install additional skills and change future agent behavior.

Mitigation: Import only from trusted sources and review the package's skill list before allowing installation.

Risk: Exported packages may contain sensitive identity, configuration, or optional memory content.

Mitigation: Inspect exported packages manually before sharing and include memory only when the user explicitly intends to share it.

Risk: Import behavior can write outside the intended workspace if environment paths are misconfigured.

Mitigation: Confirm the target OpenClaw workspace paths before import and run the skill with least necessary file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anwhere/skills/claw-clone)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON clone package and plain-text import/export report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Export mode filters configured sensitive fields; import mode can write configuration files, create .bak backups, and install missing skills.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
