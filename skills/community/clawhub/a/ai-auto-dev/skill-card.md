## Description: <br>
AI全自动化编程,Claude Code作为项目经理指挥Builder自动完成编程任务(需求对齐→指令生成→自动执行→验收→文档归档暂存). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwangxiang](https://clawhub.ai/user/mwangxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to coordinate an AI project-manager and builder workflow for coding tasks, including requirements alignment, spec generation, execution, validation, and documentation staging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks an AI builder to change files and run commands with broad project access. <br>
Mitigation: Run it only in a tightly scoped or disposable project and review generated specs, commands, and diffs before allowing execution. <br>
Risk: The workflow recommends bypassing confirmations and using unrestricted execution for builder tools. <br>
Mitigation: Keep approvals enabled where possible and avoid danger-full-access style settings unless the project is isolated and the commands are understood. <br>
Risk: The workflow can automatically stage documentation and synchronize commits, tags, or pushes to GitHub. <br>
Mitigation: Disable or manually gate commit, tag, and push behavior unless automatic remote synchronization is explicitly intended. <br>
Risk: Persistent progress files, logs, and archive files may capture sensitive project details. <br>
Mitigation: Review generated logs and staging files before sharing, committing, or pushing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mwangxiang/ai-auto-dev) <br>
- [Publisher profile](https://clawhub.ai/user/mwangxiang) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural guidance for delegating coding work, tracking progress, validating generated files, and staging documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
