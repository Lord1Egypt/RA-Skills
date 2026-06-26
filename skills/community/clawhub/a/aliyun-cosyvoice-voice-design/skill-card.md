## Description: <br>
Use when designing custom voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from a voice prompt plus preview text before using the returned voice_id in TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare and validate Alibaba Cloud Model Studio CosyVoice voice-design requests from voice prompts and preview text before reusing the returned voice_id for text-to-speech. <br>

### Deployment Geography for Use: <br>
China mainland deployment mode using the Beijing endpoint for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash; international endpoint compatibility is limited for voice clone/design. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud Model Studio credentials and may rely on DASHSCOPE_API_KEY or ~/.alibabacloud/credentials. <br>
Mitigation: Keep credentials private, avoid committing credential files or environment values, and install only when Alibaba Cloud Model Studio CosyVoice access is intended. <br>
Risk: Generated evidence files can include voice prompts, preview text, target models, prefixes, or API response summaries that may be sensitive. <br>
Mitigation: Review generated output before sharing or committing it, and delete or redact sensitive evidence files when they are no longer needed. <br>


## Reference(s): <br>
- [CosyVoice Voice Design API Reference](artifact/references/api_reference.md) <br>
- [Sources](artifact/references/sources.md) <br>
- [Alibaba Cloud CosyVoice clone/design API documentation (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api) <br>
- [Alibaba Cloud CosyVoice clone/design API documentation (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with request JSON and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write normalized request JSON under output/aliyun-cosyvoice-voice-design/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
