## Description:

Bidirectional file synchronization tool using MD5 hash and version history for conflict detection across two directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[67available](https://clawhub.ai/user/67available)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to set up and run bidirectional folder sync between two trusted directories, with conflict copies, trash preservation, version history, and logs for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the bundled sync script can be tricked into reading, copying, or moving files outside the chosen folders.

Mitigation: Use the skill only on folders you fully trust and control; avoid attacker-controlled USB drives or shared folders until path validation and symlink rejection are added.

Risk: Concurrent use against the same folder pair can corrupt state files or produce inconsistent sync decisions.

Mitigation: Run a single sync process per folder pair and review the generated logs, conflict folder, and trash folder after each sync.

## Reference(s):

- [Behavior Notes](references/behaviors.md)
- [ClawHub Skill Page](https://clawhub.ai/67available/skills/file-sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, file paths, and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to generated sync logs, state files, conflict folders, and trash folders created by the bundled sync script.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
