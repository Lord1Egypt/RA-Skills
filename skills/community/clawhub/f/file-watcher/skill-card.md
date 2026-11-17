## Description:

Monitor directories for changes with snapshots, diffs, glob filtering, and event detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation builders, agents, and operations teams use File Watcher to detect created, modified, and deleted files, capture snapshots, compare filesystem states, and emit JSON for pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions download executable Python from a mutable GitHub branch without integrity verification.

Mitigation: Review the install path and prefer the bundled file_watcher.py or a pinned, verified release before execution.

Risk: Watching or snapshotting broad directories can store sensitive file paths, sizes, timestamps, and hashes in JSON output.

Mitigation: Scope watched paths narrowly, use glob and ignore filters for sensitive areas, and treat snapshot JSON as sensitive metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itspremkumar/skills/file-watcher)
- [File Watcher GitHub repository](https://github.com/itsPremkumar/file-watcher)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON snapshot or diff output when the tool is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce filesystem event summaries, saved JSON snapshots, and snapshot comparison reports.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
