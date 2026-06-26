## Description: <br>
AI image editing and beautification suite for portrait retouching, body reshaping, AI hair styling, clothes and cosplay changes, expression edits, photo restoration, upscaling, and artistic filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beautypluscom](https://clawhub.ai/user/beautypluscom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to submit still images to BeautyPlus for portrait retouching, body reshape effects, hair and outfit changes, expression edits, restoration, upscaling, and delivery back through supported chat platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are sent to BeautyPlus for paid external processing, and delivery can send results to chat platforms such as Feishu or Telegram. <br>
Mitigation: Use the skill only when the user is comfortable with those services processing the media, verify recipients before delivery, and avoid highly sensitive photos unless provider terms are acceptable. <br>
Risk: The skill requires sensitive BeautyPlus credentials and may use optional chat-platform tokens for delivery. <br>
Mitigation: Use scoped API keys where possible and pass credentials through environment variables rather than command-line arguments or chat text. <br>
Risk: Local task history and cache files can retain task records after processing. <br>
Mitigation: Clear the documented history and cache directories when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beautypluscom/beautyplus-ai) <br>
- [BeautyPlus Developers](https://beautyplus.com/developers/console) <br>
- [BeautyPlus product overview](https://beautyplus.com/) <br>
- [Full agent workflow](SKILL.md) <br>
- [Credential setup prompts](docs/credentials-prompt.md) <br>
- [Polling, timeouts, and failure codes](docs/errors-and-polling.md) <br>
- [IM attachments and resolve-input](docs/im-attachments.md) <br>
- [Multi-platform delivery](docs/multi-platform.md) <br>
- [Reserved video flow](docs/video-reserved.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI results for image job status, result URLs, and delivery steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces still-image processing instructions and result URLs; video processing is reserved in the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
