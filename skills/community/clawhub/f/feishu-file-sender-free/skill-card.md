## Description: <br>
Helps agents send files and images through Feishu or Lark using the correct two-step upload and message flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automation builders use this skill to send selected reports, archives, documents, code files, and images to Feishu or Lark users or groups. It is suited for workflows that need the agent to produce shell commands or guidance for reliable file/image delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send a selected file or image to the wrong Feishu or Lark recipient. <br>
Mitigation: Confirm the recipient identifier, destination type, and file contents before running generated commands. <br>
Risk: The artifact includes examples that pass app secrets through command arguments or chat-visible snippets. <br>
Mitigation: Use environment variables, a secret store, or another protected credential mechanism instead of pasting app_secret values into commands or conversations. <br>
Risk: Overbroad trigger language could cause the skill to be used for unrelated file-handling tasks. <br>
Mitigation: Use the skill only for explicit Feishu or Lark file and image sending workflows. <br>
Risk: Files may contain regulated, confidential, or otherwise unauthorized content. <br>
Mitigation: Avoid regulated or secret files unless the user is authorized and the destination is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-file-sender-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu or Lark recipient IDs, file paths, app credentials, upload keys, and execution status text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
