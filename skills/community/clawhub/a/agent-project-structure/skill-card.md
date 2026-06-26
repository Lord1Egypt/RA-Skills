## Description: <br>
Agent project directory structure specification that guides agents to organize project files, logs, temporary files, configuration, data, scripts, and documentation into separate standard directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songxf1024](https://clawhub.ai/user/songxf1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to check whether an existing workspace follows a standard project directory layout or to create that layout for a new project. It is useful when logs, temporary screenshots or caches, configuration, data, scripts, and documentation need to stay separated from project source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The create script can add directories and write small template files under the selected target path. <br>
Mitigation: Run it only on a new or reviewed target path, and inspect the path before confirming execution inside an existing project. <br>
Risk: The directory convention may not match a project's existing layout or team-specific organization rules. <br>
Mitigation: Use the structure as a default convention and adjust when the user or project documentation specifies a different layout. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songxf1024/agent-project-structure) <br>
- [QUICK_START.md](QUICK_START.md) <br>
- [PROJECT_STRUCTURE.md](references/PROJECT_STRUCTURE.md) <br>
- [GITIGNORE.md](references/GITIGNORE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create directories and small template files when the create script is run against a target path.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
