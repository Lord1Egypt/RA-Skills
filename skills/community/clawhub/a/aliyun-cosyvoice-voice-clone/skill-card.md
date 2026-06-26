## Description: <br>
Use when creating cloned voices with Alibaba Cloud Model Studio CosyVoice customization models, especially cosyvoice-v3.5-plus or cosyvoice-v3.5-flash, from reference audio and then reusing the returned voice_id in later TTS calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this skill to prepare Alibaba Cloud Model Studio CosyVoice voice enrollment requests from consented reference audio and to understand how the returned voice_id is reused in later TTS synthesis. <br>

### Deployment Geography for Use: <br>
Global for general guidance; China mainland deployment mode is required for cosyvoice-v3.5-plus and cosyvoice-v3.5-flash voice clone/design, with international endpoint limitations for some target models. <br>

## Known Risks and Mitigations: <br>
Risk: Reference audio, public sample URLs, and returned voice IDs can expose sensitive voice-cloning material. <br>
Mitigation: Use reference audio only with clear speaker consent and legal rights, and avoid retaining sample URLs or voice IDs longer than needed. <br>
Risk: Calling Alibaba Cloud CosyVoice requires DashScope credentials and may be subject to provider retention, jurisdiction, and quota terms. <br>
Mitigation: Protect DASHSCOPE_API_KEY or configured DashScope credentials, review Alibaba Cloud terms before use, and avoid frequent enrollment calls that create unnecessary custom voices. <br>


## Reference(s): <br>
- [CosyVoice Voice Clone API Reference](references/api_reference.md) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud CosyVoice Clone and Design API (Chinese)](https://www.alibabacloud.com/help/zh/model-studio/cosyvoice-clone-design-api) <br>
- [Alibaba Cloud CosyVoice Clone and Design API (English)](https://www.alibabacloud.com/help/en/model-studio/cosyvoice-clone-design-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON request examples and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a request JSON file via the helper script; API calls require DashScope credentials and a public audio URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
