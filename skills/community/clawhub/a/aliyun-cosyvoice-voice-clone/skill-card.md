## Description:

Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to prepare Alibaba Cloud Model Studio CosyVoice voice-enrollment requests from public reference audio and to understand how the returned voice_id is reused in later TTS calls.

### Deployment Geography for Use:

China mainland deployment mode for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash voice cloning; other Alibaba Cloud deployment modes only where the selected target model supports voice clone/design.

## Known Risks and Mitigations:

Risk: Reference audio could be used without adequate rights or consent for voice cloning.

Mitigation: Use only audio that the operator is authorized to enroll and for which voice-cloning consent has been obtained.

Risk: Generated voice_id values are persistent resources that could enable later synthesis in the cloned voice.

Mitigation: Treat voice_id values as sensitive, limit access to them, and avoid exposing them in public logs or shared artifacts.

Risk: Real voice enrollment may create retention or deletion obligations in Alibaba Cloud Model Studio.

Mitigation: Review Alibaba Cloud retention and deletion controls before enrolling real voices.

## Reference(s):

- [CosyVoice Voice Clone API Reference](references/api_reference.md)
- [Sources](references/sources.md)
- [Alibaba Cloud Model Studio CosyVoice clone/design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api)
- [Alibaba Cloud Model Studio CosyVoice clone/design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-cosyvoice-voice-clone)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce reusable request JSON and response-validation guidance for a CosyVoice enrollment workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
