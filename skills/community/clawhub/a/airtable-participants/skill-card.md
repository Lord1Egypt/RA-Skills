## Description: <br>
Read and query retreat participant data from the Ceremonia Airtable base, including participant counts, attendance, contact segments, recipient lists, phone numbers, emails, and donation status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[austinmao](https://clawhub.ai/user/austinmao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Authorized operators and agents use this skill to query a retreat participant Airtable for CRM lookups, newsletter and SMS recipient lists, attendance questions, and donation-status checks. It is read-only by default, with record edits requiring explicit Austin approval per change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive participant contact, attendance, and donation data from Airtable. <br>
Mitigation: Install only for agents authorized to access this Airtable, use a least-privilege Airtable token, and keep exported contact and donation data private. <br>
Risk: Record modifications could alter participant CRM data if write access is available. <br>
Mitigation: Prefer a read-only Airtable token unless updates are required, and require clear Austin approval and audit logging before any PATCH operation. <br>


## Reference(s): <br>
- [Airtable Web API Introduction](https://airtable.com/developers/web/api/introduction) <br>
- [ClawHub Skill Page](https://clawhub.ai/austinmao/airtable-participants) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and summarized Airtable query results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIRTABLE_API_KEY plus confirmed Airtable base and table configuration; list queries must be fully paginated before reporting totals or recipient lists.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
