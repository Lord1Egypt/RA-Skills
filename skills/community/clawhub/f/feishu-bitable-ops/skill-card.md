## Description: <br>
Helps agents operate Feishu/Lark Bitable bases by distinguishing wiki and base tokens, listing tables and fields, and guiding record CRUD and batch writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbj375767338-arch](https://clawhub.ai/user/bbj375767338-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to read, create, update, delete, or batch-populate Feishu/Lark Bitable records while handling wiki URL token resolution and field value formats correctly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to create, update, batch-create, or delete Bitable records using configured Feishu app permissions. <br>
Mitigation: Use a least-privilege Feishu app, review app permissions, and confirm table names, record IDs, admin user IDs, and batch contents before write or delete operations. <br>
Risk: Using a wiki node token as a Bitable app token can cause failed operations and confusion about which base is being modified. <br>
Mitigation: Resolve wiki URLs with feishu_wiki_space_node get, then verify the returned app token and table ID before any CRUD action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bbj375767338-arch/feishu-bitable-ops) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Feishu/Lark tool-call examples and bash-style code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes token parsing guidance, field-format tables, CRUD examples, batch operation examples, and common error resolutions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
