## Description: <br>
AgentVibes adds offline text-to-speech controls for Claude Code and OpenClaw, including voice switching, personality styles, speed and effects, background music, language learning, and platform-specific TTS providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulpreibisch](https://clawhub.ai/user/paulpreibisch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using Claude Code or OpenClaw use this skill to manage local text-to-speech voices, playback style, speed, effects, background music, replay, and language-learning narration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local audio caching and cleanup actions can affect sensitive session audio or local files. <br>
Mitigation: Review cache behavior before use, run cleanup after sensitive sessions, and inspect separately installed command implementations before allowing update or cleanup actions to run automatically. <br>
Risk: Voice assets may be downloaded from external sources. <br>
Mitigation: Be comfortable with voice asset downloads before installing and use trusted network and storage settings for downloaded voices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paulpreibisch/agentvibes-openclaw-skill) <br>
- [Piper voices on Hugging Face](https://huggingface.co/rhasspy/piper-voices) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline slash commands and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for local TTS configuration and playback behavior.] <br>

## Skill Version(s): <br>
4.6.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
