## Description: <br>
Generates images from text prompts with ERNIE-Image and ERNIE-Image-Turbo models via AMD Radeon Cloud, with configurable size, batch count, seed, inference steps, guidance scale, and prompt enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiwork4me](https://clawhub.ai/user/aiwork4me) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn explicit text-to-image requests into locally saved PNG image files, with optional JSON output for automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters are sent to an external image-generation service, and the default endpoint uses HTTP. <br>
Mitigation: Use only non-sensitive prompts with the default endpoint; for confidential or business prompts, configure a trusted HTTPS endpoint. <br>
Risk: Generated files are written to a local output directory. <br>
Mitigation: Review or explicitly set the output directory before generation, especially in shared or automated environments. <br>
Risk: Custom HTTPS endpoints may receive AI_STUDIO_API_KEY when configured. <br>
Mitigation: Set ERNIE_BASE_URL and AI_STUDIO_API_KEY only for trusted HTTPS endpoints. <br>


## Reference(s): <br>
- [ERNIE-Image API Reference](references/api-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aiwork4me/ernie-image-radeon) <br>
- [Upstream ClawHub Skill](https://clawhub.ai/aiwork4me/ernie-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, configuration, guidance] <br>
**Output Format:** [PNG image files with MEDIA lines, optional JSON status, and markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports one to four generated images per run and avoids overwriting existing output files.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
