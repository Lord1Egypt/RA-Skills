## Description: <br>
Constant Contact API integration with managed OAuth for reading, creating, updating, deleting, and bulk-modifying Constant Contact contacts, campaigns, lists, tags, custom fields, segments, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and marketing operators use this skill to let an agent administer Constant Contact data through Maton-managed OAuth, including contact management, campaign workflows, segmentation, and analytics. It is appropriate when the user can supply a Maton API key and approve write or high-impact actions explicitly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive MATON_API_KEY credential. <br>
Mitigation: Keep MATON_API_KEY secret, provide it only through the runtime environment, and rotate it if it is exposed. <br>
Risk: Requests may affect the wrong Constant Contact account when multiple OAuth connections exist. <br>
Mitigation: Use the Maton-Connection header for account selection and confirm the intended connection before write operations. <br>
Risk: Write, bulk, delete, sender-email, OAuth connection deletion, and campaign-send operations can change marketing data or affect external recipients. <br>
Mitigation: Retrieve and show the exact target resources, summarize the effect, and wait for explicit user approval before executing high-impact actions. <br>
Risk: Campaign sends and schedules can deliver email to external recipients. <br>
Mitigation: Preview campaign content and confirm recipients, sender, subject, and schedule before sending or scheduling. <br>


## Reference(s): <br>
- [ClawHub Constant Contact listing](https://clawhub.ai/byungkyu/constant-contact) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>
- [Constant Contact V3 API Overview](https://developer.constantcontact.com/api_guide/getting_started.html) <br>
- [Constant Contact API Reference](https://developer.constantcontact.com/api_reference/index.html) <br>
- [Constant Contact Technical Overview](https://developer.constantcontact.com/api_guide/v3_technical_overview.html) <br>
- [Constant Contact Contacts Overview](https://developer.constantcontact.com/api_guide/contacts_overview.html) <br>
- [Constant Contact Email Campaigns Guide](https://developer.constantcontact.com/api_guide/email_campaigns_get_started.html) <br>
- [Constant Contact Contact Lists Overview](https://v3.developer.constantcontact.com/api_guide/lists_overview.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, and HTTP examples for Constant Contact API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write, bulk, delete, sender-email, OAuth connection deletion, and campaign-send operations require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
