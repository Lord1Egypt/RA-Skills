## Description: <br>
beehiiv API integration with managed OAuth for managing newsletter publications, subscriptions, posts, custom fields, segments, tiers, and automations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to access beehiiv through Maton OAuth, manage newsletter publications and subscribers, create or inspect posts, organize fields, segments, tiers, automations, and troubleshoot beehiiv API usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires MATON_API_KEY and can access the connected beehiiv account through Maton. <br>
Mitigation: Protect MATON_API_KEY, avoid printing it in shared logs, and install the skill only when agent access to beehiiv through Maton is intended. <br>
Risk: Requests may affect the wrong beehiiv account when multiple Maton beehiiv connections exist. <br>
Mitigation: Confirm the intended connection and include the Maton-Connection header when more than one beehiiv connection is available. <br>
Risk: Create, update, or delete operations can change subscribers, posts, fields, segments, tiers, automations, or OAuth connections. <br>
Mitigation: Require explicit user confirmation before any write or delete request, including the target resource and intended effect. <br>


## Reference(s): <br>
- [beehiiv Developer Documentation](https://developers.beehiiv.com/) <br>
- [beehiiv API Reference](https://developers.beehiiv.com/api-reference) <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/beehiiv) <br>
- [Publisher profile](https://clawhub.ai/user/byungkyu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, JavaScript, HTTP request, and JSON examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include beehiiv API paths, request headers, environment variable setup, pagination notes, error handling guidance, and confirmation requirements for write operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
