## Description:

Generates ecommerce/game/teaching 3D assets via Blender scripts (Blender 4.2+ including 5.x), with cloud Windows and local execution paths plus reference-image guided fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamasite](https://clawhub.ai/user/yamasite)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and technical content creators use this skill to generate reproducible Blender asset projects for ecommerce, game, or teaching scenarios, including specs, scripts, run instructions, exports, preview renders, and QA notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe export paths in spec.json could write generated files outside the project folder.

Mitigation: Review spec.json before execution and allow only export_glb, export_fbx_optional, and export_usdc_optional values under exports/ with no absolute paths or parent-directory components.

Risk: Generated Blender scripts and exports run against local project files.

Mitigation: Run the project in a dedicated workspace and inspect generated files before executing Blender.

Risk: Windows and cloud runner commands are described, but the evidence shows shipped macOS scripts while referenced Windows/cloud runner files are missing.

Mitigation: Confirm required runner scripts exist for the intended runtime, or use the documented Blender command pattern to create equivalent Windows/cloud commands before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yamasite/skills/blender-asset-generator)
- [Workflow](references/workflow.md)
- [Ecommerce reference-image guided template](references/ecommerce-reference-guided-template.md)
- [Degradation strategy](references/degradation-strategy.md)
- [QA checklist](references/qa-checklist.md)
- [Presets](references/presets.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON specs, Blender Python scripts, shell commands, file trees, QA results, and artifact expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a runnable Blender project package with GLB export required, optional FBX/USDC exports, preview renders, and a run log.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
