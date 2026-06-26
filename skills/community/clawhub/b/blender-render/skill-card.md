## Description: <br>
Automate Blender headless previews for STL/OBJ/FBX/BIM and multi-part 3D-print models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzyling](https://clawhub.ai/user/lzyling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and engineers use this skill to produce local preview images from 3D model assets for review, handoff, and troubleshooting. It is suited for headless Blender workflows that need orthographic Workbench views, optional contact sheets, or simple Cycles renders rather than geometry validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Blender/Python scripts against user-selected 3D model files. <br>
Mitigation: Use a trusted Blender installation, run commands in a fresh headless Blender session, and only process model files from trusted locations. <br>
Risk: Preview renders can be mistaken for model validation. <br>
Mitigation: Treat generated images as visual previews only; use a dedicated validation workflow for watertightness, printability, clearance, 3MF validity, or assembly fit. <br>
Risk: Optional contact sheets require Pillow, which may need to be installed separately. <br>
Mitigation: Install Pillow only from trusted package sources and skip contact-sheet generation when the dependency is not available or not approved. <br>
Risk: Cycles GPU rendering can depend on host GPU and Blender device configuration. <br>
Mitigation: Use Workbench or CPU rendering for portable smoke tests, and use GPU rendering only when the host render devices are known to be configured. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lzyling/blender-render) <br>
- [Publisher profile](https://clawhub.ai/user/lzyling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local script parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scripts produce PNG render files and optional contact sheets when run with Blender and, for contact sheets, Pillow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
