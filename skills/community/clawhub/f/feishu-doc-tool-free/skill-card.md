## Description: <br>
Helps agents read and edit Feishu documents, Wikis, and Bitable content, including document creation, writing, appending, and block-level operations for personal daily use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent retrieve Feishu document content, create new documents, append long Markdown content, and perform block-level edits through Feishu/Lark workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Feishu App ID and App Secret credentials. <br>
Mitigation: Use least-privilege Feishu app credentials and avoid exposing App Secret values in prompts, logs, or shared outputs. <br>
Risk: The skill can create, update, append, or modify live Feishu documents. <br>
Mitigation: Require explicit user confirmation before write, append, block-level, or delete-style operations on live documents. <br>
Risk: The skill accepts optional callback URLs for asynchronous notifications. <br>
Mitigation: Use only trusted callback URLs and review network destinations before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/feishu-doc-tool-free) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code examples and JSON-style operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce document tokens, status fields, execution logs, and Feishu configuration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
