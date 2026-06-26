# chess-coach

An OpenClaw skill that provides interactive chess coaching by monitoring Chess.com games and stats. It analyzes recent games according to the user's skill level and offers personalized, actionable advice.

## Features

- **Profile Tracking**: Connect any Chess.com username and track stats across formats (Blitz, Bullet, Rapid).
- **Recent Game Analysis**: Automatically identifies coaching opportunities in recent games.
- **Skill-Level Calibration**: Adjusts advice based on current rating (targeted and relevant feedback).
- **Daily Analysis Budget**: Designed to only analyze one "teachable moment" per day to manage costs.
- **Pattern Learning**: Accumulates observations over time to identify long-term habits and "Grand Lessons."

## Structure

```
chess-coach/
├── SKILL.md           # Core logic and instructions for OpenClaw
├── scripts/
│   └── chess_api.py   # Python script for Chess.com API interaction
└── references/
    └── skill_levels.md # Guidance on coaching priorities by rating bracket
```

## Setup for OpenClaw

To use this skill locally, place the `chess-coach` folder in your OpenClaw `skills/` directory.

## Contributing

We'd love help making the Chess Coach better! Areas for contribution:
- Improving the game analysis logic in `SKILL.md`.
- Expanding the `skill_levels.md` reference with more specific opening/endgame advice.
- Enhancing `chess_api.py` to fetch more detailed game data (like PGN move lists).

Created with ⚡ by Kael & Travis.
