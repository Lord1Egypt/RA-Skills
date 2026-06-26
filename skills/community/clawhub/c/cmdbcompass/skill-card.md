## Description: <br>
The first CMDB governance skill for ServiceNow. Audit, remediate, and govern your CMDB from any AI agent. Health scoring, duplicate detection, relationship analysis, stale CI cleanup, and governed remediation with full rollback and audit trail on every write. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nexecuteinc](https://clawhub.ai/user/nexecuteinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ServiceNow CMDB administrators, platform teams, and developers use this skill to audit CMDB health, find duplicates and stale configuration items, analyze relationships, and prepare governed remediation workflows through an MCP-compatible agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad ServiceNow CMDB changes through stored ServiceNow credentials. <br>
Mitigation: Use a least-privilege ServiceNow service account, avoid production administrator credentials initially, and require explicit approval for merge, retire, bulk update, or relationship repair actions. <br>
Risk: The installer installs external package code without pinning a trusted version. <br>
Mitigation: Review the cmdb-compass package source or pin a trusted package version before installation. <br>


## Reference(s): <br>
- [CMDB Compass ClawHub page](https://clawhub.ai/nexecuteinc/cmdbcompass) <br>
- [CMDB Compass PyPI package](https://pypi.org/project/cmdb-compass) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide MCP setup and ServiceNow CMDB audit or remediation actions; write-capable actions should require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
