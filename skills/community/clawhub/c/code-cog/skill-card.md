## Description: <br>
Code Cog lets agents delegate coding tasks to CellCog Co-work for code generation, debugging, refactoring, codebase exploration, and approved local terminal and file operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Code Cog when an agent needs to inspect a project, modify code, run tests or shell commands, and return implementation results through CellCog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local project file and terminal access can modify files or run commands in the configured workspace. <br>
Mitigation: Keep cowork_working_directory narrow, review terminal and write approvals, and enable write auto-approval only when unattended changes are acceptable. <br>
Risk: The skill requires a sensitive CELLCOG_API_KEY credential. <br>
Mitigation: Protect the API key and avoid exposing it in prompts, logs, generated files, or shared project artifacts. <br>
Risk: Generated code or command recommendations may introduce incorrect behavior. <br>
Mitigation: Review diffs and run the project's tests, linters, or build checks before relying on changes. <br>


## Reference(s): <br>
- [Code Cog on ClawHub](https://clawhub.ai/nitishgargiitd/code-cog) <br>
- [CellCog](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Text or Markdown responses with code snippets, shell commands, and generated or modified project files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CellCog Desktop, python3, CELLCOG_API_KEY, and a configured working directory for local Co-work access.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
