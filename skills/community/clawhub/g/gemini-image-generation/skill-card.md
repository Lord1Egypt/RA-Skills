## Description: <br>
Generates or edits images with Gemini using the Google GenAI SDK for OpenClaw workflows that create, transform, render, or save images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ztj7728](https://clawhub.ai/user/ztj7728) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate new image files from prompts or edit existing workspace images through Gemini, then return saved image paths for display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and source images may be sent to Gemini or a configured Gemini-compatible endpoint. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and keep GEMINI_BASE_URL unset unless the endpoint is trusted. <br>
Risk: GEMINI_API_KEY exposure could allow unauthorized API use. <br>
Mitigation: Provide GEMINI_API_KEY through a secret or environment mechanism and do not paste real keys into chat or committed files. <br>
Risk: Incorrect input or output paths could read unintended source images or write files in an unexpected location. <br>
Mitigation: Use explicit workspace-relative input and output paths for image generation and editing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ztj7728/gemini-image-generation) <br>
- [Publisher profile](https://clawhub.ai/user/ztj7728) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Package manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, JSON, Shell commands, Configuration] <br>
**Output Format:** [Saved image files with console TEXT and IMAGE lines plus a JSON summary of generated image paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional aspect ratio and image size settings; may save multiple image files with numbered suffixes; source prompts, model IDs, and input paths are not included in the final JSON summary.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
