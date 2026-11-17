## Description:

This skill helps agents manage DingTalk calendar events and meetings through DingTalk MCP servers, including scheduling, updates, participant changes, room booking, availability checks, and invitation responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cpsean](https://clawhub.ai/user/cpsean)

### License/Terms of Use:

MIT-0

## Use Case:

DingTalk users and teams use this skill to let an MCP-capable agent create, edit, delete, query, and coordinate calendar events, participants, meeting rooms, and availability. It is intended for DingTalk calendar and meeting workflows, not other calendar platforms or DingTalk messaging/document operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The DingTalk MCP endpoint can contain an API key and may be saved into agent configuration.

Mitigation: Verify the endpoint comes from the official DingTalk AIHub page, prefer project-scoped or manual configuration where possible, and avoid sharing or repeating the full URL.

Risk: Calendar access, and optional contacts access, can expose meeting details and employee lookup data.

Mitigation: Install only for users who are comfortable granting that access, and enable the contacts MCP only when participant lookup is required.

Risk: The contacts cache can retain employee identifiers locally.

Mitigation: Periodically clear the cache or avoid using it when employee identifiers are sensitive.

Risk: Write operations can create, modify, delete, or share DingTalk calendar resources.

Mitigation: Review the skill's confirmation summary before approving any non-read action.

## Reference(s):

- [DingTalk calendar and contacts MCP tools reference](artifact/references/mcp-tools.md)
- [DingTalk calendar MCP setup page](https://aihub.dingtalk.com/#/detail?mcpId=1050&detailType=marketMcpDetail)
- [DingTalk contacts MCP setup page](https://aihub.dingtalk.com/#/detail?mcpId=2400&detailType=marketMcpDetail)
- [DingTalk developer getting started](https://open.dingtalk.com/document/dingstart/dingtalk-developer)
- [ClawHub skill page](https://clawhub.ai/cpsean/skills/dingtalk-meetings-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and MCP tool-call instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DingTalk calendar MCP for core operations and optionally DingTalk contacts MCP for participant lookup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
