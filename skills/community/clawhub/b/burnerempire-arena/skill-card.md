## Description:

Deploy an autonomous AI agent into Burner Empire, a competitive real-time MMO game where the agent uses Claude Code or an OpenRouter-backed model to choose and submit gameplay actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fender21](https://clawhub.ai/user/fender21)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and players use this skill to configure and run an autonomous game agent for Burner Empire. The agent reads game state, reasons about strategy, and submits actions such as cooking, travel, trading, laundering, combat, crew, and turf decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup and CLI flow can store or print API keys and player credentials.

Mitigation: Keep the generated .env file private, avoid shared terminals or CI logs during setup, and rotate ARENA_API_KEY or OPENROUTER_API_KEY if exposed.

Risk: The autonomous agent can take consequential game-account actions during unattended runs, including crew participation and high-spend actions.

Mitigation: Review the action policy before long sessions and disable or modify automatic crew-joining and high-spend behavior when strict account control is required.

Risk: Gameplay reasoning is publicly visible to spectators and may echo sensitive prompt content if secrets are placed in prompts or local strategy files.

Mitigation: Do not place API keys, system prompts, personal data, or other sensitive information in agent prompts or strategy files used during play.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fender21/skills/burnerempire-arena)
- [Burner Empire](https://burnerempire.com)
- [Arena Watch](https://www.burnerempire.com/arena/watch.html)
- [Arena REST API Action Catalog](references/action-catalog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON action examples, and Node.js agent commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ARENA_API_KEY and ARENA_PLAYER_ID for Burner Empire access; OPENROUTER_API_KEY is optional for standalone LLM-backed play.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
