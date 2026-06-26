## Description: <br>
Queries an enterprise AliMail directory for employee names, email addresses, and employee numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Colin-megan](https://clawhub.ai/user/Colin-megan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized employees and agents use this skill to look up internal AliMail directory entries by employee name when they need an email address or employee number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose internal AliMail employee-directory data when used with valid credentials. <br>
Mitigation: Install only in authorized workspaces, use scoped AliMail OAuth credentials, and restrict access to users with a legitimate business need. <br>
Risk: Automatic lookup of names mentioned in conversation can query employee records without clear intent. <br>
Mitigation: Prefer explicit lookup prompts or confirmation before searching names mentioned in conversation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Colin-megan/alimail) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text] <br>
**Output Format:** [JSON object with matching users, total count, or error status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIMAIL_CLIENT_ID and ALIMAIL_CLIENT_SECRET; returns up to 10 matching users.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence, SKILL.md frontmatter, manifest.json, openapi.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
