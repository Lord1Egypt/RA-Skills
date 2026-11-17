## Description:

Generates and manages Draw.io, Mermaid, and Excalidraw diagrams from JSON specifications, including batch creation for network topology, architecture, flowchart, swimlane, UML, ER, mind map, and whiteboard diagrams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation teams, and operations teams use this skill to create, validate, export, and batch-generate structured diagrams for architecture, topology, process, data-modeling, and whiteboard workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local execution and file access can affect files beyond the intended diagram task.

Mitigation: Run the skill only for explicit diagram-generation tasks and review proposed commands, generated paths, and filesystem changes before execution.

Risk: The npx adapter package is enabled at runtime and may introduce supply-chain or execution risk.

Mitigation: Inspect and pin or otherwise approve the adapter package before enabling it in an agent environment.

Risk: Callback URLs can share diagram content or metadata with an unintended endpoint.

Mitigation: Avoid callback_url unless the endpoint is controlled, expected, and uses HTTPS.

Risk: Sensitive architecture or business diagrams may be exposed through generated files, logs, or output paths.

Mitigation: Confirm output locations before first run and review generated results for sensitive content before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/diagram-gen-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON specifications, configuration snippets, shell commands, and diagram files such as .drawio, .mmd, and .excalidraw]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution status, generated file paths, metadata, logs, and error details.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
