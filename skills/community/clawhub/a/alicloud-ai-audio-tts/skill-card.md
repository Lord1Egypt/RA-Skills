## Description: <br>
Generate human-like speech audio with Model Studio DashScope Qwen TTS models (qwen3-tts-flash, qwen3-tts-instruct-flash). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to convert text into speech with Alibaba Cloud DashScope Qwen TTS models, including voice lines for short drama or news videos. It also helps document request and response fields for DashScope text-to-speech workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Request JSON can include a base_url value, which may send DashScope API credentials to a non-official endpoint. <br>
Mitigation: Use only official DashScope endpoints and do not pass untrusted request JSON containing base_url. <br>
Risk: The helper downloads an audio URL returned by the service without independent URL validation. <br>
Mitigation: Only process responses from official DashScope endpoints, keep outputs in controlled directories, and review generated files before sharing them. <br>
Risk: Text prompts and generated audio may contain sensitive information handled by an external cloud service. <br>
Mitigation: Avoid sending or storing sensitive text or audio unless your Alibaba Cloud data-handling requirements allow it. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/cinience/alicloud-ai-audio-tts) <br>
- [Publisher Profile](https://clawhub.ai/user/cinience) <br>
- [DashScope SDK Reference](references/api_reference.md) <br>
- [Source List](references/sources.md) <br>
- [DashScope Beijing API Endpoint](https://dashscope.aliyuncs.com/api/v1) <br>
- [DashScope International API Endpoint](https://dashscope-intl.aliyuncs.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples plus optional generated audio files and JSON response metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated audio is saved under output/alicloud-ai-audio-tts/audio/ by default, or under OUTPUT_DIR when configured.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
