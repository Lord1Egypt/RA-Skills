## Description: <br>
Guides agents through creating, replacing, and validating Feishu Wiki documents by assembling complete Markdown locally, writing with full-document replacement, and reading back results to avoid ordering conflicts and duplicate documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwz119](https://clawhub.ai/user/xwz119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to create or update large Feishu Wiki or cloud-drive documents. It provides a repeatable write-and-verify workflow for complete Markdown documents, especially pages over 50 blocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Updating an existing Feishu document uses full-content replacement, which can overwrite current content if the wrong document token, account, or draft is used. <br>
Mitigation: Confirm the Feishu account or token, target document token, and intended content before writing; rely on Feishu version history or backups when replacing existing documents. <br>
Risk: A write success response may not prove that all intended content was persisted. <br>
Mitigation: Read the document back after writing and verify expected block counts and key section headings before reporting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwz119/feishu-wiki-writer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with JSON command examples and workflow checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; recommends read-back validation after writes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
