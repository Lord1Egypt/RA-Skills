## Description: <br>
Use when transcribing non-realtime speech with Alibaba Cloud Model Studio Qwen ASR models (`qwen3-asr-flash`, `qwen-audio-asr`, `qwen3-asr-flash-filetrans`). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to transcribe recorded audio through Alibaba Cloud DashScope Qwen ASR, including short synchronous requests and long-file asynchronous jobs with normalized transcript output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected recordings or audio URLs are sent to Alibaba Cloud DashScope for transcription. <br>
Mitigation: Use the skill only with audio that is approved for processing by DashScope and confirm account, region, and data-handling requirements before running transcription. <br>
Risk: Generated transcripts and raw API responses may contain sensitive audio-derived content and are saved locally. <br>
Mitigation: Store outputs in an approved location, limit retention, and handle transcript and raw-response files according to the sensitivity of the source audio. <br>
Risk: DashScope credentials are required for API calls. <br>
Mitigation: Use a dedicated DashScope API key, confirm the active Alibaba Cloud profile, and avoid exposing credentials in logs or shared output files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/aliyun-qwen-asr) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [Qwen ASR API Notes](references/api_reference.md) <br>
- [Official Aliyun Qwen ASR sources](references/sources.md) <br>
- [Recorded speech recognition - Qwen](https://help.aliyun.com/zh/model-studio/recorded-speech-recognition-qwen) <br>
- [Qwen ASR API reference](https://help.aliyun.com/zh/model-studio/qwen-asr) <br>
- [Qwen ASR file transcription API reference](https://help.aliyun.com/zh/model-studio/qwen-asr-filetrans-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON transcription outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized transcript text, task status, optional task IDs, and raw DashScope responses saved under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
