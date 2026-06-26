## Description: <br>
Clockify API integration with managed OAuth for tracking time and managing projects, clients, tasks, workspaces, and workspace members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to access Clockify through Maton-managed OAuth, including reading user, workspace, project, client, tag, task, and time-entry data. With explicit user approval, it can help create, update, or delete Clockify resources through API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key is a sensitive credential that grants access to connected Clockify data. <br>
Mitigation: Keep MATON_API_KEY private, avoid logging it, and install only if you trust Maton as the OAuth proxy. <br>
Risk: When multiple Clockify connections exist, requests may target the wrong account. <br>
Mitigation: Use the Maton-Connection header to select the intended Clockify connection before sending account-specific requests. <br>
Risk: Create, update, and delete operations can change billing, project, task, workspace, or time-tracking records. <br>
Mitigation: Confirm the target resource and intended effect with the user before any write or delete request. <br>


## Reference(s): <br>
- [Clockify API Documentation](https://docs.clockify.me/) <br>
- [Clockify Time Entry API Reference](https://docs.clockify.me/#tag/Time-entry) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Clockify Skill on ClawHub](https://clawhub.ai/byungkyu/clockify) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with HTTP examples and inline Python, JavaScript, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Clockify OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
