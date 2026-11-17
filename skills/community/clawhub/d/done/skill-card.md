## Description:

Automatically extracts ZIP-packaged skills and installs them to WSL2 and a Windows desktop skills folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetik-yue](https://clawhub.ai/user/aetik-yue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install ZIP-packaged skills into WSL2 and a Windows desktop backup location with progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can overwrite or delete unintended folders when given a crafted skill ZIP.

Mitigation: Install only trusted ZIP packages, review the package SKILL.md before installation, and prefer a version that validates skill names, rejects path traversal, uses unique temporary directories, and asks before overwrite or deletion.

Risk: Existing skill folders are overwritten during installation.

Mitigation: Back up existing skill folders or require explicit confirmation before replacing an installed skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aetik-yue/skills/done)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text progress updates with command-oriented installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, overwrite, and delete local skill directories during installation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
