## Description:

Voice design workflows with Alibaba Cloud Model Studio Qwen TTS VD models. Use when creating custom synthetic voices from text descriptions and using them for speech synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud Qwen TTS voice-design requests, create reusable voice prompts, and validate generated voice responses before longer speech synthesis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed or floating SDK dependencies may change behavior over time.

Mitigation: Install the skill in a virtual environment and use a pinned, reviewed dashscope package version.

Risk: Alibaba Cloud credentials could be exposed if shared in prompts, logs, or saved evidence.

Mitigation: Provide credentials only when API calls are intended and keep DASHSCOPE_API_KEY out of saved artifacts and transcripts.

Risk: Synthetic voice output may be unsuitable or misleading if generated from vague prompts.

Mitigation: Use explicit tone, pace, emotion, and timbre constraints, then validate short utterances before longer scripts.

## Reference(s):

- [Alibaba Cloud Qwen TTS Voice Design documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-audio-tts-voice-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON request or response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write normalized request JSON and validation output under the configured output directory.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
