## Description: <br>
Provides Feishu document operations using a user access token for authentication, including reading, creating, writing, and appending Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HackSing](https://clawhub.ai/user/HackSing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to work with Feishu documents through Feishu Open API under a user's access token, including reading, creating, appending, updating, and deleting document content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User access tokens allow an agent to read and change Feishu documents under the user's identity. <br>
Mitigation: Use the narrowest Feishu scopes that work and require explicit confirmation before document update or delete operations. <br>
Risk: Cached token data can expose Feishu document access on shared or poorly protected machines. <br>
Mitigation: Protect or remove ~/.config/claw-feishu-user/config.json when it is not needed and avoid shared machines for token storage. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Feishu Document API](https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDMzCM4ATm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus Feishu API responses and document changes when the helper scripts are used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and modify Feishu documents and may write cached token data to ~/.config/claw-feishu-user/config.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
