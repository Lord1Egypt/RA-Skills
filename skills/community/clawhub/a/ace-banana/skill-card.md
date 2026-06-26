## Description: <br>
Generate and edit images using the AceData Nano Banana API. Supports models like nano-banana-2, custom aspect ratios (default 16:9), and resolutions (default 2K). Handles batch generation and image-to-image (edit) tasks with local files. Use when the user wants to generate or edit high-quality images via Nano Banana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiyunnet](https://clawhub.ai/user/xiyunnet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate new images from prompts or edit existing images through the AceData Nano Banana API, with support for batch requests, model selection, aspect ratio, and resolution settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to AceData for generation or editing. <br>
Mitigation: Avoid using sensitive prompts or images unless the user is comfortable sharing them with AceData. <br>
Risk: The skill can store the AceData API token in a local .env file for reuse. <br>
Mitigation: Keep the .env file private and rotate or delete the API key if the skill directory is shared, backed up, or committed. <br>


## Reference(s): <br>
- [Nano Banana Images API Documentation](references/api_docs.md) <br>
- [AceData Cloud Platform](https://platform.acedata.cloud) <br>
- [AceData Nano Banana API Endpoint](https://api.acedata.cloud/nano-banana/images) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiyunnet/ace-banana) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; script output includes JSON responses and locally saved image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated or edited images are saved locally to a dated Desktop folder when the API request succeeds.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
