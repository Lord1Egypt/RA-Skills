## Description:

Daily-to-Goal MCP connects an agent to the Daily-to-Goal platform through MCP so users can manage goals, tasks, entities, and team performance with a D2G account and API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoke-bot](https://clawhub.ai/user/xiaoke-bot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an assistant to Daily-to-Goal for listing, creating, updating, approving, and deleting goal, task, entity, and team-performance records. It is suited to users who already have a D2G account, API key, and role permissions for the requested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill configures an unpinned remote MCP package that uses a D2G API key.

Mitigation: Install only from a trusted package source, pin a reviewed package version, and keep DTG_API_KEY in environment variables or a secrets manager rather than committed config.

Risk: The connected tools can create, update, delete, approve, and otherwise change live Daily-to-Goal records.

Mitigation: Use a dedicated least-privilege API key and require explicit confirmation before delete, approve, or other state-changing actions.

## Reference(s):

- [Daily-to-Goal web application](https://h5.dd-up.com/)
- [ClawHub skill page](https://clawhub.ai/xiaoke-bot/skills/daily-to-goal-mcp)
- [Publisher profile](https://clawhub.ai/user/xiaoke-bot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON MCP configuration and text results from the configured server]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DTG_API_KEY and a configured MCP server; available actions depend on D2G role permissions and API key scopes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
