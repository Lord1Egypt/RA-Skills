## Description: <br>
AI pair programming powered by CellCog Desktop for code, debugging, refactoring, and local development workflows on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to delegate coding, debugging, refactoring, DevOps, data pipeline, and documentation tasks to CellCog agents working within a local project directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud agents can receive auto-approved terminal and file-operation access on the user's machine. <br>
Mitigation: Install only for intentional local co-work use, scope each session to a dedicated project directory, keep work under version control, and narrow or disable auto-approval when autonomous writes or commands are not acceptable. <br>
Risk: The skill requires CELLCOG_API_KEY and CellCog Desktop, which can expose local development workflows to a remote coding service. <br>
Mitigation: Verify how the desktop app stores the API key, avoid sensitive folders, review generated changes before relying on them, and stop or disconnect CellCog Desktop when co-work access is no longer needed. <br>


## Reference(s): <br>
- [Cowork Cog on ClawHub](https://clawhub.ai/nitishgargiitd/cowork-cog) <br>
- [CellCog](https://cellcog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; CellCog responses may include JSON and task results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the cellcog dependency, CELLCOG_API_KEY, and CellCog Desktop for local co-work sessions.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
