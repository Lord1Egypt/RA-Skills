## Description:

Claw Drive is an OpenClaw skill for auto-categorizing, tagging, deduplicating, syncing, and retrieving personal files through the claw-drive CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiyuanw101](https://clawhub.ai/user/zhiyuanw101)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Claw Drive to let an OpenClaw agent store incoming files, create searchable metadata, retrieve previously stored files, and manage optional Google Drive sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-assisted personal file management creates persistent local indexes that may contain sensitive descriptions.

Mitigation: Ask for consent before reading file contents, keep sensitive descriptions brief and redacted, and review index metadata before relying on it.

Risk: Optional Google Drive sync may include sensitive identity files if exclusions are misconfigured.

Mitigation: Before enabling sync, verify the exclude list and keep identity documents out of synced paths.

Risk: Migration, reindex, and delete workflows can affect files beyond the intended targets.

Mitigation: Apply only plans you created and reviewed, use summaries or dry runs where available, and confirm exact target paths before deleting files.

Risk: Implementation flaws can exceed the skill's intended file boundaries.

Mitigation: Review and scan the skill before deployment, and run it against a constrained local drive directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhiyuanw101/skills/claw-drive)
- [Publisher Profile](https://clawhub.ai/user/zhiyuanw101)
- [Skill Homepage](https://github.com/dissaozw/claw-drive)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Sync Documentation](docs/sync.md)
- [Security Documentation](docs/security.md)
- [Tags Documentation](docs/tags.md)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, category tags, descriptions, and dry-run or status output for review.]

## Skill Version(s):

0.4.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
