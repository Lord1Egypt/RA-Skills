## Description:

Feishu document operations (User Access Token version). Use user access token for authentication. When you need to read, create, write, or append Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to authenticate with Feishu as a user and read, create, append, update, or delete Feishu document content through the Feishu Open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles persistent Feishu user credentials and cached refresh tokens, which can expose documents accessible under the user's identity.

Mitigation: Grant only the Feishu OAuth scopes needed for the task, avoid passing app secrets on the command line, and protect or remove the cached token file after use.

Risk: Document update and delete operations can modify or remove Feishu content when a document ID or block ID is wrong.

Mitigation: Manually confirm document IDs and block IDs before mutation, and test write operations on non-sensitive documents first.

Risk: The security verdict is Review because document mutation is available with weak scoping and safeguards.

Mitigation: Review the skill and its requested Feishu permissions before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hacksing/skills/feishu-user)
- [ClawHub publisher profile](https://clawhub.ai/user/hacksing)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu Document API](https://open.feishu.cn/document/ukTMukTMukTM/uADOwUjLwgDMzCM4ATm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Feishu document operation guidance and helper code that may call Feishu APIs when used by an agent.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
