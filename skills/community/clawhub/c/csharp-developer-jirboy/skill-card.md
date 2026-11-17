## Description:

Csharp Developer helps agents provide C#/.NET project templates, code generation, architecture design, and code review, with this release kept as a compatibility layer for a unified code entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold C#/.NET projects, generate C# code patterns, review code, and outline application architecture for desktop, web API, class library, and industrial-control-style workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The project creation path can turn user-controlled .NET version or output directory values into local shell execution.

Mitigation: Review before installing, use the project-creation feature only with trusted arguments, and avoid untrusted .NET version or output directory values until command execution is changed to safe argument-based execution with input validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/csharp-developer-jirboy)
- [.NET download](https://dotnet.microsoft.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown or text responses with C# code blocks, shell commands, configuration snippets, and generated project files when project creation is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal responses are agent-readable development guidance; project creation requires local .NET SDK availability and may write files to the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
