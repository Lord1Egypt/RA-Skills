## Description: <br>
Feishu Speaker helps an agent transcribe Chinese voice messages locally and send generated voice replies through Feishu using TTS and Feishu APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tel18610240060-collab](https://clawhub.ai/user/tel18610240060-collab) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI assistant operators use this skill to turn Feishu voice messages into text and send synthesized voice replies through a configured Feishu app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release can upload and send audio through Feishu using a local app secret. <br>
Mitigation: Use a minimally scoped Feishu app secret and treat any audio passed to the script as data that may leave the local machine. <br>
Risk: The artifact defaults to hardcoded Feishu app and recipient identifiers. <br>
Mitigation: Replace the bundled app_id and receiver_id with explicit local configuration and require a recipient for every send. <br>
Risk: The security summary says the skill ships less functionality than it advertises. <br>
Mitigation: Verify the installed commands and scripts before relying on advertised listen, say, reply, or reply-voice workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tel18610240060-collab/feishu-speaker) <br>
- [Publisher profile](https://clawhub.ai/user/tel18610240060-collab) <br>
- [Feishu Open Platform app console](https://open.feishu.cn/app/) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell tooling that uploads audio to Feishu and requires a local app secret plus network access.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
