## Description:

Create reliable Excalidraw diagrams in OpenClaw using the Excalidraw MCP, with export-safe labels, Excalifont text, and clear system-diagram structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickytonline](https://clawhub.ai/user/nickytonline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical teams use Excaliclaw to create editable Excalidraw architecture diagrams, system diagrams, flowcharts, and hand-drawn style diagrams in OpenClaw. The skill emphasizes preview-first diagram generation, export-safe native Excalidraw scenes, readable labels, and preserved editability metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagram content may be shared externally through an editable excalidraw.com link.

Mitigation: Review diagram content before approving export or sharing, and only share externally when the content is acceptable.

Risk: The skill may ask to install or configure an Excalidraw MCP, which changes the local agent environment.

Mitigation: Require explicit user approval before installation or configuration, use current OpenClaw-supported setup paths, and verify MCP availability with a minimal scene before proceeding.

Risk: Exports can fail, be empty, or lose editability metadata if preview and export payloads diverge.

Mitigation: Preview the diagram first, export the same full native Excalidraw scene, preserve binding metadata, and verify the exported link is non-empty before delivering it.

## Reference(s):

- [Excaliclaw on ClawHub](https://clawhub.ai/nickytonline/skills/excaliclaw)
- [nickytonline Publisher Profile](https://clawhub.ai/user/nickytonline)
- [Excalidraw](https://excalidraw.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON scene examples, shell or configuration instructions when setup is approved, and editable Excalidraw links when export succeeds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce fallback diagram formats such as Excalidraw JSON, SVG/PNG, or Mermaid when MCP preview or export is unavailable.]

## Skill Version(s):

1.0.2 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
