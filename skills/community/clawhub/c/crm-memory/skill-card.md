## Description: <br>
Crm Memory maintains structured local CRM memory files for customers, contacts, opportunities, contracts, delivery work, and conversation logs, with automatic updates after customer-related conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales agents and developers use this skill to persist customer context across conversations, retrieve relevant CRM memory before follow-up work, and keep customer records organized as Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain and update sensitive customer information with broad activation triggers and limited user control. <br>
Mitigation: Use explicit save and retrieve requests, review changes before writing customer data, and add redaction and deletion controls before using real customer records. <br>
Risk: Automatic updates and file splitting can change local CRM memory files in ways that are hard to audit after the fact. <br>
Mitigation: Keep backups, review generated diffs, and confirm split indexes before relying on updated customer records. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andyrenxu7255/crm-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/andyrenxu7255) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>
- [Artifact Manifest](artifact/clawhub.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files and concise text confirmations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains files under memory/customers/ and may split large customer records into indexed Markdown subfiles.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
