## Description: <br>
Use when designing custom voices with Alibaba Cloud Model Studio Qwen TTS VD models and creating custom synthetic voices from text descriptions for speech synthesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and voice product teams use this skill to prepare Alibaba Cloud Qwen TTS voice-design requests, define reusable voice prompts, and validate synthesis responses before using generated voices in speech workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses an Alibaba Cloud DashScope API key, which could be exposed through committed credential files, logs, or screenshots. <br>
Mitigation: Store the key in the environment or Alibaba Cloud credentials file, keep it out of source control and logs, and prefer least-privilege setup for voice prompt testing and synthesis requests. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen TTS Voice Design documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request or validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write normalized request JSON and local evidence files under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
