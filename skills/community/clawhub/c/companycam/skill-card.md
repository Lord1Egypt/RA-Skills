## Description: <br>
CompanyCam API integration with managed OAuth for managing projects, photos, users, tags, groups, documents, checklists, labels, collaborators, webhooks, and company information for contractor photo documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage CompanyCam resources through Maton's managed OAuth connector. It supports account, project, media, metadata, checklist, collaborator, and webhook workflows for contractor photo documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and access to a connected CompanyCam account. <br>
Mitigation: Install only if Maton is trusted with the CompanyCam connection, keep MATON_API_KEY out of shared terminal output, and scope access to the intended account. <br>
Risk: Create, update, delete, upload, user/group, and webhook actions can change CompanyCam account data or send event data to external URLs. <br>
Mitigation: Confirm the target resource, intended effect, webhook destination URL, and event scopes with the user before allowing the agent to act. <br>


## Reference(s): <br>
- [CompanyCam Skill on ClawHub](https://clawhub.ai/byungkyu/companycam) <br>
- [Maton](https://maton.ai) <br>
- [CompanyCam API Documentation](https://docs.companycam.com) <br>
- [CompanyCam API Reference](https://docs.companycam.com/reference) <br>
- [CompanyCam Getting Started](https://docs.companycam.com/docs/getting-started) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform CompanyCam API requests through Maton when the user provides credentials and approves write operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
