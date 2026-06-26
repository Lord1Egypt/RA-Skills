## Description: <br>
Stop AI from scattering files everywhere by enforcing consistent naming and directory structure for agent-created outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lujun2508](https://clawhub.ai/user/lujun2508) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI-agent users, and workspace maintainers use this skill to keep generated files in predictable project directories with consistent names. It helps reduce file-hunting and cleanup overhead when agents create deliverables, scripts, data, documentation, and temporary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cleanup guidance could remove rejected or temporary files too broadly if an agent applies it outside the current task scope. <br>
Mitigation: Confirm exact paths before deleting files, limit cleanup to temporary or rejected files created during the current task, and use explicit output paths for important projects. <br>


## Reference(s): <br>
- [Workspace Guardian on ClawHub](https://clawhub.ai/lujun2508/file-rules) <br>
- [Publisher profile](https://clawhub.ai/user/lujun2508) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with file paths, naming patterns, and brief saved-location confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies to Windows, Linux, and macOS agent workspaces.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release evidence; artifact frontmatter lists 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
