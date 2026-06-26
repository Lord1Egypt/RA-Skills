## Description: <br>
Use the ACE-Step API to generate music, edit songs, remix audio, create lyrics-driven songs, continue audio, and repaint audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DumoeDss](https://clawhub.ai/user/DumoeDss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and music production users use this skill to guide an agent through ACE-Step music generation, lyric-driven song creation, audio continuation, remixing, and repainting through the bundled shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, lyrics, and generated music requests may be sent to the configured API endpoint. <br>
Mitigation: Verify the configured api_url before use and avoid sending private or proprietary lyrics unless the service is trusted. <br>
Risk: API keys may be exposed if users inspect or print sensitive configuration values. <br>
Mitigation: Use the documented key-check and masked list commands, and avoid printing or reading the raw api_key value. <br>
Risk: The shell workflow depends on curl and jq, and dependency installation can modify the user's environment. <br>
Mitigation: Treat jq installation as a manual setup step that requires explicit user approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DumoeDss/acestep) <br>
- [ACE-Step API Reference](api-reference.md) <br>
- [ACE Music API key page](https://acemusic.ai/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON task results, and generated audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save JSON results and MP3/WAV/FLAC audio files to an acestep_output directory when the bundled script is executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
