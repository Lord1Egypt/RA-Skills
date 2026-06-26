## Description: <br>
Guides an agent through creating, reading, writing, clearing, and deleting Feishu documents and document blocks with Feishu Open Platform APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu workspace operators use this skill to guide agents through document creation, content reads, appends, replacement workflows, block deletion, and Wiki-token resolution. It is suited for workflows where an authenticated agent needs to manage Feishu document content under user direction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents authenticated Feishu document write authority. <br>
Mitigation: Install and use it only where the agent is permitted to act on Feishu documents, and grant the Feishu app the minimum document access needed for the task. <br>
Risk: The examples include clearing or overwriting document content. <br>
Mitigation: Before destructive operations, require the agent to restate the document ID, summarize what will be deleted or replaced, and obtain explicit confirmation. <br>
Risk: A wrong document ID or Wiki token could direct changes to the wrong document. <br>
Mitigation: Resolve Wiki tokens to the target document ID, show the target link or identifier to the user, and prefer append or targeted updates unless full replacement is intentional. <br>


## Reference(s): <br>
- [Feishu Document API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document) <br>
- [Feishu Batch Delete Blocks API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/children/batch_delete) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command snippets and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Feishu app credentials, tenant access token, document identifiers, and review before executing destructive document operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
