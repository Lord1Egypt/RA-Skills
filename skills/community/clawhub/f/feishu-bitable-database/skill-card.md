## Description: <br>
Read, query, update, and manage Feishu Bitable data using SQL-like commands with automatic URL parameter extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xjli360](https://clawhub.ai/user/xjli360) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Feishu Bitable schemas, query records, aggregate table data, and create, update, or delete records through command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update or delete live Feishu Bitable records. <br>
Mitigation: Preview matching records before update or delete operations, avoid filter-based destructive commands until the match set is verified, and keep backups or exports for important tables. <br>
Risk: The skill uses Feishu app credentials and caches tenant access tokens. <br>
Mitigation: Use least-privilege Feishu app permissions and treat FEISHU_APP_SECRET and cached tenant tokens as sensitive credentials. <br>


## Reference(s): <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require FEISHU_APP_ID and FEISHU_APP_SECRET, and can read or modify live Feishu Bitable records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
