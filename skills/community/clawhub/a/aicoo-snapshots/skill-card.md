## Description:

Aicoo Snapshots helps an agent save, list, and restore note versions through Aicoo OS snapshot endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xisen-w](https://clawhub.ai/user/xisen-w)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users working with Aicoo notes use this skill to create pre-edit backups, inspect snapshot history, restore a specific note version, and schedule folder-level backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An Aicoo API key could be sent through an unvalidated base URL in examples that use PULSE_BASE.

Mitigation: Use a least-privilege Aicoo API key and run PULSE_BASE examples only after fixing and verifying the official Aicoo API endpoint.

Risk: Restore, edit, and bulk backup operations can modify notes or affect many notes when the target is ambiguous.

Mitigation: Require explicit note IDs, version IDs, and folder scope before executing restore, undo, edit, or scheduled backup commands.

## Reference(s):

- [Aicoo API base URL](https://www.aicoo.io/api/v1)
- [Aicoo Snapshots ClawHub skill page](https://clawhub.ai/xisen-w/skills/aicoo-snapshots)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides curl examples for Aicoo OS snapshot and note endpoints.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter metadata.version is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
