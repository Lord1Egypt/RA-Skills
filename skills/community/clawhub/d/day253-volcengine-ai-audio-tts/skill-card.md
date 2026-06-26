## Description: <br>
Generates text-to-speech audio with Volcengine (ByteDance) speech services using the online one-shot HTTP API, with support for voice selection, language options, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[day253](https://clawhub.ai/user/day253) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to synthesize narration or multilingual speech through Volcengine TTS, configure voice and audio parameters, and save generated audio plus response metadata locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthesis text is sent to Volcengine/ByteDance for processing. <br>
Mitigation: Use the skill only for text that is acceptable to send to that provider, and avoid submitting sensitive or restricted content unless approved for the deployment. <br>
Risk: Volcengine credentials can be exposed if tokens are placed in request JSON, shared outputs, logs, or version control. <br>
Mitigation: Store credentials in environment variables or a private .env file, keep .env out of version control, and avoid writing secrets into request files or output directories. <br>
Risk: Unpinned Python dependencies can make installs less reproducible. <br>
Mitigation: Pin the requests package version in deployment environments that require repeatable builds. <br>


## Reference(s): <br>
- [Volcengine TTS API Reference](references/api_reference.md) <br>
- [Source Links](references/sources.md) <br>
- [Volcengine Online Speech Synthesis API](https://www.volcengine.com/docs/6561/79820) <br>
- [Volcengine TTS Parameter Basics](https://www.volcengine.com/docs/6561/79823) <br>
- [Volcengine Speaker Parameter List](https://www.volcengine.com/docs/6561/79824) <br>
- [Volcengine Console FAQ](https://www.volcengine.com/docs/6561/196768) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, Python script usage, and generated local audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include audio output, request payloads, response metadata, and validation logs under output/volcengine-ai-audio-tts/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
