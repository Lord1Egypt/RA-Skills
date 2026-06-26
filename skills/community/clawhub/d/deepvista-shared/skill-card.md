## Description: <br>
DeepVista CLI: Authentication, global flags, and security conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this shared reference to work with the DeepVista CLI, including authentication, global flags, command syntax, output formats, and security conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The on-load update check may run a command and make a network request without explicit user awareness. <br>
Mitigation: Review the skill before installation and require user approval or disable automatic update checks in environments where background commands or network calls are not acceptable. <br>


## Reference(s): <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>
- [ClawHub skill page](https://clawhub.ai/jingconan/deepvista-shared) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI usage guidance, authentication commands, exit-code references, and safety conventions.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
