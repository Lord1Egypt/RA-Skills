## Description: <br>
Use when users ask to generate Java code from database tables with EasyCode-style templates, including parsing db config, remembering last-used generation settings, resolving output paths from base package, and producing a file generation plan/execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huhua1990](https://clawhub.ai/user/huhua1990) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Java and MyBatis-style project code from database tables. It helps normalize generation inputs, plan output files, resolve package paths, fetch table metadata when needed, and execute EasyCode-style rendering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database credentials may be saved in local state, including plaintext passwords. <br>
Mitigation: Use least-privilege database accounts, avoid production passwords, and inspect .easycode-skill/state.json after use. <br>
Risk: Optional project formatting commands can execute local commands. <br>
Mitigation: Only enable --run-project-format or project_format_command for commands that have been reviewed and are fully trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huhua1990/easycode-skill) <br>
- [Function Schema](references/function-schema.json) <br>
- [Template Groups](references/template-groups.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON specs, shell commands, and generated Java source files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans file writes before execution; execution may write generated files and update local state.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
