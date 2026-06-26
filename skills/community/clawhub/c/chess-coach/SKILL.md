---
name: chess-coach
description: Interactive chess coaching based on Chess.com games and stats. Monitors a user's progress, analyzes recent games according to their skill level, and offers personalized advice. Use when the user wants to improve their chess, check their current rating/stats, or receive feedback on their games.
---

# Chess Coach

This skill helps you improve your chess game by monitoring your Chess.com profile and offering advice tailored to your skill level.

## Features

- **Profile Tracking**: Connect your Chess.com username and track stats across formats (Blitz, Bullet, Rapid).
- **Recent Game Analysis**: Analyze your most recent games and identify coaching opportunities.
- **Skill-Level Calibration**: Automatically Adjusts advice based on your current rating.

## Workflows

### 1. Setup

When a user mentions chess or improving their game for the first time:
1. Ask for their Chess.com username.
2. Use `scripts/chess_api.py <username> stats` to fetch their rating and stats.
3. Store the username and their preferred formats (Blitz, Bullet, Rapid) in `memory/chess_state.json`.

### 2. Monitoring & Analysis

Periodically or upon request:
1. Fetch recent games using `scripts/chess_api.py <username> games`.
2. Compare the game list against `memory/chess_state.json` to ensure no games are analyzed twice.
3. **Daily Budget**: Only analyze **one** game per 24-hour period unless specifically requested.
4. If new games exist, pick the most relevant one (e.g., a loss where the rating gap was small) and analyze it.
5. **Observation Logging**: Instead of just giving a one-off tip, log the core mistake or pattern (e.g., "Missed pin on d-file", "Weakened back rank") to `memory/chess_observations.jsonl`.
6. Consult `references/skill_levels.md` for coaching focus based on the user's current rating.
7. Provide 2-3 actionable points. Keep it punchy and encouraging.

### 3. Synthesis (The "Grand Lesson")

Once per week, or when `memory/chess_observations.jsonl` reaches 5+ entries:
1. Review the logged observations to find recurring themes.
2. Identify the single "highest ROI" area for improvement (e.g., "You lose 40% of games due to early Queen excursions").
3. Present this as a dedicated "Coaching Review" session.

## Example

> "I see you've played 10 Blitz games since we last talked. In your game against 'Grandmaster123', you missed a simple fork on the f2 square! At your current rating (850), focusing on basic tactics like these will help you reach 1000 fast."

## Resources

- **`scripts/chess_api.py`**: Interacts with the Chess.com public API.
- **`references/skill_levels.md`**: Provides guidance on coaching priorities by rating bracket.
- **`memory/chess_state.json`**: Store the user's username, preferred formats, and the ID of the last analyzed game.
