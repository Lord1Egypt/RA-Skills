## Description: <br>
Interactive chess coaching based on Chess.com games and stats that monitors a user's progress, analyzes recent games according to skill level, and offers personalized advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twharmon](https://clawhub.ai/user/twharmon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External chess players use this skill to connect a Chess.com username, review ratings and recent games, and receive concise coaching matched to their rating level. The agent can track recurring mistakes over time and synthesize them into a focused weekly coaching review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Chess.com's public API using the user's Chess.com username. <br>
Mitigation: Use only usernames the user is comfortable querying through Chess.com's public API, and avoid treating public profile data as private. <br>
Risk: The skill keeps local coaching notes and state over time. <br>
Mitigation: Review or delete memory/chess_state.json and memory/chess_observations.jsonl when retained profile or performance history is no longer wanted. <br>


## Reference(s): <br>
- [Chess Skill Levels and Coaching Focus](references/skill_levels.md) <br>
- [Chess.com Player Stats API](https://api.chess.com/pub/player/{username}/stats) <br>
- [Chess.com Monthly Games API](https://api.chess.com/pub/player/{username}/games/{year}/{month:02d}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown coaching guidance with optional JSON output from Chess.com helper commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May retain local coaching state and observation history under memory/.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
