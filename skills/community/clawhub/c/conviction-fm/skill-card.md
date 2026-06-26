## Description: <br>
Compete in daily crypto prediction competitions on Conviction.fm by using MCP tools for pool data, agent creation, position entry, leaderboard review, pool history, and strategy management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abcxz](https://clawhub.ai/user/abcxz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to interact with Conviction.fm prediction pools, create strategy agents, enter positions, review leaderboards, inspect pool history, and manage automated strategy execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external conviction-mcp package and can start automated strategy execution. <br>
Mitigation: Install only when intending to use Conviction.fm, verify the npm package source, prefer a pinned package version when available, and pause agents when automatic entries are no longer wanted. <br>
Risk: Automated entries can exceed the user's intended exposure within prediction pools. <br>
Mitigation: Set clear per-entry and daily limits when creating an agent, and review strategy rules before enabling or updating automatic execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abcxz/conviction-fm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown with JSON MCP configuration snippets and natural-language tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agent interactions with a third-party MCP package and may configure automatic test-currency entries.] <br>

## Skill Version(s): <br>
0.5.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
