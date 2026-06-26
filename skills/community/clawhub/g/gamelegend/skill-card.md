## Description: <br>
Game discovery and recommendations powered by GameLegend's Gameplay DNA engine for finding similar games, deciding what to play next, and exploring games by gameplay style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipLudington](https://clawhub.ai/user/PhilipLudington) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer game discovery questions, find titles similar to a named game, and recommend games based on gameplay feel and remembered preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Game searches and preference clues may be sent to GameLegend when the agent looks up recommendations. <br>
Mitigation: Use the skill only when comfortable sharing game-related interests with the public GameLegend API. <br>
Risk: Remembered likes and dislikes can personalize recommendations but may retain gaming preferences longer than intended. <br>
Mitigation: Tell the agent not to remember gaming preferences or clear its memory when personalization is not desired. <br>


## Reference(s): <br>
- [GameLegend](https://gamelegend.com) <br>
- [GameLegend API Documentation](https://gamelegend.com/docs/api) <br>
- [GameLegend MCP Server](https://www.npmjs.com/package/@gamelegend/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/PhilipLudington/gamelegend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Concise conversational Markdown with game recommendations, similarity scores, gameplay traits, and links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the public GameLegend API and use remembered gaming preferences to tailor future recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
