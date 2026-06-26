## Description: <br>
Front API integration with managed OAuth for managing conversations, messages, contacts, tags, inboxes, teammates, and teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to let an agent inspect and manage Front workspace data through Maton-managed OAuth, including customer conversations, messages, contacts, tags, inboxes, teammates, and teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY and uses OAuth-backed Front access through Maton. <br>
Mitigation: Keep MATON_API_KEY secret, store it in an environment or secrets manager, and install only if you trust Maton to proxy Front requests. <br>
Risk: Requests can target the wrong Front workspace when multiple Front connections are active. <br>
Mitigation: Use the Maton-Connection header to select the intended Front connection before making API calls. <br>
Risk: Send, create, update, and delete operations can alter shared customer communications and workspace resources. <br>
Mitigation: Review and confirm the target resource and intended effect before every write operation. <br>
Risk: Front workspace data may include sensitive customer, teammate, or account information. <br>
Mitigation: Limit use to authorized workspaces and handle retrieved data according to the organization's customer data policies. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/front-api) <br>
- [Maton](https://maton.ai) <br>
- [Front API Reference](https://dev.frontapp.com/reference/introduction) <br>
- [Front API Authentication](https://dev.frontapp.com/docs/authentication) <br>
- [Front API Rate Limits](https://dev.frontapp.com/docs/rate-limiting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP endpoint examples, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and network access; may perform OAuth-backed Front API calls when authorized.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
