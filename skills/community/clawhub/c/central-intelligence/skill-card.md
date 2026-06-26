## Description: <br>
Persistent memory across sessions for remembering facts, recalling them later with semantic search, sharing knowledge between agents, and forgetting outdated memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alekseimarchenko](https://clawhub.ai/user/alekseimarchenko) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist selected memories across sessions, retrieve relevant prior context, and manage memory scope for agent, user, or organization sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memories are stored in an external persistent memory service, which can create privacy or confidentiality exposure if sensitive content is saved. <br>
Mitigation: Do not store secrets, credentials, personal identifiers, or confidential business data as memories; review content before saving. <br>
Risk: Sharing a memory beyond the agent scope may expose information to other agents for the same user or organization. <br>
Mitigation: Use agent scope by default and share only non-sensitive information that is relevant to other agents. <br>
Risk: Recalled memories may be stale or no longer accurate. <br>
Mitigation: Verify recalled memories before acting on critical information and delete outdated memories with the forget command. <br>


## Reference(s): <br>
- [Central Intelligence service](https://centralintelligence.online) <br>
- [Central Intelligence repository](https://github.com/AlekseiMarchenko/central-intelligence) <br>
- [Central Intelligence API](https://central-intelligence-api.fly.dev) <br>
- [ClawHub skill page](https://clawhub.ai/alekseimarchenko/central-intelligence) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CI_API_KEY and sends selected memory content to an external Central Intelligence service.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
