## Description: <br>
Creaa AI helps agents generate and edit images and generate videos through the Creaa.ai API using text-to-image, image-edit, text-to-video, and image-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yys2024](https://clawhub.ai/user/yys2024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and external agents use this skill to submit Creaa.ai media-generation tasks, poll asynchronous task status, and retrieve generated image or video results. It is intended for workflows that need command-ready API guidance for image generation, image editing, text-to-video, image-to-video, model discovery, and usage checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source images or videos, and task details are sent to the third-party Creaa.ai service. <br>
Mitigation: Avoid submitting personal, confidential, or regulated content unless Creaa.ai handling policies have been reviewed and accepted. <br>
Risk: The skill requires a Creaa API key for authenticated requests. <br>
Mitigation: Keep CREAA_API_KEY secret, do not paste it into chats, and do not commit it to repositories. <br>
Risk: Media generation and editing tasks consume Creaa API credits. <br>
Mitigation: Check available usage and pricing before submitting tasks, especially for video generation or repeated polling workflows. <br>


## Reference(s): <br>
- [Creaa.ai](https://creaa.ai) <br>
- [Creaa.ai Profile API Keys](https://creaa.ai/profile) <br>
- [Creaa.ai Pricing](https://creaa.ai/pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/yys2024/creaa-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with curl commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CREAA_API_KEY environment variable and sends prompts, image data, source media URLs, and task details to Creaa.ai.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
