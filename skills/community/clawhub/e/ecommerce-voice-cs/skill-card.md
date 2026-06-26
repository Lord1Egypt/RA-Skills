## Description: <br>
E-commerce voice customer-service skill for OpenClaw-style hosts that can run independent after-sales support and sales-call modes, generate text replies or scripts, and create SenseAudio TTS audio files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaocaijic](https://clawhub.ai/user/xiaocaijic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add voice-enabled e-commerce support workflows to an agent host. It collects mode-specific configuration, produces after-sales responses or sales scripts, calls SenseAudio TTS, and returns text plus local audio playback metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive session or configuration data may be retained locally in bundled or runtime .session_state files. <br>
Mitigation: Remove bundled session-state files before release and store runtime state in a host-managed location with appropriate retention and access controls. <br>
Risk: The skill can write generated audio files to caller-provided paths and asks the host to retain them. <br>
Mitigation: Restrict audio_output_path to a dedicated writable directory and avoid sharing paths that expose unrelated local files. <br>
Risk: Playback metadata requests immediate local audio playback. <br>
Mitigation: Gate or disable autoplay on shared machines and require host-side confirmation where unexpected audio playback is a concern. <br>
Risk: SenseAudio API keys are required for TTS calls. <br>
Mitigation: Provide keys through a host secret store or SENSEAUDIO_API_KEY environment variable rather than persisting them in session state or payload logs. <br>
Risk: The default child voice may be inappropriate for some commercial sales or support contexts. <br>
Mitigation: Use a neutral adult voice unless there is a documented product or compliance reason for the default voice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaocaijic/ecommerce-voice-cs) <br>
- [SenseAudio voice API documentation](https://senseaudio.cn/docs/voice_api) <br>
- [SenseAudio API key documentation](https://senseaudio.cn/docs/api-key) <br>
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, API Calls, Configuration instructions] <br>
**Output Format:** [JSON responses with text, optional audio_file path, playback metadata, and local MP3 or WAV audio files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses session_id for stateful mode setup, SENSEAUDIO_API_KEY or api_key for TTS, and audio_output_path for retained local audio files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
