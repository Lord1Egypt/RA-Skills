## Description: <br>
Automatically sort and rename files by type into structured folders with undo support, configurable filters, and dry-run preview for safe batch organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize busy local directories, especially Downloads-style folders, by previewing, sorting, renaming, and optionally undoing file moves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move and rename local files immediately, including important or synced directories if directed there. <br>
Mitigation: Run dry-run first on a small test folder, avoid important or synced directories until behavior is verified, and keep backups. <br>
Risk: Undo depends on the local organization log and may not cover every recovery scenario after files are changed or logs are missing. <br>
Mitigation: Keep the organization log with the affected files and validate restore behavior on noncritical test data before relying on undo for important files. <br>


## Reference(s): <br>
- [File Type Patterns Reference](references/file-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/indigas/claw-file-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May preview planned moves with dry-run and describe file organization results when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
