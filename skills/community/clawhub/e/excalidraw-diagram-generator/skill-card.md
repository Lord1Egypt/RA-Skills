## Description:

Generates editable Excalidraw diagrams as .excalidraw JSON files from natural-language requests for flowcharts, relationship diagrams, mind maps, architecture diagrams, and related diagram types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elihuvillaraus](https://clawhub.ai/user/elihuvillaraus)

### License/Terms of Use:


## Use Case:

External users, developers, and teams use this skill to turn descriptions of processes, systems, data flows, object models, or relationships into editable Excalidraw diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated diagrams may contain inaccurate relationships, crowded layouts, or overlapping elements.

Mitigation: Review the .excalidraw file before sharing or relying on it, keep diagrams focused, and split complex requests into smaller diagrams.

Risk: Optional icon-library workflows may require downloading .excalidrawlib files and running local setup or helper commands.

Mitigation: Review downloaded library sources and command paths before running setup, and use basic shapes when icon libraries are not installed or trusted.

Risk: The inspected package references helper scripts for icon handling that are not included in the artifact.

Mitigation: Confirm helper scripts exist in the installed skill before following script-based icon instructions.

## Reference(s):

- [Excalidraw JSON Schema Reference](references/excalidraw-schema.md)
- [Excalidraw Element Types Guide](references/element-types.md)
- [Excalidraw](https://excalidraw.com)
- [Excalidraw Libraries](https://libraries.excalidraw.com/)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [.excalidraw JSON files with concise Markdown summaries, opening instructions, and optional shell command snippets for icon-library setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated diagrams should keep element counts manageable, use unique element IDs, avoid overlapping elements, and use Excalifont for text elements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
