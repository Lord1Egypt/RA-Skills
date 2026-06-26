## Description: <br>
Splits long content into Feishu document blocks, creates an empty document, appends each block, and verifies the result to avoid blank Feishu documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icesumer-lgtm](https://clawhub.ai/user/icesumer-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create Feishu documents from long answers, markdown, or Mermaid-heavy content while preserving document structure. It is intended for workflows that need controlled block-by-block writes, optional destination-folder selection, and post-create verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic triggers can create or append remote Feishu documents with limited explicit consent. <br>
Mitigation: Disable or narrow automatic triggering and require user confirmation before every Feishu write. <br>
Risk: The release evidence warns that expected scripts should be verified before use. <br>
Mitigation: Verify the missing scripts from a trusted source before installation or execution. <br>
Risk: Document content may include secrets, personal data, or regulated information that would be uploaded to a Feishu workspace. <br>
Mitigation: Use only approved Feishu workspaces and accounts for sensitive data, and avoid sending restricted content unless the workspace is cleared for that data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/icesumer-lgtm/feishu-doc-block-writer) <br>
- [Quick Reference](artifact/QUICK-REFERENCE.md) <br>
- [Test Report](artifact/TEST-REPORT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON-style execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends remote Feishu documents and can return document links, document tokens, block counts, content length, and parent folder tokens.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact/skill.json lists 1.0.0 and QUICK-REFERENCE.md lists v2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
