## Description: <br>
Automatically scans and cleans completed C tasks weekly, compressing insights into MEMORY.md and generating cleanup reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People who manage C-class task files can run or schedule this skill to summarize useful completed-task notes into memory, clear completed entries, and create a cleanup report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script overwrites completed task records and has no built-in dry-run or undo mode. <br>
Mitigation: Confirm the configured paths, test on a copy of the task file, and keep backups before installing or scheduling it. <br>
Risk: Selected completed-task content may be retained in local memory and cleanup report files. <br>
Mitigation: Review task content and storage locations before running it when completed tasks may contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/largetool/c-task-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown reports and local file updates with console logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to configured task, memory, and log paths on the local filesystem.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
