## Description: <br>
This skill helps agents guide e-commerce users through the 51aic/Aicraft service for AI image generation, video generation, image editing, detail-page creation, style replication, and asset management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howerlin0329](https://clawhub.ai/user/howerlin0329) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers and operators use this skill to prepare product images, short product videos, AI detail-page images, style-replicated product visuals, and related asset-management actions through the 51aic/Aicraft service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires users to paste a 51aic/Aicraft account token into the chat. <br>
Mitigation: Use the skill only when intending to access that service, treat the token as a credential, and avoid sharing it in public or persistent conversations. <br>
Risk: The skill can upload user images to a third-party service for generation or editing. <br>
Mitigation: Confirm that each image is appropriate to send to 51aic/Aicraft before upload and that the user has rights to use it. <br>
Risk: The skill can delete assets from the user's third-party account. <br>
Mitigation: Before deletion, require the agent to list the exact asset IDs and obtain explicit user approval. <br>
Risk: Watermark-removal workflows can be misused on images the user does not own or have permission to modify. <br>
Mitigation: Use watermark removal only for images the user owns or is authorized to edit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howerlin0329/aicraft-skill) <br>
- [51aic Aicraft platform](https://www.51aic.com?source=agents) <br>
- [OpenClaw token page](https://www.51aic.com/openclaw?source=agents) <br>
- [Image generation modes](references/image-modes.md) <br>
- [Video generation configuration](references/video-config.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON, Python, curl, and PowerShell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include third-party API request examples, thumbnail links, original asset links, task IDs, progress summaries, and deletion confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence; artifact _meta.json reports 1.0.7) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
