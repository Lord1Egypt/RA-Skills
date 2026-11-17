## Description:

Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content or audio teams use this skill to prepare and validate Alibaba Cloud DashScope CosyVoice voice design requests from a voice prompt, preview text, target model, and output settings before using the returned voice_id in TTS.

### Deployment Geography for Use:

Global, subject to Alibaba Cloud DashScope regional endpoint and model availability.

## Known Risks and Mitigations:

Risk: DASHSCOPE_API_KEY exposure in code, logs, or evidence files.

Mitigation: Keep the API key in environment variables or Alibaba Cloud credentials and exclude it from saved outputs, logs, and shared evidence.

Risk: Voice prompts, preview text, request JSON, and response summaries may contain sensitive project data.

Mitigation: Store generated files in controlled output paths and review or redact them before sharing.

Risk: Unsupported endpoint and model pairings can make voice design requests fail.

Mitigation: Match target_model to the deployment region and later TTS model; use China mainland deployment for cosyvoice-v3.5 design models as documented by the skill.

## Reference(s):

- [CosyVoice Voice Design API Reference](references/api_reference.md)
- [Sources](references/sources.md)
- [Alibaba Cloud CosyVoice Clone and Design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api)
- [Alibaba Cloud CosyVoice Clone and Design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api)
- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-cosyvoice-voice-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request bodies and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can prepare a request JSON file under output/aliyun-cosyvoice-voice-design; API keys, voice prompts, preview text, requests, and response summaries should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
