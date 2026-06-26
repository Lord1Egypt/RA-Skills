## Description: <br>
Aicoo Discover helps an agent search Aicoo Square for relevant people, present concise profile recommendations, and suggest next contact actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xisen-w](https://clawhub.ai/user/xisen-w) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, builders, and other Aicoo users use this skill to discover people on Square by interests, project context, or explicit search criteria, then decide whether to chat, connect, or send a request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide credentialed chat, connect, friend-request, or batch actions that may change Aicoo network relationships. <br>
Mitigation: Require explicit user confirmation before any chat, connect, friend-request, or batch action, and provide API keys only when those account effects are acceptable. <br>
Risk: The skill requires sensitive credentials for network operations. <br>
Mitigation: Keep API keys out of agent output, use scoped environment variables, and review proposed API calls before execution. <br>


## Reference(s): <br>
- [Aicoo Discover on ClawHub](https://clawhub.ai/xisen-w/aicoo-discover) <br>
- [Aicoo Square search endpoint](https://www.aicoo.io/api/square) <br>
- [Aicoo guest chat endpoint](https://www.aicoo.io/api/chat/guest-v04) <br>
- [Aicoo network connect endpoint](https://www.aicoo.io/api/v1/network/connect) <br>
- [Aicoo network request endpoint](https://www.aicoo.io/api/v1/network/request) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with concise profile lists and optional curl command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use public Square search and, with explicit user authorization and credentials, account-affecting chat, connect, or friend-request API calls.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
