## Description: <br>
FeishuBitable-Plus is a Node.js CLI skill for operating Feishu Bitable tables with natural-language commands, CRUD actions, batch import/export, synchronization, and data quality analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwybirth](https://clawhub.ai/user/zwybirth) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operations teams use this skill to query and manage Feishu Bitable records from an agent or CLI workflow. It supports record creation, update, deletion, import/export, synchronization, and data quality review when connected to authorized Feishu credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Natural-language commands can create, update, delete, import, or synchronize Feishu Bitable business records without enough built-in safeguards. <br>
Mitigation: Use least-privilege Feishu permissions, test against non-production tables first, review intended changes before execution, and back up important data before write/delete/import/sync operations. <br>
Risk: The stored Feishu App Secret is sensitive and is not protected by a real keychain or strong encryption according to the server security guidance. <br>
Mitigation: Treat local configuration files as secrets, restrict filesystem access, rotate credentials after exposure, and prefer credentials scoped to only the required Bitable permissions. <br>
Risk: The release overstates local-only privacy protections and should not be relied on as written. <br>
Mitigation: Review network behavior and data handling before installing in a production environment, and validate the skill against organizational privacy and security requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zwybirth/feishu-bitable-plus) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Project homepage listed in skill.yaml](https://github.com/openclaw/feishu-bitable-plus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI text output, markdown guidance, and JSON files for table import/export workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu App ID, App Secret, app token, and table or record identifiers; write, delete, import, and sync commands can modify business data.] <br>

## Skill Version(s): <br>
1.0.0-beta (source: server release, skill.yaml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
