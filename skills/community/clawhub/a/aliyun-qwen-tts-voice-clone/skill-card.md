## Description:

Use when cloning voices with Alibaba Cloud Model Studio Qwen TTS VC models and synthesizing text with cloned timbre.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud Qwen TTS voice-cloning requests, validate response shape, and document safe operation for sample-based voice synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can be misused if enrollment audio is provided without permission.

Mitigation: Use the skill only with voice samples the user is authorized to clone and review consent requirements before generating audio.

Risk: The DashScope API key and saved request files may expose credentials, text, or voice-sample references.

Mitigation: Keep the API key narrowly scoped, store it outside committed files, and review generated output files before sharing or retention.

Risk: Unpinned SDK installation can introduce dependency drift.

Mitigation: Install the SDK in an isolated environment and prefer pinned dependency versions for repeatable operation.

## Reference(s):

- [Alibaba Cloud Model Studio Qwen TTS Voice Cloning](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-tts-voice-clone)
- [sources.md](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write normalized request JSON and validation evidence under the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
