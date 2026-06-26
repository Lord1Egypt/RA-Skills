## Description: <br>
AI voice creation skill for speech recognition, text-to-speech, and audio processing with Alibaba Cloud DashScope models, with first-run behavior that may auto-manage DashScope API keys and install the Alibaba Cloud CLI ModelStudio plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to transcribe audio, generate speech from text, and create styled voice output through Alibaba Cloud DashScope voice models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can modify the Alibaba Cloud CLI setup and create or store a real DashScope API key. <br>
Mitigation: Set `DASHSCOPE_API_KEY` manually with least-privilege permissions before use, and review whether automatic key management is acceptable for the target environment. <br>
Risk: Voice requests send audio or text to Alibaba Cloud DashScope and may incur usage charges. <br>
Mitigation: Confirm data handling requirements and expected costs before processing sensitive, regulated, or large audio and text inputs. <br>
Risk: Automatic API key management may require broad Bailian permissions if users choose the documented full-access policy. <br>
Mitigation: Prefer the documented custom RAM policy with only the required ModelStudio key-management actions when API key automation is needed. <br>


## Reference(s): <br>
- [DashScope Voice API Documentation Reference](references/api-docs.md) <br>
- [DashScope Voice Model List](references/models.md) <br>
- [DashScope Voice API Error Codes Reference](references/error-codes.md) <br>
- [RAM Policies for Bailian Voice Creator](references/ram-policies.md) <br>
- [Audio File Transcription API Documentation](https://help.aliyun.com/zh/model-studio/qwen-asr-api-reference) <br>
- [Speech Synthesis API Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-api-reference) <br>
- [Model List](https://help.aliyun.com/zh/model-studio/models) <br>
- [Get API Key](https://help.aliyun.com/zh/model-studio/get-api-key) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-bailian-voice-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration guidance, and generated Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or download audio files through DashScope service calls when used with valid credentials.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
