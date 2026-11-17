## Description:

Feishu Cli Board helps agents create and manage Feishu whiteboards, including precise node layouts, Mermaid or PlantUML imports, image export, and node retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giswilson](https://clawhub.ai/user/giswilson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace users use this skill to generate architecture diagrams, flowcharts, kanban-style boards, and other visualizations inside Feishu documents using feishu-cli whiteboard commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggers may route ordinary drawing or visualization requests to Feishu whiteboard operations that change remote documents.

Mitigation: Install only when that routing is desired, and confirm the target document or whiteboard before running creation commands.

Risk: Feishu credentials with broad workspace access could allow unintended document or whiteboard changes.

Mitigation: Use a narrowly scoped Feishu app and avoid broad workspace credentials for casual visualization tasks.

## Reference(s):

- [Feishu Cli Board on ClawHub](https://clawhub.ai/giswilson/skills/feishu-cli-board)
- [Whiteboard node API reference](references/node-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Feishu whiteboard node JSON and commands that create or modify remote whiteboards; review target documents and generated payloads before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
