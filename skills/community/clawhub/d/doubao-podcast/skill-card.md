## Description: <br>
Guides agents through integrating Doubao/ByteDance Podcast TTS, including WebSocket binary frames, streaming audio handling, browser proxy architecture, caching, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mileszhang001-boom](https://clawhub.ai/user/mileszhang001-boom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate Doubao/ByteDance podcast text-to-speech into applications, generate podcast audio from article URLs or short text, and troubleshoot streaming, timeout, credential, and metadata issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic podcast TTS requests may trigger this Doubao-specific skill when another provider is intended. <br>
Mitigation: Confirm that the task is for Doubao or ByteDance podcast TTS before applying provider-specific protocol and API guidance. <br>
Risk: Article URLs and text sent to the API may be processed by a third-party service. <br>
Mitigation: Do not send private articles, internal URLs, or confidential text unless third-party processing by ByteDance is approved. <br>
Risk: API credentials can be exposed if copied into client-side code or committed files. <br>
Mitigation: Keep credentials in environment variables or a secrets manager and route browser integrations through a server-side proxy. <br>
Risk: The helper script performs network calls and writes generated MP3 files. <br>
Mitigation: Review the script before execution and run it only in an environment where Doubao API access and local audio output are expected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mileszhang001-boom/doubao-podcast) <br>
- [Volcengine Console](https://console.volcengine.com/) <br>
- [Agent Skills](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline code snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Python or Node.js implementation guidance for WebSocket frames, API credentials, audio handling, and caching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
