## Description: <br>
AI-native ERP system with self-extending OS for accounting, invoicing, inventory, purchasing, tax, billing, HR, payroll, advanced accounting, financial reporting, module generation, schema migration, and audit workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mailnike](https://clawhub.ai/user/mailnike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, finance teams, HR/payroll administrators, and developers use this skill to manage local ERP records, run accounting and payroll workflows, generate financial reports, install industry or regional modules, and scaffold or validate ERP extensions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate business, payroll, inventory, and accounting records, including submit, cancel, approve, restore, cleanup, and scheduled recurring actions. <br>
Mitigation: Use it only with reviewed permissions, backups, and human approval for high-impact financial or personnel workflows. <br>
Risk: The skill can install or update modules and deploy modules from downloaded code. <br>
Mitigation: Review module sources and restrict installation, update, schema apply, schema rollback, and deploy actions to trusted operators. <br>
Risk: The web dashboard setup can clone a web project and change host-level nginx, systemd, and TLS configuration. <br>
Mitigation: Avoid production dashboard setup until the cloned project and host configuration changes have been reviewed and approved. <br>


## Reference(s): <br>
- [ERP Claw on ClawHub](https://clawhub.ai/mailnike/erp-claw) <br>
- [OpenClaw](https://openclaw.org) <br>
- [ERPClaw website](https://www.erpclaw.ai) <br>
- [ERPClaw Web dashboard](https://github.com/avansaber/erpclaw-web) <br>
- [WebClaw dashboard](https://github.com/avansaber/webclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with command examples, JSON-like action results, generated code, configuration instructions, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Python scripts that read or mutate a SQLite ERP database and may initiate confirmed module installation or dashboard setup actions.] <br>

## Skill Version(s): <br>
3.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
