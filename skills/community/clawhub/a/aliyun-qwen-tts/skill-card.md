## Description: <br>
Generates human-like speech audio with Model Studio DashScope Qwen TTS models and documents request and response fields for text-to-speech workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to synthesize speech with DashScope Qwen TTS models for short-form video, news, voice line generation, and TTS integration documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for synthesis is sent to Alibaba Cloud DashScope, and generated audio or request artifacts may be stored locally. <br>
Mitigation: Use approved input text, keep outputs in a private directory, and configure DASHSCOPE_API_KEY through secure environment or credential storage. <br>
Risk: The helper script can use a caller-supplied service URL and downloads the returned audio URL. <br>
Mitigation: Restrict or remove arbitrary base_url overrides, validate returned HTTPS hosts against expected DashScope or Alibaba domains, and add download time and size limits before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-qwen-tts) <br>
- [DashScope SDK Reference (Qwen TTS)](references/api_reference.md) <br>
- [Source list](references/sources.md) <br>
- [DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1) <br>
- [DashScope international API endpoint](https://dashscope-intl.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; the helper script can write WAV audio files and JSON response metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is saved under an output directory; non-streaming audio URLs are temporary, and streaming output is Base64 PCM at 24 kHz.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
