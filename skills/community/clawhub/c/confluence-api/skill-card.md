## Description: <br>
Confluence API integration with managed OAuth for managing pages, spaces, blogposts, comments, and attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to read and manage Confluence Cloud content through Maton-managed OAuth. It supports page, space, blogpost, comment, attachment, property, task, label, and custom-content workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and OAuth connection that can access Confluence content. <br>
Mitigation: Install only if Maton is trusted to broker access, keep MATON_API_KEY secret, and avoid sharing command output that could expose credentials or sensitive workspace data. <br>
Risk: Create, update, and delete operations can change or remove Confluence content. <br>
Mitigation: Require exact user confirmation of the target resource and intended effect before approving any write operation. <br>
Risk: When multiple Confluence connections exist, a request may target the wrong workspace or account. <br>
Mitigation: Specify the intended connection with the Maton-Connection header when more than one account is available. <br>


## Reference(s): <br>
- [Confluence skill on ClawHub](https://clawhub.ai/byungkyu/confluence-api) <br>
- [Maton](https://maton.ai) <br>
- [Confluence REST API V2 documentation](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/) <br>
- [Confluence REST API V2 reference](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/) <br>
- [Confluence storage format](https://confluence.atlassian.com/doc/confluence-storage-format-790796544.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with inline HTTP endpoints and Python or JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a Confluence OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
