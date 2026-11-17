## Description:

Text-to-speech generation on Volcengine (ByteDance) speech services for narration, multi-language speech output, voice selection, and TTS troubleshooting through the online one-shot HTTP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[day253](https://clawhub.ai/user/day253)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to synthesize speech from text with Volcengine voices, configure voice and audio parameters, and save generated audio plus response metadata for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends synthesized text and Volcengine app credentials to Volcengine's online TTS service.

Mitigation: Use only approved text, use a dedicated Volcengine token, and rotate or revoke credentials if they are exposed.

Risk: Request files, saved payloads, logs, or response metadata may contain sensitive text or credentials.

Mitigation: Keep credentials in environment variables rather than shared request files, avoid logging secrets, and delete saved outputs that contain sensitive content.

Risk: The script depends on the external Volcengine API, valid voice and cluster settings, and the Python requests package.

Mitigation: Use a virtual environment with pinned dependencies, run a minimal credential and voice check before full synthesis, and reduce request rate when rate-limited.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/day253/skills/day253-volcengine-ai-audio-tts)
- [Volcengine TTS API Reference](references/api_reference.md)
- [Source list](references/sources.md)
- [Online Speech Synthesis API](https://www.volcengine.com/docs/6561/79820)
- [Parameter Basics](https://www.volcengine.com/docs/6561/79823)
- [Speaker Parameter List](https://www.volcengine.com/docs/6561/79824)
- [Console FAQ for appid, cluster, and token](https://www.volcengine.com/docs/6561/196768)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline bash commands, JSON request examples, local audio files, and optional normalized JSON response metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio output is saved locally under output/volcengine-ai-audio-tts/audio/ by default; output location can be overridden with --output or OUTPUT_DIR.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
