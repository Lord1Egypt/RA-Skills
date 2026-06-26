## Description: <br>
Uploads files from local disk, URLs, or Feishu messages to accessible Feishu Bitable attachment fields through the material upload flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyjbazinga-stack](https://clawhub.ai/user/gyjbazinga-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to move local, URL-hosted, or Feishu message files into Feishu Bitable attachment fields and update or create the target record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload files into Feishu and modify Bitable records. <br>
Mitigation: Use a least-privileged Feishu app and confirm the app_token, table, field, record, source file, and append setting before each run. <br>
Risk: URL mode can fetch content from untrusted or internal addresses. <br>
Mitigation: Avoid URL mode for untrusted, sensitive, or internal URLs; prefer a reviewed local file when the source is uncertain. <br>
Risk: Replace and create operations can change record contents or create new records. <br>
Mitigation: Treat replace and create modes as record-changing actions and review the input payload before execution. <br>


## Reference(s): <br>
- [Feishu API Implementation Notes](artifact/references/feishu-api-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gyjbazinga-stack/feishu-bitable-attachment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON input examples, and JSON success or error results from the upload script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_APP_ID and FEISHU_APP_SECRET, a target Bitable app token, table and field identifiers or names, a source file reference, and append or replace selection.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
