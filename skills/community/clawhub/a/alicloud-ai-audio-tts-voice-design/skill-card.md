## Description: <br>
Voice design workflows with Alibaba Cloud Model Studio Qwen TTS VD models. Use when creating custom synthetic voices from text descriptions and using them for speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design custom synthetic voices from text descriptions with Alibaba Cloud Model Studio Qwen TTS voice-design models and prepare normalized request or validation artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses an Alibaba/DashScope API key and installs the provider SDK. <br>
Mitigation: Install the SDK in an isolated environment and use a scoped Alibaba/DashScope API key. <br>
Risk: Voice prompts and synthesis text may contain confidential content that is sent to the provider or stored in local output files. <br>
Mitigation: Avoid confidential text in prompts unless provider processing and local storage are acceptable for the use case. <br>


## Reference(s): <br>
- [Qwen TTS Voice Design Documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [ClawHub Skill Page](https://clawhub.ai/cinience/alicloud-ai-audio-tts-voice-design) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/cinience) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request or response artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local request JSON and response validation summaries under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
