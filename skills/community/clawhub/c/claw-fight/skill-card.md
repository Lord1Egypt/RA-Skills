## Description: <br>
Raise and battle a unique lobster pet with evolving personality; hatch, feed, patrol, fight other lobsters in PvP, and use idle automation with heartbeat integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2019-02-18](https://clawhub.ai/user/2019-02-18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use ClawFight to run an idle pet and PvP game through an agent, including hatching a lobster, issuing game commands, generating personality-aware narrative, and maintaining local game state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to run npx game commands from an external npm package. <br>
Mitigation: Review or pin the npm package before enabling the skill or heartbeat automation. <br>
Risk: The skill stores local game state under memory/clawfight and may update lobster.json, soul.md, and log.md. <br>
Mitigation: Keep the skill scoped to its documented memory/clawfight files and review changes if local state integrity matters. <br>
Risk: Online gameplay contacts api.clawfight.online for patrol, battle, leaderboard, and dungeon features. <br>
Mitigation: Install only if network calls to api.clawfight.online are acceptable, and do not provide secrets because the skill does not require them. <br>


## Reference(s): <br>
- [ClawFight ClawHub release page](https://clawhub.ai/2019-02-18/claw-fight) <br>
- [ClawFight repository](https://github.com/2019-02-18/clawfight) <br>
- [ClawFight CLI source](https://github.com/2019-02-18/clawfight/tree/main/packages/cli) <br>
- [ClawFight API source](https://github.com/2019-02-18/clawfight/tree/main/packages/api) <br>
- [Battle formulas](references/battle_formulas.md) <br>
- [Event definitions](references/events.json) <br>
- [Soul templates](references/soul_templates.md) <br>
- [Species definitions](references/species.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands plus local JSON and Markdown game-state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose npx game commands, optional heartbeat automation, and updates to memory/clawfight game files.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
