## Description: <br>
High-quality voice synthesis with 18 personas, 32 languages, sound effects, batch processing, and voice design using ElevenLabs API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and agent users use this skill to generate speech, sound effects, batch audio, and voice previews through the ElevenLabs API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text, sound prompts, and the ElevenLabs API key may be sent to ElevenLabs. <br>
Mitigation: Use a dedicated quota-limited API key, prefer environment variables over plaintext config files, and avoid sensitive content. <br>
Risk: Batch inputs or output paths can write files outside the intended output folder. <br>
Mitigation: Review batch files and output paths before running scripts, and run the skill from a dedicated working directory. <br>
Risk: Credential guidance is inconsistent across setup and runtime documentation. <br>
Mitigation: Use ELEVEN_API_KEY or ELEVENLABS_API_KEY environment variables as the preferred configuration path. <br>


## Reference(s): <br>
- [ElevenLabs Voice Guide](references/voice-guide.md) <br>
- [ElevenLabs API Documentation](https://docs.elevenlabs.io) <br>
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library) <br>
- [ElevenLabs Sound Effects API](https://elevenlabs.io/docs/api-reference/sound-generation) <br>
- [ElevenLabs Voice Design API](https://elevenlabs.io/docs/api-reference/voice-generation) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated audio files when scripts are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an ElevenLabs API key; scripts may write MP3 files and local usage/configuration files.] <br>

## Skill Version(s): <br>
2.1.6 (source: frontmatter, CHANGELOG, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
