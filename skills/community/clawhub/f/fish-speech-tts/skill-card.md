## Description: <br>
Fish Speech TTS helps agents create voiceover audio with voice cloning, rule-based emotion analysis, multi-segment synthesis, batch line generation, and local voice library management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taosiuman](https://clawhub.ai/user/taosiuman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media creators use this skill to generate short-drama and AI-drama voiceovers through a local Fish Speech API, including permitted reference-voice cloning, emotion-aware line synthesis, batch script processing, and reusable voice profile management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can process sensitive voice audio or create speech in a person's voice without appropriate permission. <br>
Mitigation: Use only reference voices the user is authorized to use, and delete retained reference audio when it is no longer needed. <br>
Risk: Sending text and reference audio to an untrusted API endpoint could expose private content. <br>
Mitigation: Keep the Fish Speech API on localhost when possible and avoid untrusted --api-base endpoints. <br>
Risk: Generated audio and voice profile files may remain in local output or voice_profiles directories. <br>
Mitigation: Review where outputs are written and remove stored voice profiles or audio artifacts that should not persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taosiuman/skills/fish-speech-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Analysis, Configuration instructions] <br>
**Output Format:** [CLI text, Python API calls, JSON voice-profile data, and generated audio files such as MP3, WAV, OPUS, or PCM] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable Fish Speech API, defaults to localhost, and may write output audio plus voice profile files to local directories.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
