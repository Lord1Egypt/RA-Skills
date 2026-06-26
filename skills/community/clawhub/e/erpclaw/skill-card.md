## Description: <br>
AI-native ERP system for accounting, invoicing, inventory, purchasing, tax, billing, HR, payroll, advanced accounting, and financial reporting across ERP domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
GNU General Public License v3 <br>


## Use Case: <br>
Business users and operators use this skill to let an agent manage local ERP workflows such as company setup, invoices, payments, inventory, payroll, reporting, and period-close tasks while keeping accounting records in an ERP database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority over sensitive accounting, payroll, banking, modules, and local files. <br>
Mitigation: Install only for a trusted ERP environment, start with a test database, keep backups, restrict roles, and require explicit human approval for posting, imports, payroll, key restore, credential changes, module updates, customer emails, and period-close workflows. <br>
Risk: Incorrect or under-reviewed financial actions can affect books of record. <br>
Mitigation: Review module sources before install or update, protect payroll and ACH outputs, avoid arbitrary CSV paths, and require human confirmation for high-impact actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mailnike/erpclaw) <br>
- [ERPClaw website](https://www.erpclaw.ai) <br>
- [ERPClaw docs](https://www.erpclaw.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Plain-language responses with command-backed ERP actions and structured JSON results from local scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and git on darwin or linux; optional ERPCLAW_DB_PATH controls the local database path.] <br>

## Skill Version(s): <br>
4.8.0 (source: SKILL.md frontmatter, CHANGELOG, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
