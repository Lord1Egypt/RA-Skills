## Description: <br>
Agentvibes Voice Skill helps agents generate and manage text-to-speech playback across Piper TTS, macOS Say, Windows SAPI, and Soprano with voice selection, preview, speed, effects, background music, and language-learning modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, content creators, and language learners use this skill to configure agent voice output, preview and switch voices, apply speech effects, and generate spoken playback for agent interaction or media workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's offline/no-account claims conflict with API key and network requirements. <br>
Mitigation: Confirm the selected provider, voice-download path, and API-backed behavior before use, and avoid sensitive text until the data path is understood. <br>
Risk: Voice downloads, translation, cloud, or provider modes may involve network access. <br>
Mitigation: Use the skill only in environments where network access for voice downloads and provider-backed features is acceptable. <br>
Risk: Generated audio and replay behavior may leave cached content on disk. <br>
Mitigation: Review cache locations and cleanup behavior before processing private or sensitive text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agentvibes-voice-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Audio] <br>
**Output Format:** [Agent command guidance with JSON status results and generated audio playback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Voice downloads and provider-backed features may require network access; replay behavior uses a recent-audio cache.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
