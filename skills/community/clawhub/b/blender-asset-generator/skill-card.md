## Description: <br>
Generates ecommerce/game/teaching 3D assets via Blender scripts (Blender 4.2+ including 5.x). Supports cloud Windows and local machines; reference-image guided workflow with graceful degradation when vision is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yamasite](https://clawhub.ai/user/yamasite) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical artists, and ecommerce or game teams use this skill to generate reproducible Blender asset projects from text descriptions or reference-image-assisted specifications. It produces structured specs, Blender Python scripts, run instructions, exports, preview renders, and QA guidance for 3D asset delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local Blender Python scripts can modify files or the active Blender scene. <br>
Mitigation: Use a fresh copied project folder, review generated scripts and specs before execution, and avoid running them against an important open Blender scene. <br>
Risk: The package advertises Windows and cloud runner scripts, but the security evidence notes that those scripts appear to be missing. <br>
Mitigation: Confirm or create the Windows/cloud runner scripts before using those runtimes, or use the included macOS scripts where appropriate. <br>
Risk: Reference-image dimensions may be uncertain when no scale anchor or multimodal vision is available. <br>
Mitigation: Require at least one confirmed anchor dimension, mark unconfirmed values as low confidence, and keep open questions in the generated spec. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Ecommerce Reference-Image Guided Template](references/ecommerce-reference-guided-template.md) <br>
- [Degradation Strategy](references/degradation-strategy.md) <br>
- [QA Checklist](references/qa-checklist.md) <br>
- [Presets](references/presets.md) <br>
- [Output Template](assets/output-template.md) <br>
- [Project Skeleton README](assets/project-skeleton/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown response with project package details, spec.json content, Blender Python scripts, run commands, expected artifacts, and QA evaluation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets Blender 4.2+ including 5.x; GLB export is required, FBX and USDC are optional, and preview renders plus run logs are expected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
