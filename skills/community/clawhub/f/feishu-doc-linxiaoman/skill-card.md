## Description: <br>
Creates, reads, appends, overwrites, updates, and deletes Feishu document content through a connected Feishu document tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noir-hedgehog](https://clawhub.ai/user/noir-hedgehog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and their operators use this skill to create and maintain Feishu documents, including reading content, appending Markdown, overwriting documents, and managing individual document blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write, update_block, and delete_block actions can change or remove content in important or shared Feishu documents. <br>
Mitigation: Confirm the document token, block ID, target account, and availability of version history or backups before using document-changing actions. <br>
Risk: Creating a document with large initial content can result in an empty document. <br>
Mitigation: Create an empty document first, then append Markdown content in follow-up actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noir-hedgehog/feishu-doc-linxiaoman) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Feishu document action guidance using doc_token, content, title, folder_token, and block_id parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
