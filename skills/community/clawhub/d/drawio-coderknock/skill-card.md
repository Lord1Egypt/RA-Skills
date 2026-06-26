## Description: <br>
Generates local Draw.io architecture and flowchart files from preset templates, including e-commerce and CEX exchange architecture diagrams, and can open them in a local Draw.io installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coder-knock](https://clawhub.ai/user/coder-knock) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and architects use this skill to generate editable Draw.io diagrams for system architecture and common process flows. It is useful for quickly creating local diagram artifacts that can be opened, reviewed, and exported in Draw.io. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local diagram files and may open the local Draw.io application. <br>
Mitigation: Use a workspace intended for generated diagrams and review generated files before sharing or committing them. <br>
Risk: Opening diagrams depends on the Draw.io executable found on the local machine. <br>
Mitigation: Confirm that the Draw.io executable on PATH or in the system install location is legitimate before enabling automatic opening. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coder-knock/drawio-coderknock) <br>
- [Draw.io desktop releases](https://github.com/jgraph/drawio-desktop/releases) <br>
- [diagrams.net online editor](https://app.diagrams.net/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python commands and generated .drawio or .mmd files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are written to the selected workspace and may be opened in the local Draw.io application when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
