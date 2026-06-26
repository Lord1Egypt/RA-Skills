## Description: <br>
Feishu/Lark Bitable CRUD skill that teaches an agent to use feishu_bitable_* tools for creating, reading, and updating Feishu Bitable records while resolving wiki URLs to real bitable app tokens before use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingzuer](https://clawhub.ai/user/lingzuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to read or write Feishu/Lark Bitable data, including records, fields, and tables. It helps avoid token confusion by requiring URL metadata resolution before CRUD operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can create or update Feishu Bitable data when granted write access. <br>
Mitigation: Use least-privilege Feishu permissions, grant collaborator access only to intended Bitables, and require confirmation of the target app, table, records, fields, and values before writes. <br>
Risk: Using a wiki node token as a bitable app token can target the wrong identifier and cause failed operations. <br>
Mitigation: Resolve every Feishu wiki or base URL with feishu_bitable_get_meta before performing CRUD operations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lingzuer/feishu-bitable-crud) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline tool-call examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance depends on the Feishu plugin and least-privilege Feishu permissions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
