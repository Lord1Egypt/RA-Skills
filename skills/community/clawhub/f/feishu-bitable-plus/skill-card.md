## Description:

FeishuBitable-Plus is a local Node.js CLI skill for operating Feishu Bitable with natural-language commands, CRUD actions, batch import and export, table sync, reporting, and data quality analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwybirth](https://clawhub.ai/user/zwybirth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and modify Feishu Bitable data from an agent or CLI. It supports natural-language requests and explicit commands for records, tables, import/export, sync, reports, and data quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete live Feishu Bitable business data through broad natural-language and CLI commands.

Mitigation: Use a least-privilege Feishu app and test write, delete, and sync commands on non-production tables before allowing production use.

Risk: Feishu app secrets are stored weakly and may be exposed if passed on the command line.

Mitigation: Avoid command-line secrets, prefer interactive credential entry, restrict local credential file access, and rotate any secret previously entered in shell history.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zwybirth/skills/feishu-bitable-plus)
- [ClawHub Publisher Profile](https://clawhub.ai/user/zwybirth)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown guidance with CLI commands, terminal text, and JSON command outputs or exported files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can execute Feishu Bitable API operations and write exported records to local JSON files.]

## Skill Version(s):

1.0.0-beta (source: server release metadata, skill.yaml, CHANGELOG released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
