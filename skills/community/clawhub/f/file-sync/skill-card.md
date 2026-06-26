## Description: <br>
Bidirectional file synchronization tool using MD5 hashes and version history for conflict detection between two user-selected directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[67available](https://clawhub.ai/user/67available) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users with two local folders use this skill to run or configure bidirectional file synchronization, such as syncing a PC folder with removable storage while preserving conflicts and deletion history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script mutates files in user-selected directories. <br>
Mitigation: Test on sample folders first, back up important data, and choose narrow paths before syncing valuable files. <br>
Risk: Conflicts and deletions are retained locally in .conflict and .trash directories. <br>
Mitigation: Review .conflict and .trash after each run before deleting or reusing retained files. <br>
Risk: State and log artifacts retain file names, hashes, timestamps, and sync actions. <br>
Mitigation: Review .sync_state.json and .sync_logs for local retention concerns before sharing or archiving synced folders. <br>


## Reference(s): <br>
- [File Sync on ClawHub](https://clawhub.ai/67available/file-sync) <br>
- [Detailed behavior notes and edge cases](references/behaviors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown with inline shell commands and local file-system artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs can mutate selected folders and create .conflict, .trash, .sync_state.json, and .sync_logs artifacts.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
