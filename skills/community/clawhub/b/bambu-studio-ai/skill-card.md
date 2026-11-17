## Description:

Bambu Studio Ai helps agents automate Bambu Lab 3D printing workflows including model search or generation, printability analysis, colorization, preview, Bambu Studio handoff, printer control, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyixuan2](https://clawhub.ai/user/heyixuan2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D-printing users use this skill to guide an agent through Bambu Lab model selection or generation, model repair and preview, Bambu Studio handoff, and optional printer status, print, and monitoring actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a real Bambu Lab printer and use printer credentials.

Mitigation: Use manual print mode by default, keep credentials local and access-limited, and require explicit confirmation before any print or printer-control action.

Risk: Raw G-code and automatic pause or monitoring features can affect printer behavior during a physical print.

Mitigation: Avoid raw G-code unless the command is understood, and enable auto-pause or background monitoring only after an explicit user opt-in.

Risk: Image-to-3D and model-generation workflows may fetch untrusted image URLs or generated assets.

Mitigation: Use trusted inputs where possible, review generated models in preview and Bambu Studio before printing, and isolate the runtime environment with pinned dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heyixuan2/skills/bambu-studio-ai)
- [AI 3D Generation API Reference](references/3d-generation-apis.md)
- [AI 3D Generation Prompt Engineering Guide](references/3d-prompt-guide.md)
- [Bambu Lab Cloud API Reference](references/bambu-cloud-api.md)
- [Bambu Lab MQTT Protocol Reference](references/bambu-mqtt-protocol.md)
- [Colorize Geometry Enhancement](references/colorize-geometry-enhancement.md)
- [Manifold3d API Reference and 3D Printing Patterns](references/manifold-examples.md)
- [Bambu Lab Model Specifications](references/model-specs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated or modified local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce printer-control commands, 3D model files, previews, configuration updates, and monitoring guidance when the user opts in.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
