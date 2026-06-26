## Description: <br>
AIGC Generator helps an agent handle text-to-image requests with negative prompts, aspect ratio selection, and batch generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushenjie](https://clawhub.ai/user/gushenjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers can ask an OpenClaw agent to generate images from prompts, save the generated image files, and deliver them through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated prompts and images may be sent to external AIGC, file-service, and Feishu destinations. <br>
Mitigation: Use a dedicated AIGC API key, avoid confidential prompts or images, and confirm AIGC_BASE_URL and the Feishu destination before running the skill. <br>
Risk: The skill relies on execution instructions that should be reviewed before installation. <br>
Mitigation: Prefer package-relative script paths, structured command arguments, and explicit opt-in before Feishu or file-service uploads. <br>
Risk: The skill requires sensitive credentials through AIGC_API_KEY. <br>
Mitigation: Store credentials only in a trusted runtime, scope the key to this use case, and rotate it if generated content or logs may have exposed it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gushenjie/aigc-gen) <br>
- [AIGC Studio registration (English)](https://tczlld.com/aistudio/en/) <br>
- [AIGC Studio registration (Chinese)](https://tczlld.com/aistudio/zh/) <br>
- [AIGC API base URL](https://tczlld.com/aistudio/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON-marked generator output containing local image paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIGC_API_KEY and optional AIGC_* environment variables; generated images are saved as local files and may be uploaded to Feishu.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
