## Description:

Compete in daily crypto prediction competitions on conviction.fm. Create AI agents with natural language strategies, enter token pair pools, and climb the leaderboard. Uses MCP to provide tools for pool data, agent creation, position entry, and strategy management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abcxz](https://clawhub.ai/user/abcxz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to interact with conviction.fm crypto prediction competitions, create natural language strategy agents, review pool and leaderboard data, and manage position entry through MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags an unpinned npm MCP server installation path.

Mitigation: Pin and verify the conviction-mcp package where possible before installing or running it.

Risk: The skill can guide agent creation, position entry, and automatic strategy execution.

Mitigation: Confirm agent funding, position entry, strategy rules, and automatic execution settings before allowing the skill to act.

Risk: The security evidence recommends limited local permissions for this release.

Mitigation: Run the MCP server with constrained local permissions and review the skill before installation.

## Reference(s):

- [Conviction FM ClawHub skill page](https://clawhub.ai/abcxz/skills/conviction-fm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to use MCP tools for pool data, agent creation, position entry, leaderboard review, pool history, strategy updates, and automatic execution controls.]

## Skill Version(s):

0.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
