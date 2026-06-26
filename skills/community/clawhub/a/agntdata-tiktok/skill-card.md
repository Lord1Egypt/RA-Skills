## Description: <br>
Use one API key to pull TikTok short-form video and creator data for agents, automations, and analytics, returning structured JSON with credit-based pricing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, analytics teams, and social research teams use this skill to call agntdata TikTok endpoints for video details, creator profiles, account search, video search, collections, and user video feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an agntdata API key and sends TikTok usernames, video IDs, search terms, and use-case text to agntdata. <br>
Mitigation: Install only when agntdata is trusted for the request data, keep the key in an environment variable or secrets manager, and avoid sending confidential research terms unless approved. <br>
Risk: Requests use credit-based pricing and can incur usage costs. <br>
Mitigation: Monitor account credit usage and scope automated requests to the minimum data needed. <br>
Risk: The skill recommends a separate OpenClaw plugin for native tools. <br>
Mitigation: Review and scan the @agntdata/openclaw-tiktok plugin independently before installing it. <br>


## Reference(s): <br>
- [TikTok API documentation](https://agnt.mintlify.app/apis/social/tiktok) <br>
- [agntdata documentation](https://agnt.mintlify.app) <br>
- [agntdata dashboard](https://app.agntdata.dev/dashboard) <br>
- [ClawHub skill page](https://clawhub.ai/jaencarrodine/agntdata-tiktok) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with JSON examples and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY and curl; API responses are structured JSON from agntdata endpoints.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
