## Description:

Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud CosyVoice voice enrollment requests from a voice prompt, preview text, target model, and output settings before using the returned voice_id for text-to-speech.

### Deployment Geography for Use:

China mainland for cosyvoice-v3.5 voice design; other regions depend on Alibaba Cloud Model Studio endpoint and target-model support.

## Known Risks and Mitigations:

Risk: Voice prompts and preview text may be sent to Alibaba Cloud and may also be saved locally in generated request files.

Mitigation: Do not include confidential, regulated, personal, or unauthorized voice-related content unless that handling is acceptable for the Alibaba Cloud account and local environment.

Risk: Using an unsupported endpoint or mismatched target_model can produce failed enrollments or unusable voices.

Mitigation: Choose the Alibaba Cloud endpoint and target model supported for the deployment region, and match the target_model to the later speech synthesis model.

Risk: Invalid request fields can cause API errors or incorrect preview behavior.

Mitigation: Validate that prefix is letters or digits only and no more than 10 characters, voice_prompt and preview_text stay within documented limits, and language_hints match the preview_text language.

## Reference(s):

- [CosyVoice Voice Design API Reference](references/api_reference.md)
- [Sources](references/sources.md)
- [Alibaba Cloud CosyVoice clone and design API documentation (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api)
- [Alibaba Cloud CosyVoice clone and design API documentation (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-audio-cosyvoice-voice-design)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies and optional bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local request JSON files under the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
