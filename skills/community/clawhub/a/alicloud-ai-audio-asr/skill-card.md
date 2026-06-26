## Description: <br>
Transcribes recorded audio with Alibaba Cloud Model Studio Qwen ASR models for transcript generation, timestamped outputs, and DashScope/OpenAI-compatible ASR request documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe recorded audio with Alibaba Cloud DashScope Qwen ASR, choose sync or async workflows, and save normalized transcript outputs and raw API responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio is sent to Alibaba Cloud DashScope for transcription. <br>
Mitigation: Use the skill only when authorized to process the chosen audio with Alibaba Cloud, and avoid highly sensitive recordings unless compliance requirements allow it. <br>
Risk: Saved transcript and raw-response files may contain private content. <br>
Mitigation: Protect, minimize, or delete saved transcript and raw-response files according to the data sensitivity and retention requirements. <br>
Risk: The helper script requires a DashScope API key. <br>
Mitigation: Use a scoped API key and keep credentials in environment variables or the supported credentials file rather than embedding them in prompts or output files. <br>


## Reference(s): <br>
- [Qwen ASR API Notes (Non-Realtime)](references/api_reference.md) <br>
- [Official Alibaba Cloud Qwen ASR Sources](references/sources.md) <br>
- [Recorded Speech Recognition - Qwen](https://help.aliyun.com/zh/model-studio/recorded-speech-recognition-qwen) <br>
- [Qwen ASR OpenAI-Compatible API](https://help.aliyun.com/zh/model-studio/qwen-asr) <br>
- [Qwen ASR File Transcription API](https://help.aliyun.com/zh/model-studio/qwen-asr-filetrans-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples plus normalized JSON transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include transcript text, optional task IDs, status, and raw DashScope API responses saved under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
