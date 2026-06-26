## Description: <br>
Generate and edit images using the AceData Nano Banana API with configurable models, aspect ratios, resolutions, batch generation, and local image edit inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate images from text prompts or edit existing images through the AceData Nano Banana API. It is intended for workflows that need script-driven image generation, local or remote image inputs, and saved image outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review reports an unrelated backup routine that could copy the saved API key file outside the skill directory. <br>
Mitigation: Review or remove the backup routine before use, especially any behavior that copies `.env` or other credential files. <br>
Risk: The skill uses a bearer token for AceData and may save it in a local `.env` file. <br>
Mitigation: Use a revocable AceData API key, restrict its permissions where possible, and rotate it if it may have been exposed. <br>
Risk: Local image inputs can be uploaded to AceData CDN/API for editing, which may expose sensitive image content to external processing. <br>
Mitigation: Avoid submitting confidential images unless the user accepts AceData and CDN processing for those inputs. <br>
Risk: Generated outputs are written to a dated Desktop folder. <br>
Mitigation: Check the Desktop output folder after use and move or delete generated images according to local data handling requirements. <br>


## Reference(s): <br>
- [Nano Banana Images API Documentation](references/api_docs.md) <br>
- [AceData Cloud Platform](https://share.acedata.cloud/r/1uN88BrUTQ) <br>
- [ClawHub skill page](https://clawhub.ai/xiyunnet/ace-banana2) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, files] <br>
**Output Format:** [Markdown instructions and Python CLI output, with generated image files saved locally.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for an AceData API key when missing, can upload local images to AceData CDN/API for editing, and saves generated images to a dated Desktop folder.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
