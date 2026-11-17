## Description:

Provides secure, versioned sync and restore commands for OpenClaw memory, workspace files, and custom skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arakichanxd](https://clawhub.ai/user/arakichanxd)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to back up, restore, list, and inspect versioned OpenClaw memory, workspace files, and custom skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive OpenClaw memory, workspace content, custom skills, and Git credentials.

Mitigation: Review the workspace and skill directories before installation, use a private backup repository, and configure a least-privilege token.

Risk: Restore operations can replace local agent behavior and skills, especially when confirmation is skipped with --force.

Mitigation: Avoid --force unless a separate trusted backup exists, and confirm the selected backup version before restoring.

Risk: Nested skill secrets may be captured in backup history.

Mitigation: Inspect custom skill directories for secrets before syncing and do not rely on the current implementation to exclude every nested secret.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arakichanxd/skills/claw-sync)
- [Artifact README](artifact/claw-sync/README.md)
- [Artifact Skill Definition](artifact/claw-sync/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style command guidance and terminal status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local backups, update remote Git backup contents, list versions, or restore workspace files.]

## Skill Version(s):

2.0.2 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
