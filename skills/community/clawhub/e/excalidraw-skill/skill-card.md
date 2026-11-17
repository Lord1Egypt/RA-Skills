## Description:

Generates .excalidraw diagram files for diagrams, flowcharts, architecture charts, and visualizations, then exports them to PNG or SVG via Kroki or excalidraw-brute-export-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to create clean Excalidraw diagrams for systems, processes, decisions, comparisons, and architecture explanations, including cases where relationships are clearer visually than in prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the public Kroki export path can send full diagram contents to an external service.

Mitigation: Use the local CLI or a local Kroki Docker endpoint for confidential diagrams, and avoid placing secrets, credentials, or sensitive architecture details in diagrams sent to the public Kroki service.

Risk: The local setup path recommends globally installing unpinned npm tooling.

Mitigation: Prefer pinned project-local npm dependencies and review installed package versions before using the local export workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/excalidraw-skill)
- [Excalidraw Skill Homepage](https://github.com/Agents365-ai/excalidraw-skill)
- [Kroki](https://kroki.io)
- [Kroki Excalidraw SVG API](https://kroki.io/excalidraw/svg)
- [Excalidraw Schema Reference](references/schema-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Excalidraw JSON, shell commands, and generated .excalidraw, PNG, or SVG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [SVG export can use Kroki; PNG export requires the local excalidraw-brute-export-cli and Firefox setup. PDF is not supported.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
