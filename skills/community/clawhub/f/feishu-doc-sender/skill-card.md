## Description: <br>
Helps agents find workspace Word (.docx) and PDF documents, confirm matched files, and send selected documents to Feishu/Lark users or groups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill when an agent needs to find workspace Word or PDF documents, confirm the exact matches, and help send them to Feishu/Lark users or groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documents may contain sensitive content, embedded metadata, comments, or tracked changes that should not be shared with the selected recipient. <br>
Mitigation: Before approving a send, review the exact file list, recipient or group, file sensitivity, document metadata, and the Feishu/Lark account or integration being used. <br>
Risk: Workspace file discovery may match unintended documents when filenames are generic or keywords are broad. <br>
Mitigation: Use specific keywords or format filters and require confirmation of the matched files before any document is sent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/feishu-doc-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown/text responses with optional shell commands and JSON file listings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Lists matched document files for user confirmation before sending; the helper script can emit JSON for file listings.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
