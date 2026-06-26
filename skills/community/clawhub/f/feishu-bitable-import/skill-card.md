## Description: <br>
Imports local CSV, Excel, or JSON data into Feishu Bitable, with field-type inference, incremental sync, full replacement, append-only sync, and table creation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanlansss](https://clawhub.ai/user/guanlansss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to prepare Feishu credentials, identify app and table IDs, and run import or sync commands that move local business data into Feishu Bitable tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete or overwrite Feishu Bitable business records, especially when full sync mode is used. <br>
Mitigation: Back up important tables, verify app_token and table_id before running commands, and avoid --mode full unless replacing all existing records is intentional. <br>
Risk: The skill requires Feishu credentials and write access to Bitable data. <br>
Mitigation: Use a dedicated least-privilege Feishu app, grant only the required Bitable permissions, and keep the .env file out of source control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guanlansss/feishu-bitable-import) <br>
- [How to get app_token and table_id](references/get-id-guide.md) <br>
- [Feishu Bitable API Documentation](https://open.feishu.cn/document/ukTMukTMukTM/uYTM5UjL2ETO14iNkozM) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of local Python scripts that read CSV, Excel, or JSON files and call Feishu Bitable APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
