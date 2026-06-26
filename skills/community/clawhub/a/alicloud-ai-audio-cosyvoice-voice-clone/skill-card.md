## Description: <br>
Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare Alibaba Cloud Model Studio CosyVoice voice-enrollment requests from authorized public reference audio and to understand how the returned voice_id is reused in later TTS calls. <br>

### Deployment Geography for Use: <br>
China mainland for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash clone workflows; model support varies for international deployment. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help create reusable cloned voices from audio URLs without proving speaker consent. <br>
Mitigation: Use only reference audio from speakers who explicitly authorized cloning, and record consent before enrollment. <br>
Risk: The Alibaba Cloud API key and returned voice_id can enable unauthorized voice operations if exposed. <br>
Mitigation: Treat DASHSCOPE_API_KEY and voice_id values as sensitive secrets, avoid committing them to repositories, and restrict access to generated outputs. <br>
Risk: Reference audio URLs and long-lived voice clones can create privacy and lifecycle-management exposure. <br>
Mitigation: Prefer time-limited sample URLs and confirm Alibaba Cloud retention and deletion options before creating durable cloned voices. <br>
Risk: Using a different synthesis model from the enrollment target_model can cause later TTS requests to fail. <br>
Mitigation: Reuse the same target_model family for enrollment and later speech synthesis. <br>


## Reference(s): <br>
- [CosyVoice Voice Clone API Reference](references/api_reference.md) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud CosyVoice Clone and Design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api) <br>
- [Alibaba Cloud CosyVoice Clone and Design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request bodies and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a request.json file when using the bundled helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
