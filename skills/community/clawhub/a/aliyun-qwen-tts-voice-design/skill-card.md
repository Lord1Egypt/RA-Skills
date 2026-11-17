## Description:

Use when designing custom voices with Alibaba Cloud Model Studio Qwen TTS VD models from text descriptions and using them for speech synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to prepare Alibaba Cloud Qwen TTS voice-design requests, create reusable synthetic voice prompts, and validate response shapes before using generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Alibaba/DashScope credentials for TTS operations.

Mitigation: Expose only the credentials needed for the voice-design task and use a clean virtual environment.

Risk: Generated voice output may be unsuitable or inconsistent for reuse without review.

Mitigation: Validate generated voices with short utterances and review output before reuse.

Risk: The helper setup installs the dashscope package without a pinned version.

Mitigation: Pin the dashscope dependency in controlled environments to improve supply-chain hygiene.

## Reference(s):

- [Alibaba Cloud Qwen TTS Voice Design Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-qwen-tts-voice-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce normalized voice-design request JSON and response validation summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
