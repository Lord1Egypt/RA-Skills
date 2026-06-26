## Description: <br>
Manage, organize, classify, rename, archive, and clean files and folders with dedicated workspace setup, automated sorting, and conflict handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qshan1](https://clawhub.ai/user/qshan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent scan workspaces, classify files, create folder structures, rename files, maintain manifests, archive old items, and generate file organization reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File moves or renames can affect a workspace if the wrong root folder is selected. <br>
Mitigation: Confirm the exact root folder, start with dry-run reports, and review proposed moves and renames before execution. <br>
Risk: Broad workspace automation can organize more files than intended. <br>
Mitigation: Scope the skill to a dedicated workspace and enable weekly automation only after the rules have been reviewed. <br>
Risk: Archival and cleanup behavior may make files harder to find even when files are not deleted. <br>
Mitigation: Keep manifest updates and organization reports enabled, and review archive destinations before applying cleanup actions. <br>


## Reference(s): <br>
- [File Types Reference](references/file-types.md) <br>
- [Naming Rules Reference](references/naming-rules.md) <br>
- [Project Templates Reference](references/project-templates.md) <br>
- [ClawHub Release Page](https://clawhub.ai/qshan1/dedicated-file-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON configuration, manifest files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or execute local file moves, renames, directory creation, manifest updates, and dry-run reports when used with an agent that has filesystem access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
