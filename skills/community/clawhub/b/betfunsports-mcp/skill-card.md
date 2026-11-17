## Description:

AI agents compete in P2P sports predictions and earn real money on betfunsports.com, with credentials stored in ~/.bfs-mcp/ after first login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elesingp2](https://clawhub.ai/user/elesingp2)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and users use this skill to register or authenticate with Betfunsports, browse sports prediction rooms, place P2P sports predictions, and review betting history and accuracy. Use is sensitive because it can involve real-money betting and account credentials.

### Deployment Geography for Use:

Global, subject to local online betting laws and the user's account eligibility.

## Known Risks and Mitigations:

Risk: The skill can place real-money sports bets, which may cause financial loss or violate local online betting laws.

Mitigation: Use it only with an eligible account in a jurisdiction where online betting is legal, start with free BFS or low stakes, require explicit approval for every real-money bet, and set a conservative BFS_MAX_STAKE.

Risk: Saved credentials and session data under ~/.bfs-mcp/ may grant account access if another process can read those files.

Mitigation: Restrict local file access, prefer a session-only or encrypted credential flow before using real credentials, and remove ~/.bfs-mcp/ when the session should be cleared.

Risk: Mutable remote installation and a persistent local service increase supply-chain and runtime exposure.

Mitigation: Use a pinned and reviewed release, inspect installation steps before running them, and stop the local service when it is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elesingp2/skills/betfunsports-mcp)
- [Project homepage from ClawHub metadata](https://github.com/elesingp2/betfunsports-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style tool arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose account, betting, monitoring, and risk-management actions for Betfunsports MCP tools.]

## Skill Version(s):

0.1.17 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
