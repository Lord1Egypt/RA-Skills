## Description: <br>
End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Matttgx](https://clawhub.ai/user/Matttgx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate short videos from text prompts, turn image sequences into video, and add voice-over narration using configured AI providers and FFmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, narration, images, or media may be sent to configured external AI providers. <br>
Mitigation: Avoid submitting confidential or proprietary content unless the provider terms and project policy permit it. <br>
Risk: API keys and paid provider usage can expose credentials or create unexpected costs. <br>
Mitigation: Keep keys in a private .env file, use project-scoped keys, and set provider spending limits. <br>
Risk: Unpinned dependencies can change behavior or introduce vulnerable packages over time. <br>
Mitigation: Install in a virtual environment and pin or lock dependency versions before production use. <br>
Risk: FFmpeg commands can overwrite existing output files. <br>
Mitigation: Review output paths before running scripts and preserve important media files separately. <br>


## Reference(s): <br>
- [OpenAI API Keys](https://platform.openai.com/api-keys) <br>
- [OpenAI Platform](https://platform.openai.com) <br>
- [LumaAI](https://lumalabs.ai) <br>
- [Runway](https://runwayml.com) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [Replicate](https://replicate.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated media files such as MP4, PNG, and MP3 when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured provider API keys for provider-backed generation and FFmpeg for media processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
