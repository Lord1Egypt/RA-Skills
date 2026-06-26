## Description: <br>
A conversational CRM skill that helps an administrator create, update, search, and analyze customer records stored as local YAML files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1232023](https://clawhub.ai/user/luis1232023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators and administrators use this skill to maintain lightweight CRM records, add follow-up and service activity, search customer data, and generate sales or service summaries from local YAML files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive customer contact, service, and sales data in local YAML files. <br>
Mitigation: Use it only in a trusted workspace, define privacy and retention practices before real customer use, and keep backups of customer data. <br>
Risk: Customer names are used to construct local filenames, and the security evidence flags unsafe file path handling. <br>
Mitigation: Do not use customer names containing slashes, dots, or path-like characters; maintainers should add filename validation and path containment before production use. <br>
Risk: Several workflows write or update CRM records. <br>
Mitigation: Require manual confirmation for write actions and maintain recoverable backups before bulk or production usage. <br>


## Reference(s): <br>
- [CRM Manager design reference](references/design_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/luis1232023/crm-manager-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown responses, CLI output, and YAML customer record files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and updates local CRM YAML files under the skill data directory.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
