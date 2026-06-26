## Description: <br>
Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models for creating cloned voices from sample audio and synthesizing text with cloned timbre. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Alibaba Cloud Model Studio Qwen TTS voice-cloning requests, validate response shape, and preserve reproducible evidence for voice synthesis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, voice IDs, saved request files, sample URLs, and API responses may contain sensitive voice or identity information. <br>
Mitigation: Use least-privilege DashScope credentials, store generated files only where needed, and protect or delete sensitive artifacts when they are no longer required. <br>
Risk: Voice cloning can be misused when the speaker has not authorized enrollment or synthesis. <br>
Mitigation: Use the skill only when there is clear authorization from the speaker and review consent and policy requirements before uploading voice recordings. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen TTS voice cloning documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Skill reference sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default generated request output is under output/ai-audio-tts-voice-clone/ unless overridden.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
