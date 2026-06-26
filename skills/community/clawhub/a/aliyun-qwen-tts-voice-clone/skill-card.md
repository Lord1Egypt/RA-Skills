## Description: <br>
Helps agents use Alibaba Cloud Model Studio Qwen TTS voice-cloning models to create cloned voices from sample audio and synthesize text with the cloned timbre. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare Alibaba Cloud Qwen TTS voice-clone requests, validate response shape, and organize output evidence for cloned-voice audio workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice samples, generated audio URLs, request files, and voice IDs can contain sensitive biometric or personally identifiable information. <br>
Mitigation: Use only consented voice samples, keep generated files and identifiers private, and delete local outputs when they are no longer needed. <br>
Risk: Alibaba Cloud credentials are required for normal use and could be exposed if copied into artifacts or prompts. <br>
Mitigation: Use a dedicated API key through `DASHSCOPE_API_KEY` or the Alibaba Cloud credentials file and avoid committing credentials or generated evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-qwen-tts-voice-clone) <br>
- [Artifact reference list](references/sources.md) <br>
- [Alibaba Cloud Qwen TTS voice cloning documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local request JSON and response-validation summaries under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
