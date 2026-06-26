## Description: <br>
Calls a configured Dify API from OpenClaw so an agent can query a knowledge base in conversational mode with optional conversation continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yep123456](https://clawhub.ai/user/yep123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, support teams, and developers use this skill to ask questions against a configured Dify knowledge base from OpenClaw. It is suited for internal document lookup, policy Q&A, and customer-support style knowledge retrieval when the Dify deployment is trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Dify API key and endpoint configuration. <br>
Mitigation: Use a scoped API key, store it only in the expected local configuration file, and rotate it if it is exposed. <br>
Risk: User questions are sent to the configured Dify endpoint and may be logged by that deployment. <br>
Mitigation: Use only approved Dify deployments and avoid sending secrets, regulated data, or other sensitive content unless that endpoint is authorized for it. <br>
Risk: Responses depend on the availability, permissions, and quality of the configured Dify knowledge base. <br>
Mitigation: Confirm the endpoint, access policy, and knowledge-base content before relying on answers for operational decisions. <br>


## Reference(s): <br>
- [Dify API documentation](https://docs.dify.ai/) <br>
- [Dify Workflow Run API](https://docs.dify.ai/reference/dify-api/apis/workflow-run) <br>
- [OpenClaw CLI tools documentation](https://docs.openclaw.ai/cli-tools) <br>
- [Server-Sent Events API](https://developer.mozilla.org/zh-CN/docs/Web/API/Server-sent_events) <br>
- [ClawHub release page](https://clawhub.ai/yep123456/dify-chat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Command-line text output with streamed API response text and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIFY_API_KEY and a configured DIFY_API_BASE; sends user queries to the configured Dify endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md changelog, released 2026-04-14 in skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
