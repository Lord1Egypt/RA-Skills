## Description: <br>
Perform advanced filesystem tasks including recursive listing, name and content searching, batch copying, moving, deleting, and directory size and type analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanth-hn](https://clawhub.ai/user/srikanth-hn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for practical filesystem workflows, including listing directories, searching files and content, analyzing directory structure and size, and preparing scoped batch file operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch copy, move, delete, rename, or sed replacement commands can modify or remove unintended files if paths or matches are too broad. <br>
Mitigation: Review the exact command, path scope, and file list before execution; keep operations inside the intended project directory and back up important files before destructive changes. <br>
Risk: Filesystem searches and previews can expose private or sensitive files when run across broad directories. <br>
Mitigation: Limit searches to the intended workspace and avoid system, home, credential, or private directories unless that access is explicitly intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be reviewed and scoped before execution, especially copy, move, delete, rename, and sed replacement operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
