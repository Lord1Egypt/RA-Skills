## Description: <br>
MiniMax multimodal generation toolkit for voice, music, image, image-to-image, and video generation via MiniMax APIs using cross-platform Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuan-huicheng](https://clawhub.ai/user/yuan-huicheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate and save MiniMax TTS, music, images, image-to-image outputs, and videos from prompts or media references, with optional Feishu delivery instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media are sent to MiniMax and may contain sensitive images, voices, audio, or video references. <br>
Mitigation: Use only approved, non-confidential inputs and obtain permission before uploading another person's face or voice. <br>
Risk: The optional MiniMax API host override can send requests through a non-default endpoint. <br>
Mitigation: Use the default MiniMax host unless the alternate host is trusted and approved. <br>
Risk: Generated media may be prepared for Feishu delivery after creation. <br>
Mitigation: Review generated files and destination chat IDs before sending content through Feishu. <br>


## Reference(s): <br>
- [Ali Minimax Toolkit on ClawHub](https://clawhub.ai/yuan-huicheng/ali-minimax-toolkit) <br>
- [MiniMax Image Generation API](https://platform.minimaxi.com/docs/api-reference/image-generation-t2i) <br>
- [MiniMax Image-to-Image API](https://platform.minimaxi.com/docs/api-reference/image-generation-i2i) <br>
- [MiniMax Music Generation API](https://platform.minimaxi.com/docs/api-reference/music-generation) <br>
- [MiniMax TTS Guide](references/tts-guide.md) <br>
- [MiniMax Video Generation API Documentation](references/video-api.md) <br>
- [MiniMax Video Prompt Writing Guide](references/video-prompt-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is saved under minimax-output/ by convention.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
