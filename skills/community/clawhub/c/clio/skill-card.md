## Description: <br>
Clio API integration with managed OAuth for reading, creating, updating, and deleting legal practice data such as matters, contacts, activities, tasks, documents, calendar entries, time entries, and billing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal operations users and their agents use this skill to work with Clio Manage records through Maton's managed OAuth gateway, including matter, contact, task, document, calendar, time, and billing workflows. It is appropriate when the user can provide a valid Maton API key and explicitly approve write or delete operations against specific records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change sensitive legal practice data through Maton, including matters, contacts, documents, billing, and time entries. <br>
Mitigation: Install only if the organization permits this third-party OAuth gateway, keep MATON_API_KEY private, and use the narrowest Clio permissions available. <br>
Risk: Write and delete operations can modify or remove legal records when given the wrong target account or record identifier. <br>
Mitigation: Default to read-only lookup first, specify the intended connection when multiple Clio accounts exist, and approve writes or deletes only after checking exact record IDs and consequences. <br>


## Reference(s): <br>
- [ClawHub Clio skill page](https://clawhub.ai/byungkyu/clio) <br>
- [Maton homepage](https://maton.ai) <br>
- [Clio API Documentation](https://docs.developers.clio.com/api-reference/) <br>
- [Clio Fields Guide](https://docs.developers.clio.com/api-docs/clio-manage/fields/) <br>
- [Clio Rate Limits](https://docs.developers.clio.com/api-docs/clio-manage/rate-limits/) <br>
- [Clio Permissions](https://docs.developers.clio.com/api-docs/permissions/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with API endpoint guidance and Python, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Clio OAuth account.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
