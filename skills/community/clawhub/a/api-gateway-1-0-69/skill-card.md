## Description: <br>
Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call native endpoints for connected services such as Google Workspace, Microsoft 365, GitHub, Notion, Slack, Airtable, and HubSpot after the user authorizes each service connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is a broad API gateway that can act on many connected services. <br>
Mitigation: Connect only the accounts needed, verify the active connection before use, and require explicit human confirmation before create, update, delete, send, publish, billing, admin, or webhook actions. <br>
Risk: The Maton API key enables use of the gateway with any service connections the user has authorized. <br>
Mitigation: Keep MATON_API_KEY secret, avoid sharing it in prompts or logs, and remove unneeded or stale service connections. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kenswj/api-gateway-1-0-69) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Maton API Reference](https://www.maton.ai/docs/api-reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and the MATON_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
