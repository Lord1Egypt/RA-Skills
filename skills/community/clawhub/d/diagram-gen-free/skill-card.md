## Description:

Generates and edits Draw.io, Mermaid, and Excalidraw diagram files from natural-language intent for network topology, architecture, flowchart, swimlane, UML, and whiteboard use cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and documentation teams use this skill to turn diagram requests into structured specifications and generated diagram files for architecture reviews, network planning, process documentation, repository docs, and whiteboard collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external connector package invoked through npx.

Mitigation: Verify the connector package source and version before installation or execution.

Risk: The connector can create or overwrite files in the workspace.

Mitigation: Restrict output paths to a dedicated diagrams directory and review target filenames before generation.

Risk: Generated diagrams may be incorrect if the requested structure or JSON specification is incomplete.

Mitigation: Review the diagram specification and generated file for schema validity, correct relationships, and readable layout before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-gen-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON diagram specifications and generated diagram file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Draw.io, Mermaid, or Excalidraw artifacts through the configured connector service.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
