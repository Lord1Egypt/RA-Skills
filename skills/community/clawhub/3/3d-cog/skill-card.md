## Description: <br>
AI 3D model generation powered by CellCog for text-to-3D, image-to-3D, game assets, product visualization, characters, props, environments, and batch generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitishgargiitd](https://clawhub.ai/user/nitishgargiitd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to ask an agent to create GLB 3D models from text descriptions, reference images, sketches, product photos, or batch item lists for games, AR/VR, e-commerce, 3D printing, education, and training. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, images, sketches, product photos, or design inputs to CellCog as an external service. <br>
Mitigation: Avoid sending confidential designs, regulated data, private images, or third-party content unless you have permission and the service terms meet your requirements. <br>
Risk: The skill requires CELLCOG_API_KEY, which could expose account access if copied into logs, commits, or shared transcripts. <br>
Mitigation: Store the API key in the agent environment or secret manager and keep it out of source files, chat transcripts, and command output. <br>
Risk: Generated GLB assets may need review for geometry quality, material fidelity, platform performance, and rights suitability before use. <br>
Mitigation: Inspect and test generated models in the target engine or 3D tool, and confirm asset rights and content suitability before publishing or manufacturing. <br>


## Reference(s): <br>
- [CellCog](https://cellcog.ai) <br>
- [ClawHub 3d Cog release](https://clawhub.ai/nitishgargiitd/3d-cog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with Python examples, setup commands, and generated GLB files from the CellCog service.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and CELLCOG_API_KEY; generated 3D assets should be reviewed in the target toolchain before production use.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
