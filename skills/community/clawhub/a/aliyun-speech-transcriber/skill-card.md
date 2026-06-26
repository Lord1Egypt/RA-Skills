## Description: <br>
Transcribes publicly accessible audio or video URLs into JSON transcripts and best-effort plain text using Aliyun DashScope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenggongdu](https://clawhub.ai/user/chenggongdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to submit cloud-accessible media URLs, including signed Qiniu URLs, to Aliyun DashScope and receive transcription JSON plus extracted text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted media URLs and resulting transcript data are shared with Aliyun DashScope. <br>
Mitigation: Only submit media the user intends to transcribe, and use short-lived signed URLs for private media. <br>
Risk: Credential exposure could allow unauthorized DashScope API use. <br>
Mitigation: Use a dedicated or revocable API key through environment variables and never hardcode credentials. <br>


## Reference(s): <br>
- [Aliyun DashScope](https://dashscope.aliyun.com/) <br>
- [Aliyun speech environment variables](references/env-example.md) <br>
- [ClawHub skill page](https://clawhub.ai/chenggongdu/aliyun-speech-transcriber) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Text, Shell commands, Configuration] <br>
**Output Format:** [JSON with transcript text and task metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Aliyun DashScope API key and externally accessible media URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
