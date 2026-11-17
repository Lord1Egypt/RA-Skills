## Description:

Voice cloning workflows with Alibaba Cloud Model Studio Qwen TTS VC models for creating cloned voices from sample audio and synthesizing text with cloned timbre.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud Qwen TTS voice-cloning requests, validate response shape, and document evidence for reproducible audio synthesis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned SDK installation can change runtime behavior across environments.

Mitigation: Use a dedicated virtual environment and pin a reviewed dashscope SDK version before running the workflow.

Risk: API keys, enrollment audio, and generated voice_id values can expose sensitive voice-cloning capability if logged or shared.

Mitigation: Keep DASHSCOPE_API_KEY out of logs, restrict access to voice samples and voice_id values, and use only samples with consent and a retention plan.

## Reference(s):

- [Alibaba Cloud Qwen TTS Voice Cloning Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Skill Reference Sources](references/sources.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can validate response files for audio URL or base64 PCM output shape.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
