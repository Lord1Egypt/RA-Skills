## Description: <br>
Connect to Daily-to-Goal (D2G) platform via MCP to manage goals, tasks, entities, and team performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoke-bot](https://clawhub.ai/user/xiaoke-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an AI assistant to Daily-to-Goal via MCP for goal, task, entity, and team-performance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write goals, tasks, entities, and team data in the Daily-to-Goal account tied to its API key. <br>
Mitigation: Confirm the account and installation intent before use, and use a dedicated or least-privilege API key where available. <br>
Risk: Broad trigger wording may route generic goal or task requests to this integration. <br>
Mitigation: Clarify that the user wants Daily-to-Goal before creating, updating, deleting, approving, or otherwise changing records. <br>
Risk: The required DTG_API_KEY grants access according to its configured scopes and role. <br>
Mitigation: Store the key in environment variables or a secrets manager, avoid committing it to version control, and review scopes and role permissions. <br>


## Reference(s): <br>
- [Daily-to-Goal platform](https://h5.dd-up.com/) <br>
- [ClawHub skill page](https://clawhub.ai/xiaoke-bot/daily-to-goal-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON configuration examples and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DTG_API_KEY and a D2G account; available actions depend on account role and API key scopes.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
