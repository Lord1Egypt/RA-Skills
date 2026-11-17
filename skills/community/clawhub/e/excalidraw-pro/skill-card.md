## Description:

Generate Excalidraw diagrams (.excalidraw files) from natural language descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jannik689](https://clawhub.ai/user/jannik689)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and other external users use this skill to turn natural language requests into Excalidraw flowcharts, architecture diagrams, mind maps, and sequence diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite local diagram files in the current workspace.

Mitigation: Use explicit output filenames and review paths before running it in a sensitive directory.

Risk: Generated diagrams may be incomplete or misleading if the natural language request or intermediate JSON omits important relationships.

Mitigation: Review the intermediate JSON and resulting diagram before relying on it for decisions or documentation.

## Reference(s):

- [Excalidraw](https://excalidraw.com)
- [ClawHub skill page](https://clawhub.ai/jannik689/skills/excalidraw-pro)
- [Publisher profile](https://clawhub.ai/user/jannik689)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON input examples and generated .excalidraw files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates diagram_input.json and writes a local .excalidraw JSON file for opening in Excalidraw.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
