## Description: <br>
Relays Feishu group-chat messages between two configured bot instances so they can sustain a topic-focused multi-agent conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puddy3133](https://clawhub.ai/user/puddy3133) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run two Feishu bots on separate machines that continue a controlled group-chat discussion around a configured topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad group-chat phrases can control a background auto-posting daemon. <br>
Mitigation: Install only in a dedicated, approved Feishu group; prefer explicit commands, consider require_mention=true, keep round counts low while testing, and monitor or stop the daemon when done. <br>
Risk: The skill requires sensitive Feishu and OpenClaw credentials, and evidence notes that token fragments may appear in logs. <br>
Mitigation: Use least-privilege Feishu app permissions, protect the runtime config file, restrict log access, and rotate credentials if logs containing token fragments were exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puddy3133/feishu-multi-agent-replay) <br>
- [Publisher profile](https://clawhub.ai/user/puddy3133) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu messages API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local OpenClaw API and Feishu app credentials; reply length is controlled by max_reply_tokens in configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
