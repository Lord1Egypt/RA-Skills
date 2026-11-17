## Description:

Exports an OpenClaw instance's accumulated knowledge into an Obsidian-compatible ExpertPack composite for backup, migration, or portable knowledge snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianhearn](https://clawhub.ai/user/brianhearn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan an OpenClaw workspace, propose ExpertPack pack assignments, scaffold distilled pack files, compose a composite manifest, and validate the resulting export before migration or backup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic redaction may not catch every secret or sensitive operational detail.

Mitigation: Manually inspect the scan manifest and final export, especially operational/tools.md and operational/infrastructure.md, before sharing or using the export.

Risk: An output path or slug containment issue can write outside the intended export folder.

Mitigation: Run the skill only in trusted workspaces, choose a dedicated export directory, and avoid untrusted IDENTITY.md files or externally supplied scan manifests until containment checks are fixed.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installation and use it only on workspaces whose contents and file names are trusted.

## Reference(s):

- [ExpertPack homepage](https://expertpack.ai)
- [ExpertPack schema summary](references/schemas-summary.md)
- [ExpertPack schema docs](https://expertpack.ai/#schemas)
- [ClawHub skill page](https://clawhub.ai/brianhearn/skills/expertpack-export)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON scan manifests, Markdown pack files, YAML manifests, and terminal validation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; exported content should be manually reviewed for secrets and privacy-sensitive details.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
