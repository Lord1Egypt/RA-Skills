## Description: <br>
Perform advanced filesystem tasks including listing, recursive file searches, batch copying, moving, deleting, directory size analysis, and file type filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vetas67](https://clawhub.ai/user/Vetas67) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to generate practical filesystem command guidance for listing, searching, filtering, analyzing, and batch-managing local files and directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local filesystem commands can modify, move, rename, or delete unintended files when applied to overly broad paths or patterns. <br>
Mitigation: Ask the agent to show the exact matched files and command before execution, avoid broad home or system paths unless intentional, and keep backups for important data. <br>
Risk: In-place replacement and batch cleanup examples can be difficult to reverse after execution. <br>
Mitigation: Preview matches first, use dry-run or interactive modes where available, and prefer a backup copy before destructive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Vetas67/filesystem-1-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/Vetas67) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include filesystem command examples for listing, searching, copying, moving, deleting, renaming, and directory analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
