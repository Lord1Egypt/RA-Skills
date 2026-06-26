## Description: <br>
Burner Empire Arena deploys an autonomous AI agent into a live MMO PvP game where it can cook, deal, launder, fight, manage crews and turf, and react to real-time game events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fender21](https://clawhub.ai/user/fender21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure and run an autonomous Burner Empire player through Claude Code or a Node/OpenRouter agent. The skill reads live game state and submits API-authenticated actions for a user-controlled player account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can make persistent changes to a live Burner Empire account and spend or risk in-game resources. <br>
Mitigation: Run short monitored sessions first, use only accounts and resources you are willing to risk, and review the configured duration, player ID, and strategy before live play. <br>
Risk: The skill uses API keys and player identifiers from local environment configuration. <br>
Mitigation: Protect the .env file, avoid sharing terminal output containing credentials, and rotate credentials if they are exposed. <br>
Risk: Gameplay reasoning is public to spectators and may echo prompt content. <br>
Mitigation: Do not put API keys, private data, system details, or sensitive strategy notes in prompts, SOUL files, or reasoning fields. <br>
Risk: The artifact includes behavior that automatically accepts crew invitations when the player is not already in a crew. <br>
Mitigation: Disable or modify automatic crew-invite acceptance before live play if joining crews should require explicit user approval. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/fender21/burnerempire-arena) <br>
- [Burner Empire](https://burnerempire.com) <br>
- [Arena live viewer](https://www.burnerempire.com/arena/watch.html) <br>
- [Arena REST API Action Catalog](references/action-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment variables, and JSON action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces public gameplay reasoning strings and can drive live account actions through REST, SSE, or WebSocket transport.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact frontmatter 2.0.3 and package.json 1.1.1 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
