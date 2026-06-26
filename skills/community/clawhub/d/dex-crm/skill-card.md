## Description: <br>
Manage Dex personal CRM contacts, notes, reminders, and contact details through Dex API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaybna](https://clawhub.ai/user/jaybna) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to search or browse Dex contacts, add notes, create or check reminders, and inspect contact details such as phone numbers, email addresses, and birthdays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad read/write authority over Dex CRM contacts, notes, and reminders, including delete and archive operations. <br>
Mitigation: Use a Dex API key with access you are comfortable granting, review the exact target records before write/delete/archive actions, and require explicit confirmation before changes. <br>
Risk: The included cleanup script can bulk-archive contacts based on heuristic junk detection. <br>
Mitigation: Run the cleanup script with --dry-run first and review all proposed archived contacts before running it without dry-run mode. <br>


## Reference(s): <br>
- [Dex CRM](https://getdex.com) <br>
- [Dex API Settings](https://getdex.com/settings/api) <br>
- [Dex API Base](https://api.getdex.com/api/rest) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaybna/dex-crm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Dex API requests that read, create, update, delete, or archive CRM records; requires DEX_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
