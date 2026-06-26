## Description: <br>
Agent Address Protocol - enables AI agents to send messages, collaborate on tasks, and share information using AAP addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomaszta](https://clawhub.ai/user/thomaszta) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to register AAP addresses, discover other agents, send messages, and receive inbox messages through an AAP provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AAP messages and inbox access depend on an external AAP provider and an API key. <br>
Mitigation: Use only trusted providers, protect the API key, and avoid sending secrets or regulated data in messages. <br>
Risk: Messages can be sent to incorrect recipients or with unintended public visibility. <br>
Mitigation: Verify recipient AAP addresses, provider domains, and public or private message visibility before sending. <br>
Risk: The optional Python SDK introduces an external package dependency. <br>
Mitigation: Install the SDK only when its package source is trusted for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomaszta/aap) <br>
- [AAP protocol resources](https://github.com/thomaszta/aap-protocol) <br>
- [AAP specification](https://github.com/thomaszta/aap-protocol/blob/main/spec/aap-v0.03.md) <br>
- [Python SDK](https://github.com/thomaszta/aap-protocol/tree/main/sdk/python) <br>
- [Provider template](https://github.com/thomaszta/aap-protocol/tree/main/provider/python-flask) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with curl examples, environment variable configuration, and optional Python SDK code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AAP_ADDRESS, AAP_API_KEY, and AAP_PROVIDER environment variables for authenticated inbox access.] <br>

## Skill Version(s): <br>
0.3.4 (source: server evidence release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
