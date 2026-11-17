## Description:

Diagram生成器 helps agents turn natural-language diagram requests into Draw.io, Mermaid, or Excalidraw diagram specifications and files for topology, architecture, process, swimlane, UML, and whiteboard use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, documentation teams, and workflow automation users use this skill to create or edit structured diagrams from natural-language intent. It is suited for architecture documentation, network topology planning, process diagrams, UML diagrams, and whiteboard-style diagram drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external diagram connector.

Mitigation: Review the connector package and configuration before installation and use it only when diagram generation through that connector is intended.

Risk: The skill can write diagram files and may replace existing files when directed to an existing path.

Mitigation: Direct output to known diagram paths and use new filenames unless replacement is intentional.

Risk: API keys or connector credentials could be exposed if stored in project files.

Mitigation: Keep API keys out of repository files and configure secrets through the agent or environment secret mechanism.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-gen)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON diagram specifications, connector calls, shell configuration snippets, and generated diagram file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or overwrite Draw.io, Mermaid, or Excalidraw files through an external diagram connector.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
