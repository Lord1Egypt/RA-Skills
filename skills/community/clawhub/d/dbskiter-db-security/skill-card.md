## Description: <br>
数据库安全审计 helps agents run dbskiter database security audits, including SQL injection checks, sensitive data scans, permission reviews, login monitoring, audit log analysis, password policy checks, and configuration reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magicczc](https://clawhub.ai/user/magicczc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database administrators, and security engineers use this skill to select and interpret dbskiter security commands for authorized database audits and remediation planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database audits can expose sensitive database, personal data, and account-level security findings if scans are run too broadly or shared carelessly. <br>
Mitigation: Use the skill only on databases the user is authorized to audit, scope scans to specific databases or tables where possible, and treat generated audit output as confidential. <br>
Risk: The skill relies on a local dbskiter CLI that performs the actual audit commands. <br>
Mitigation: Install and use the dbskiter CLI only from a trusted source before allowing an agent to execute its commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/magicczc/dbskiter-db-security) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/magicczc) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Analysis, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on the dbskiter CLI and an authorized database target; command output may include confidential database and account findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
