## Description: <br>
Anygen Diagram helps agents generate and manage diagrams for technical and business documentation using AnyGen CLI commands, API calls, templates, and batch workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and enterprise teams use this skill to create diagrams, standardize diagram templates, batch-generate visual assets, and integrate diagram generation into documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagram descriptions or source document excerpts may be sent to AnyGen's external service. <br>
Mitigation: Redact sensitive business, customer, and architecture details before use when policy requires it. <br>
Risk: The skill includes commands that configure API keys and run CLI or API workflows. <br>
Mitigation: Use scoped API keys, store secrets outside shared files, and review generated commands before running them. <br>
Risk: Generated diagram assets may be written to project folders and reused in documentation workflows. <br>
Mitigation: Write outputs to project-specific directories and review generated diagrams before publishing or sharing them. <br>


## Reference(s): <br>
- [AnyGen Diagrams API](https://api.anygen.io/v1/diagrams) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/anygen-diagram) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, Python, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of PNG, SVG, PDF, and Markdown diagram assets through an external AnyGen service.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
