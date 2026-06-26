## Description: <br>
Provides safe local file read, write, and listing guidance scoped by default to the OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanz](https://clawhub.ai/user/huanz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to view, edit, list, and create files within an OpenClaw workspace, including logs, Markdown reports, scripts, and configuration files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read, list, and edit workspace files, which may expose or alter sensitive project content. <br>
Mitigation: Keep sensitive files outside the workspace when possible and review important file edits before relying on them. <br>
Risk: Writes outside the intended workspace could affect user files beyond the skill's stated scope. <br>
Mitigation: Use relative paths or workspace subdirectories and avoid write operations outside the workspace. <br>
Risk: Destructive file operations can remove important configuration, source, or system files. <br>
Mitigation: Avoid deletion of important files and require explicit user intent before destructive edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huanz/filesystem-access) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text, Markdown, code snippets, shell commands, and file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should stay scoped to workspace file operations and avoid destructive edits unless explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
