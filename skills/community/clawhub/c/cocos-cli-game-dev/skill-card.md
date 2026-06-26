## Description: <br>
Create, build, and modify 2D or 3D Cocos game projects using the Cocos CLI and Cocos MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyihunter](https://clawhub.ai/user/liuyihunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create Cocos game projects, make scene and game changes through the Cocos MCP server, and build web test packages with the Cocos CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to start and automatically trust a long-running local Cocos MCP server. <br>
Mitigation: Confirm the project directory and MCP registration before use, keep the server bound locally, and stop it after the task. <br>
Risk: Troubleshooting logs may capture command output or project context in `.learnings/ERRORS.md`. <br>
Mitigation: Review `.learnings/ERRORS.md` before sharing or committing the project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuyihunter/cocos-cli-game-dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify Cocos project files through Cocos CLI and MCP tooling.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
