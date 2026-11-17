## Description:

Organizes local computer files using a Six Dimensions of Life model, classifying by filename semantics, moving collection folders as units, and creating only needed directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keson1521](https://clawhub.ai/user/keson1521)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to have an agent organize a chosen local folder into a personal two-level taxonomy for health, wealth, relationships, entertainment, knowledge, and wisdom. It is intended for semantic file sorting, collection-folder handling, and directory creation without deleting files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reorganize many local files without a required preview or confirmation.

Mitigation: Use it only on a narrow folder you choose, preferably after a backup, and ask the agent for a dry-run manifest before allowing changes.

Risk: Broad execution could move or rename files in home folders, system folders, synced drives, or active project directories.

Mitigation: Avoid those locations and confirm the planned actions have no overwrites or symlink escapes before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keson1521/skills/file-steward)
- [ClawHub publisher profile](https://clawhub.ai/user/keson1521)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown report with file organization actions and optional move or rename manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file moves, renames, and directory creation; no deletion is authorized by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
