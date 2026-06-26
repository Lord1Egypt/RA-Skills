## Description: <br>
Bambu Studio AI helps agents search or generate 3D models, analyze and repair meshes, prepare previews and colorization, hand off to Bambu Studio, and monitor Bambu Lab printer workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyixuan2](https://clawhub.ai/user/heyixuan2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and 3D printing operators use this skill to coordinate model search or generation, printability analysis, Bambu Studio review, printer control, and print monitoring while keeping user approval in the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control physical Bambu printer hardware, including print actions and raw G-code paths. <br>
Mitigation: Require explicit user approval before printer operations, prefer manual Bambu Studio printing, and avoid raw G-code unless the user intentionally requests it. <br>
Risk: Monitoring and auto-pause workflows may use camera snapshots and background checks. <br>
Mitigation: Require opt-in before monitoring or auto-pause, show users when snapshots are captured, and treat snapshots and model files as sensitive local data. <br>
Risk: The skill may handle Bambu cloud credentials, LAN access codes, and third-party 3D generation API keys. <br>
Mitigation: Store secrets only in the documented local secret files with restrictive permissions, avoid committing generated configuration or token files, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heyixuan2/bambu-studio-ai) <br>
- [Bambu Lab Model Specifications](references/model-specs.md) <br>
- [Bambu Lab Cloud API Reference](references/bambu-cloud-api.md) <br>
- [Bambu Lab MQTT Protocol Reference](references/bambu-mqtt-protocol.md) <br>
- [AI 3D Generation API Reference](references/3d-generation-apis.md) <br>
- [AI 3D Generation Prompt Engineering Guide](references/3d-prompt-guide.md) <br>
- [Manifold3d API Reference and 3D Printing Patterns](references/manifold-examples.md) <br>
- [Colorize geometry enhancement notes](references/colorize-geometry-enhancement.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration values, and generated model or preview file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local model, preview, color map, configuration, token cache, and monitoring log files when the user authorizes those workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
