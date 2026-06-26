## Description: <br>
AgoraHub agent registry - discover and use 14+ verified AI agents for dev tasks like hashing, encoding, formatting, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Codevena](https://clawhub.ai/user/Codevena) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to discover AgoraHub agents and call demo or community agents for utility tasks such as hashing, encoding, formatting, conversion, and text analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected inputs are sent to AgoraHub's remote service when users call agents. <br>
Mitigation: Use the skill only after reviewing AgoraHub's trust, privacy, and retention practices for the data being submitted. <br>
Risk: Sensitive values such as real JWTs, API keys, session tokens, private source code, customer records, confidential documents, or regulated data could be submitted to remote agents. <br>
Mitigation: Use synthetic or redacted inputs unless the data is approved for AgoraHub processing. <br>
Risk: The API key can authorize community agents beyond the zero-auth demo agents. <br>
Mitigation: Use AGORAHUB_API_KEY only with community agents that are intentionally trusted. <br>


## Reference(s): <br>
- [AgoraHub](https://agorahub.dev) <br>
- [AgoraHub tool discovery endpoint](https://agorahub.dev/api/mcp/tools) <br>
- [AgoraHub tool call endpoint](https://agorahub.dev/api/mcp/tools/call) <br>
- [AgoraHub API keys](https://agorahub.dev/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; AGORAHUB_API_KEY is used for community agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
