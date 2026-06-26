## Description: <br>
Basecamp API integration with managed OAuth for managing projects, to-dos, messages, schedules, documents, and team collaboration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to connect an agent to Basecamp through Maton-managed OAuth and perform project, to-do, message, schedule, document, chat, comment, and collaboration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY provides OAuth-mediated access to the connected Basecamp account through Maton. <br>
Mitigation: Install only if Maton is trusted, keep MATON_API_KEY private, and review the connected Basecamp permissions. <br>
Risk: The skill can create, update, or delete Basecamp projects, to-dos, comments, and other account data. <br>
Mitigation: Require explicit user confirmation of the target resource and intended effect before any write or delete operation. <br>
Risk: Multiple Basecamp OAuth connections can cause requests to target the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one active Basecamp connection exists. <br>


## Reference(s): <br>
- [ClawHub Basecamp skill page](https://clawhub.ai/byungkyu/basecamp) <br>
- [Basecamp 4 API Documentation](https://github.com/basecamp/bc3-api) <br>
- [Basecamp Authentication Guide](https://github.com/basecamp/bc3-api/blob/master/sections/authentication.md) <br>
- [Basecamp API Reference](https://github.com/basecamp/bc3-api#endpoints) <br>
- [Maton Basecamp API endpoint](https://api.maton.ai/basecamp/{resource}.json) <br>
- [Maton connection management](https://api.maton.ai/connections) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline HTTP paths, JSON examples, and Python or JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY for OAuth-mediated Basecamp access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
