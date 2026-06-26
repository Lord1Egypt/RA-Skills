## Description: <br>
Generates songs, soundtracks, jingles, lullabies, and other music from text prompts using the ElevenLabs Eleven Music API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdbotborges](https://clawhub.ai/user/clawdbotborges) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators, developers, and agents use this skill to generate short or long music tracks from text prompts, including instrumental pieces and tracks with AI-generated vocals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided music prompts to ElevenLabs for generation. <br>
Mitigation: Avoid sensitive or confidential prompt content and confirm that use of ElevenLabs is acceptable for the intended workflow. <br>
Risk: The skill uses a paid ElevenLabs account through ELEVENLABS_API_KEY. <br>
Mitigation: Use a dedicated or revocable API key where possible, keep it in the environment, and monitor account usage. <br>
Risk: Running the script with uv resolves and executes the listed Python dependencies. <br>
Mitigation: Run in a controlled environment and review dependency resolution before use in managed systems. <br>
Risk: The script writes the generated audio file to the selected local output path. <br>
Mitigation: Choose explicit scratch or destination paths carefully to avoid overwriting or misplacing generated audio. <br>


## Reference(s): <br>
- [ElevenLabs Pricing](https://elevenlabs.io/pricing) <br>
- [ClawHub skill page](https://clawhub.ai/clawdbotborges/elevenlabs-music) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands; script stdout returns the generated audio file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an MP3 audio file to the requested output path, or to /tmp/music.mp3 by default.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
