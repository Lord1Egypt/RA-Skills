## Description:

Generates hand-drawn Excalidraw-style diagrams from prompts, using a local Docker canvas service to create, export, save, and optionally insert PNG/SVG diagrams into Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenyangze](https://clawhub.ai/user/zhenyangze)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and product teams use this skill to create architecture diagrams, flowcharts, ER diagrams, topology diagrams, and other Excalidraw-style visuals from natural-language prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start or use a local Docker canvas service and run browser-based export JavaScript.

Mitigation: Run it only in an environment where local Docker and browser automation are acceptable, and review the commands before execution.

Risk: The skill can move generated image files and update Markdown where requested.

Mitigation: Provide exact output paths and review proposed file edits before applying them.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/zhenyangze/Excalidraw-Handdraw-Skill)
- [ClawHub skill page](https://clawhub.ai/zhenyangze/skills/excalidraw-handdraw-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell commands, plus generated PNG/SVG diagram files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update Markdown files with image references when the user requests insertion or replacement.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
