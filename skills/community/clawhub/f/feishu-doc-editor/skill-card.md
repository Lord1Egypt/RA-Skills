## Description: <br>
Feishu document creation and editing operations using OpenAPI. Activate when user needs to create, edit, or read Feishu documents programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuligu](https://clawhub.ai/user/zhuligu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure Feishu app permissions and make authorized OpenAPI calls that create, read, update, or delete Feishu document content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through Feishu document edits and deletes that can change authorized documents. <br>
Mitigation: Confirm the target document and operation before making edits or deletions, and test on non-production documents first. <br>
Risk: The skill requires Feishu app credentials and tenant access tokens. <br>
Mitigation: Use a dedicated Feishu app with minimum permissions, keep secrets out of chats, logs, shell history, and repositories, and rotate or revoke tokens when finished. <br>
Risk: Broad app or document permissions can expose documents beyond the intended task. <br>
Mitigation: Add the app only to documents the user is authorized to access, grant the narrowest usable permissions, and remove collaborator access when work is complete. <br>


## Reference(s): <br>
- [Feishu OpenAPI Detailed Guide](references/api-guide.md) <br>
- [Feishu Document Permission Setup Guide](references/permission-setup.md) <br>
- [Feishu Document API Common Errors](references/common-errors.md) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [ClawHub release page](https://clawhub.ai/zhuligu/feishu-doc-editor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu OpenAPI request examples and permission troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
