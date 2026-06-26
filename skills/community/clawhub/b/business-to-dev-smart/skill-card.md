## Description: <br>
Smart business-to-dev requirement translator that analyzes a project codebase, understands business requirements, references actual code, and generates implementation-ready developer documentation for any technology stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wumaohua233](https://clawhub.ai/user/wumaohua233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn business feature requests, optional UI screenshots, and project context into executable development requirement documents. It helps identify relevant existing code, propose interface and data model changes, and break implementation work into developer tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the project path provided by the user and can save a local project summary containing architecture or business details. <br>
Mitigation: Review .ai-memory/project-profile.md for sensitive details, add .ai-memory/ to .gitignore when appropriate, and delete or refresh the file before sharing the repository or after major code changes. <br>
Risk: Generated implementation guidance and code references may be incomplete or may not fully match the target codebase. <br>
Mitigation: Have developers review the generated requirements, interface designs, data models, and task breakdown against the actual code before implementation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wumaohua233/business-to-dev-smart) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact examples](artifact/EXAMPLE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, interface tables, implementation steps, and task checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local .ai-memory/project-profile.md file in the scoped project path to preserve project structure and architecture context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
