## Description: <br>
Helps an agent organize Jeff's local documents by proposing and, after confirmation, applying Chinese folder naming and categorization rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamdracula](https://clawhub.ai/user/iamdracula) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Personal-agent users use this skill when Jeff asks an agent to reorganize a local folder. The agent scans the folder, proposes a structure, and after confirmation moves files, preserves original filenames, applies pinyin-initial prefixes to top-level Chinese folder names, and removes empty directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Folder renames, file moves, and empty-directory removal can cause misplaced files or unwanted local changes. <br>
Mitigation: Review the proposed moves, folder renames, and empty directories before execution, and keep backups for important document collections. <br>
Risk: Similar organization names can be incorrectly merged during classification. <br>
Mitigation: Keep distinct entities separate when the skill calls out a difference, and ask Jeff before acting on uncertain classifications. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iamdracula/file-organization-rules) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with proposed file operations and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to show the plan before making uncertain changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
