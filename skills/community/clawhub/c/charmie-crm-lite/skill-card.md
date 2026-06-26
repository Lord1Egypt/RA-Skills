## Description: <br>
Lightweight CRM with SQLite – manage contacts. Upgrade to Pro for email, messaging, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[businessbrainsolutions](https://clawhub.ai/user/businessbrainsolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to manage a local SQLite contact list through an agent, including adding, searching, updating, and deleting contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete CRM records through broad natural-language requests. <br>
Mitigation: Use explicit commands for update and delete actions, such as naming the target contact and requested change. <br>
Risk: Important contact data could be lost if local records are modified or deleted unintentionally. <br>
Mitigation: Keep backups of important contact data before using write or delete operations. <br>


## Reference(s): <br>
- [Charmie CRM Lite on ClawHub](https://clawhub.ai/businessbrainsolutions/charmie-crm-lite) <br>
- [Business Brain Solutions homepage](https://BusinessBrainSolutions.WealthDaoinc.com) <br>
- [Charmie CRM Professional upgrade](https://BusinessBrainSolutions.WealthDaoinc.com/pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text responses and JSON-encoded contact search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create, update, and delete records in a local SQLite contacts database.] <br>

## Skill Version(s): <br>
3.0.3 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
