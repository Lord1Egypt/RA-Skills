## Description: <br>
Control Adobe desktop apps - Photoshop, Illustrator, Premiere, After Effects, InDesign, Audition - from the shell via Flue, without an MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sfkislev](https://clawhub.ai/user/sfkislev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to let an agent inspect and make bounded, user-directed edits inside supported Adobe desktop applications through Flue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables desktop automation through an external Flue bridge that can change files open in supported Adobe applications. <br>
Mitigation: Install and use it only for requested Adobe-app tasks, review the Flue package before setup, and keep actions bounded and inspectable. <br>
Risk: Setup requires installing an external package. <br>
Mitigation: Do not install or configure Flue unless the user explicitly approves setup in the current session. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sfkislev/adobe-flue) <br>
- [Flue project](https://github.com/SFKislev/flue) <br>
- [Flue package on PyPI](https://pypi.org/project/flue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and app scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bridge commands can return structured JSON when Flue is installed and used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
