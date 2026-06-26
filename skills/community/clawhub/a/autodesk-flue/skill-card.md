## Description: <br>
Control Autodesk desktop apps - 3ds Max and friends - from the shell via Flue, without an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and technical operators use this skill when they want an agent to inspect or make bounded, human-directed changes inside Autodesk desktop applications, currently focused on 3ds Max through Flue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to install or use Flue, a local bridge that can operate inside professional desktop applications. <br>
Mitigation: Require explicit user approval before installing or setting up Flue, and review the Flue package or source before use. <br>
Risk: Automation through Flue can modify scenes or documents in Autodesk and other desktop applications. <br>
Mitigation: Use small, inspectable, user-directed steps and avoid destructive actions unless the user explicitly requests them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sfkislev/autodesk-flue) <br>
- [Flue GitHub project](https://github.com/SFKislev/flue) <br>
- [Flue PyPI package](https://pypi.org/project/flue) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented bridge interaction guidance; the skill itself is documentation-only and does not generate files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
