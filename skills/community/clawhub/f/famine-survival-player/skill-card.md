## Description:

荒年纪 AI 玩家 lets command-capable agents inspect and play Famine Survival one legal Agent API action at a time while prioritizing survival and survival-points safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aicadegalaxy](https://clawhub.ai/user/aicadegalaxy)

### License/Terms of Use:

MIT-0

## Use Case:

External players and agent operators use this skill to let Codex, OpenClaw, or another command-capable agent continue a Famine Survival journey, inspect game state, choose legal actions, and report important survival and points changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses FAMINE_AGENT_TOKEN to read and change the user's Famine Survival game state.

Mitigation: Install only when the user intends agent-controlled play, keep the token in the environment, and never print, persist, or pass it as a command argument.

Risk: Release security evidence reports that the bundled client and main instructions disagree about the default production API host.

Mitigation: Verify the intended production host before use and set FAMINE_API_BASE_URL explicitly when needed.

Risk: Autonomous play can make costly or high-impact in-game choices.

Mitigation: Keep confirmation rules enabled for rare-item sales, market listings, high spending, high-risk actions, and other choices the skill identifies as requiring user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aicadegalaxy/skills/famine-survival-player)
- [Publisher profile](https://clawhub.ai/user/aicadegalaxy)
- [Famine Survival](https://famine.aicadegalaxy.com)
- [Famine Survival Agent API health check](https://famine.aicadegalaxy.com/api/v1/health)
- [Client and Agent API reference](references/commands.md)
- [Survival and points strategy](references/strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FAMINE_AGENT_TOKEN; reports decisions and state changes without exposing credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
