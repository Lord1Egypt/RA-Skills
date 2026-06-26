## Description: <br>
Generate and edit images using Nano Banana (Gemini-3-Pro-Image-Preview) API with automatic base64 encoding and decoding, image compression, and optional Discord integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonboi](https://clawhub.ai/user/jasonboi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images or edit local images through a Gemini-compatible image API while avoiding manual base64 handling. It is also useful when generated images should be saved locally or intentionally sent to a Discord channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected images, API keys, and Discord sends may expose privacy-sensitive information. <br>
Mitigation: Install only when the Banana/Gemini-compatible API endpoint is trusted for the prompts and images being provided. <br>
Risk: Passing an API key on the command line may expose credentials through shell history or process inspection. <br>
Mitigation: Prefer the BANANA_API_KEY environment variable or a protected config file for API key storage. <br>
Risk: Using --channel-id sends the generated image and caption to a Discord channel. <br>
Mitigation: Use --channel-id only when the target Discord channel is intentional and appropriate for the content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jasonboi/banana-api) <br>
- [Banana API endpoint](https://nn.147ai.com) <br>
- [Publisher profile](https://clawhub.ai/user/jasonboi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper saves generated image files locally and can optionally send them to a Discord channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
