## Description: <br>
Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI audio practitioners use this skill to prepare normalized Alibaba Cloud Model Studio CosyVoice voice design requests from a voice prompt, preview text, target model, and output settings before submitting them to the provider API. <br>

### Deployment Geography for Use: <br>
China mainland for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash voice design; international use depends on the selected endpoint and supported CosyVoice model. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud/DashScope credentials and may send voice prompts or preview text to the provider API. <br>
Mitigation: Treat DASHSCOPE_API_KEY and credentials files as sensitive, and avoid using private, regulated, or proprietary text unless provider handling is acceptable. <br>
Risk: Generated request artifacts can contain voice_prompt, preview_text, target_model, and prefix values in local output files. <br>
Mitigation: Review local output artifacts before sharing, committing, or retaining them. <br>


## Reference(s): <br>
- [CosyVoice Voice Design API Reference](references/api_reference.md) <br>
- [Alibaba Cloud Model Studio CosyVoice Clone and Design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api) <br>
- [Alibaba Cloud Model Studio CosyVoice Clone and Design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-ai-audio-cosyvoice-voice-design) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON request bodies and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write normalized request JSON under output/alicloud-ai-audio-cosyvoice-voice-design/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
