## Description: <br>
Csharp Developer helps agents create C#/.NET project scaffolds, generate code, design architecture, review code, and debug implementation issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill for C#/.NET project setup, WPF, WinForms, ASP.NET Core, class library work, code generation, architecture planning, code review, and debugging support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project creation can run local shell commands from insufficiently constrained project options, .NET version values, or output paths. <br>
Mitigation: Use controlled project type and .NET version values, avoid untrusted output paths, and run without elevated privileges. <br>
Risk: Generated serial-port or hardware control code may be unsafe if used directly with real equipment. <br>
Mitigation: Review and test generated hardware-control code in a controlled environment before connecting it to real devices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/csharp-developer-jirboy) <br>
- [.NET SDK download](https://dotnet.microsoft.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with code snippets, command examples, configuration details, and structured result objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .NET project files when the create-project task is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
