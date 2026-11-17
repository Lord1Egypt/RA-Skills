## Description:

Converts FBX 3D model files to GLB/glTF through a Node.js CLI or a deployable browser-based converter with 3D preview support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzh448](https://clawhub.ai/user/zzh448)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and 3D content creators use this skill to convert FBX assets to GLB locally or to deploy a simple web converter for upload, preview, and download workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External conversion dependencies and install paths are not fully verified by the supplied evidence.

Mitigation: Install only from a versioned release, pin dependencies or use a lockfile, and review dependency sources before using private model files.

Risk: The deployed web converter may handle confidential model files in a browser context with JavaScript and WASM assets.

Mitigation: Use the deployed page for confidential models only when Three.js and WASM assets are vendored or otherwise integrity-verified.

Risk: The CLI writes output files and can overwrite existing files when forced.

Mitigation: Review input and output paths before execution, and use overwrite flags only when replacing an existing asset is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzh448/skills/fbx-to-glb)
- [AssimpJS](https://github.com/kovacsv/assimpjs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and file-path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of converted .glb files or static web deployment files when executed by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
