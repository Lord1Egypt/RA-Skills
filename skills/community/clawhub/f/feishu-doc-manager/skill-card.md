## Description: <br>
Publishes Markdown content to Feishu Docs with automatic formatting, table conversion, permission management, and batch writing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shuai-DaiDai](https://clawhub.ai/user/Shuai-DaiDai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and document automation users use this skill to create, write, append, update, and manage permissions for Feishu Docs from Markdown-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite, delete, append to, or otherwise modify Feishu documents. <br>
Mitigation: Require explicit confirmation for destructive or bulk document actions and verify document IDs before execution. <br>
Risk: The skill can add, remove, or update collaborators and permission levels. <br>
Mitigation: Use a Feishu app or token with minimum required scopes and confirm collaborator identities and permission levels before applying changes. <br>
Risk: The release asks users to install external code that server evidence did not link to resolved import provenance. <br>
Mitigation: Review the repository before installing and pin a trusted commit or release when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Shuai-DaiDai/feishu-doc-manager) <br>
- [Skill homepage from artifact](https://github.com/Shuai-DaiDai/feishu-doc-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and Feishu document operation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may direct an agent to create or modify Feishu document content and permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
