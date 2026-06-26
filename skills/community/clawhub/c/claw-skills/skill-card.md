## Description: <br>
OpenClaw 插件开发助手，输出可运行的插件骨架、安装命令和调试步骤。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boleyn](https://clawhub.ai/user/boleyn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide whether an OpenClaw extension should be a Skill or Plugin, then generate a minimal runnable scaffold with install, debug, publish, rollback, and troubleshooting guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated install, publish, rollback, or cleanup commands could target the wrong package, registry, or path if accepted without review. <br>
Mitigation: Review package names, registry targets, paths, and destructive cleanup steps before running generated commands. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured sections and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include runnable package scaffolds, install commands, debug commands, publish commands, rollback commands, and risk troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
