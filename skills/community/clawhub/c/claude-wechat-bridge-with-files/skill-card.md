## Description: <br>
Helps an agent configure OpenClaw or Claude Code to receive WeChat messages and media through ClawBot, reply through the bridge, and optionally send proactive text messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinadu-ai](https://clawhub.ai/user/tinadu-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal automation users use this skill to connect a dedicated WeChat ClawBot account to OpenClaw or Claude Code, pass inbound text and media into the agent, and send progress updates back to WeChat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose WeChat conversations and attachments to the local agent workflow and connected services. <br>
Mitigation: Use a dedicated WeChat account, avoid sending secrets or sensitive files, and review the content before allowing the agent to process it. <br>
Risk: The proactive sender reuses stored WeChat credentials and can send outbound messages without a built-in per-message approval step. <br>
Mitigation: Review wsend.js before use, protect the local credential directory, and enable proactive sending only when that behavior is intentional. <br>
Risk: The media patch downloads inbound images, files, voice, and video to local storage. <br>
Mitigation: Treat the media directory as sensitive local data, limit access to the machine, and remove retained media when it is no longer needed. <br>
Risk: The bridge depends on a third-party npm package and development-channel loading. <br>
Mitigation: Pin the npm package version, review updates before installing them, and stop the bridge process when the session is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinadu-ai/claude-wechat-bridge-with-files) <br>
- [claude-wechat-channel npm package](https://www.npmjs.com/package/claude-wechat-channel) <br>
- [WeChat ClawBot overview](https://cloud.tencent.com/developer/article/2644003) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, and JavaScript/Bash helper files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional local scripts for patching media handling and sending proactive WeChat text messages.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
