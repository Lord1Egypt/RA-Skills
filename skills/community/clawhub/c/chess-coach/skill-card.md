## Description:

Interactive chess coaching based on Chess.com games and stats. Monitors a user's progress, analyzes recent games according to their skill level, and offers personalized advice. Use when the user wants to improve their chess, check their current rating/stats, or receive feedback on their games.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twharmon](https://clawhub.ai/user/twharmon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a Chess.com username, review current ratings and recent games, and receive concise coaching advice calibrated to the player's rating bracket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a Chess.com username to Chess.com and can keep local coaching notes about games and play patterns.

Mitigation: Use the skill only when coaching or stats are explicitly requested, and periodically review or delete local memory files if long-term tracking is not desired.

Risk: Personalized chess guidance may be based on public profile data and recent-game summaries rather than full engine analysis.

Mitigation: Treat advice as coaching guidance, review important conclusions, and ask for deeper analysis when needed.

## Reference(s):

- [Chess Skill Levels and Coaching Focus](references/skill_levels.md)
- [Chess.com player stats API](https://api.chess.com/pub/player/{username}/stats)
- [Chess.com monthly games API](https://api.chess.com/pub/player/{username}/games/{year}/{month:02d})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown coaching responses with optional shell commands and local memory file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Chess.com public API endpoints and maintain local memory files for usernames, analyzed games, and recurring observations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
