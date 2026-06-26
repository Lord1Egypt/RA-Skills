## Description: <br>
Analyzes local or remote videos with the Doubao 2.0 model when the agent has a video path or URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielcy](https://clawhub.ai/user/danielcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ask targeted questions about a local video file or remote video URL and receive Doubao model analysis through Volcengine Ark. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Videos or remote video URLs are sent to Volcengine Ark for AI processing. <br>
Mitigation: Use only videos you are authorized to share and avoid sensitive, private, copyrighted, or confidential content unless approved. <br>
Risk: The skill requires an ARK_API_KEY and may incur provider cost or quota usage. <br>
Mitigation: Use a dedicated key where possible, keep it out of prompts and logs, and monitor provider costs and quota. <br>
Risk: The remote-video fallback can download large or untrusted videos into the workspace. <br>
Mitigation: Avoid the fallback for large, sensitive, private, copyrighted, or untrusted videos unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielcy/doubao-video-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/danielcy) <br>
- [Volcengine Ark service endpoint](https://ark.cn-beijing.volces.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Text response from the Volcengine Ark API, typically consumed as Markdown or plain text by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a prompt and either a local video path or a remote video URL; requires ARK_API_KEY and Python.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
