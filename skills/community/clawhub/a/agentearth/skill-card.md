## Description: <br>
Agentearth helps an agent discover, select, validate, and execute Agent Earth tools for current information, decision support, data retrieval, and multi-step external-information tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanminghui](https://clawhub.ai/user/shanminghui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route external-information requests through Agent Earth, including current news, weather, price lookups, tool discovery, and context-aware multi-step tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes broad user requests and selected conversation context to Agent Earth under the configured API key. <br>
Mitigation: Use only with approved data and avoid secrets, credentials, confidential documents, and sensitive personal data. <br>
Risk: Agent Earth can choose and execute unspecified remote tools, including actions that may affect accounts, upload files, post publicly, change data, or spend money. <br>
Mitigation: Validate the selected tool and parameters, and require explicit approval before sensitive, public, account-changing, or cost-incurring actions. <br>


## Reference(s): <br>
- [Agentearth ClawHub page](https://clawhub.ai/shanminghui/agentearth) <br>
- [Agent Earth API specification](references/api-spevification.md) <br>
- [Agent Earth](https://agentearth.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text summarizing remote tool results and next-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGENT_EARTH_API_KEY and may send task prompts and selected conversation context to Agent Earth.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
