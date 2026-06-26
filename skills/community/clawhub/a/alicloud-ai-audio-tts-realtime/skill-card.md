## Description: <br>
Provides real-time speech synthesis guidance and a compatibility probe for Alibaba Cloud Model Studio Qwen TTS Realtime models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose Qwen realtime TTS models, configure DashScope credentials, and validate low-latency streaming speech synthesis on Alibaba Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud DashScope credentials and sends synthesis text to a cloud API. <br>
Mitigation: Use a dedicated API key where possible and avoid sending confidential or regulated text unless applicable Alibaba Cloud terms and policies allow it. <br>
Risk: Changing the DashScope endpoint or output path can route data or generated audio somewhere unexpected. <br>
Mitigation: Keep the default Alibaba endpoint unless an alternative is verified, and review output paths before running fallback audio generation. <br>
Risk: Some SDK or runtime combinations may reject realtime model calls. <br>
Mitigation: Run the provided probe script, using strict mode for gating workflows that require realtime compatibility. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen TTS Realtime Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-ai-audio-tts-realtime) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands; the demo script emits JSON and can write WAV audio files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses DashScope credentials and writes fallback audio under output/ai-audio-tts-realtime/audio/ when requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
