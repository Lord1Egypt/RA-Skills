## Description:

Feishu document creation and editing operations using OpenAPI. Activate when user needs to create, edit, or read Feishu documents programmatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuligu](https://clawhub.ai/user/zhuligu)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to create, read, update, and troubleshoot Feishu documents through Feishu OpenAPI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through Feishu document read/write access with persistent app permissions.

Mitigation: Grant only the required Feishu scopes, limit app coverage and document collaboration to intended users and documents, and revoke access when the work is complete.

Risk: Token and app-secret examples may lead users to expose credentials in shared terminals, shell history, scripts, or verbose curl logs.

Mitigation: Use secret storage or environment variables, avoid printing Authorization headers or app secrets, and rotate credentials if they may have been exposed.

Risk: Write, update, or delete API calls can modify the wrong Feishu document or block when IDs are copied incorrectly.

Mitigation: Confirm document IDs, block IDs, permissions, and target documents before edits or deletes, and test first on non-production documents.

## Reference(s):

- [Feishu OpenAPI Detailed Guide](references/api-guide.md)
- [Feishu Document Permission Setup Guide](references/permission-setup.md)
- [Feishu Document API Common Errors Guide](references/common-errors.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [ClawHub skill page](https://clawhub.ai/zhuligu/skills/feishu-doc-editor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Feishu OpenAPI setup steps, permission guidance, document operation examples, and troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
