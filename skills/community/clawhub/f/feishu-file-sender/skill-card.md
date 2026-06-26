## Description: <br>
Uploads a local file through the Feishu OpenAPI and sends it as a file message from an OpenClaw agent to a target chat or user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziwenwang28](https://clawhub.ai/user/ziwenwang28) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators using OpenClaw with Feishu use this skill to return generated local files to a Feishu chat or user as downloadable attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected local files to Feishu recipients. <br>
Mitigation: Verify the file path and target chat or user ID before sending sensitive files. <br>
Risk: The skill reads Feishu app credentials from the local OpenClaw configuration. <br>
Mitigation: Keep ~/.openclaw/openclaw.json protected and limit Feishu app permissions where possible. <br>
Risk: The skill requires network access to Feishu APIs. <br>
Mitigation: Allow only the required Feishu endpoints and review API errors or logs when delivery fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ziwenwang28/feishu-file-sender) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; runtime delivery is a Feishu file message.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, network access to Feishu OpenAPI, a local file path, and OpenClaw Feishu credentials.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata, SKILL.md frontmatter, clawdis.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
