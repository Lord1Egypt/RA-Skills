## Description: <br>
File Classification Manager routes workspace files into synchronized project output and temporary directories based on file purpose and project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sun2001](https://clawhub.ai/user/sun2001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent workflows use this skill to keep OpenClaw workspaces organized by routing generated outputs, intermediate files, source documents, and cleanup candidates into project-specific `projects/` and `temp/` directories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically read and move files in a workspace without a built-in preview or confirmation step. <br>
Mitigation: Use it first on non-critical workspaces or with explicit review, backups, and rollback planning before broad cleanup. <br>
Risk: Automatic project detection and file classification can route files to an unexpected project or storage area. <br>
Mitigation: Provide explicit project context for important files and review migration reports after cleanup operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sun2001/file-classification-manager) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [JavaScript module APIs and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces destination paths and migration reports when used by an agent or workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
