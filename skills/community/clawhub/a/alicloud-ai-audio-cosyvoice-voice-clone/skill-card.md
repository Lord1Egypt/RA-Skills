## Description:

Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare CosyVoice voice-clone enrollment requests from public reference audio and to understand how the returned voice_id is reused in later text-to-speech calls.

### Deployment Geography for Use:

China mainland deployment mode for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash voice cloning; other regions only where Alibaba Cloud Model Studio documents compatible CosyVoice clone support.

## Known Risks and Mitigations:

Risk: Voice cloning can affect speaker identity and consent rights.

Mitigation: Use only reference audio for which the user has rights and explicit consent from the speaker.

Risk: Reference audio URLs, API responses, and voice_id values can expose sensitive voice-clone assets.

Mitigation: Limit access to these values, avoid publishing them in logs or shared artifacts, and store them only where required.

Risk: Custom voices may persist after enrollment.

Mitigation: Confirm the Alibaba Cloud deletion and retention process before enrolling production voices and delete unused custom voices promptly.

## Reference(s):

- [CosyVoice Voice Clone API Reference](references/api_reference.md)
- [Sources](references/sources.md)
- [Alibaba Cloud Model Studio CosyVoice Clone and Design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api)
- [Alibaba Cloud Model Studio CosyVoice Clone and Design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with JSON request bodies and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include target_model, prefix, public voice sample URL, language_hints, optional preprocessing fields, and guidance for handling the returned voice_id.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
