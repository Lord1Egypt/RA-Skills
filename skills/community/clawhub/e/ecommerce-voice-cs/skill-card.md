## Description:

Ecommerce Voice CS helps an agent run separate after-sales customer support and telephone sales modes, producing response text and SenseAudio TTS audio files after mode-specific configuration and confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and agent hosts can use this skill to collect required service or sales configuration, confirm mode activation, generate Chinese customer-facing reply text, and create retained local TTS audio for playback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated customer-service or sales text is sent to SenseAudio for TTS generation.

Mitigation: Avoid sending sensitive customer data or confidential sales content unless SenseAudio processing is approved for that data.

Risk: API keys and session configuration may be retained in local session-state files.

Mitigation: Prefer the SENSEAUDIO_API_KEY environment variable, avoid chat-style API key entry, and clear session-state files after use.

Risk: Audio files are retained on disk at caller-provided output paths.

Mitigation: Use a controlled output directory with appropriate permissions and retention cleanup.

Risk: Sales mode may activate after a non-empty confirmation-stage reply.

Mitigation: Require explicit host-side confirmation before enabling sales mode in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaocaijic/skills/ecommerce-voice-cs)
- [SenseAudio voice API documentation](https://senseaudio.cn/docs/voice_api)
- [SenseAudio API key documentation](https://senseaudio.cn/docs/api-key)
- [SenseAudio text-to-speech API documentation](https://senseaudio.cn/docs/text_to_speech_api)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Configuration guidance]

**Output Format:** [JSON response containing generated text, audio_file path, playback object, state metadata, and optional error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates retained local MP3 audio by default, supports selected SenseAudio voice IDs, and returns null audio/playback fields during configuration-only stages.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
