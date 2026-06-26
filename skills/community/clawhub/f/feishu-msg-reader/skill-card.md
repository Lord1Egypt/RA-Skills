## Description: <br>
Fetch Feishu message content by message_id, with optional thread context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadblue22](https://clawhub.ai/user/deadblue22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve Feishu message content by message ID, inspect raw message payloads, and optionally include thread context for replies or interactive-card fallback text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Feishu messages accessible to the configured Feishu app or tenant token. <br>
Mitigation: Use least-privileged Feishu credentials and only fetch message IDs needed for the current task. <br>
Risk: Passing a tenant access token on the command line can expose the token through shell history or process listings. <br>
Mitigation: Prefer environment variables or the OpenClaw config file over the --token argument when possible. <br>
Risk: Using --thread retrieves additional conversation context beyond the target message. <br>
Mitigation: Use --thread only when surrounding replies are needed to interpret the requested message. <br>


## Reference(s): <br>
- [Feishu Open Platform APIs](https://open.feishu.cn/open-apis) <br>
- [ClawHub skill page](https://clawhub.ai/deadblue22/feishu-msg-reader) <br>
- [Publisher profile](https://clawhub.ai/user/deadblue22) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from the Feishu fetch script plus Markdown guidance and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script returns parsed message fields and can include a chronologically sorted thread array when --thread is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
