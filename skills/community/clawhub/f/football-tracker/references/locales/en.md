# Football Tracker - English Output Pack

Use this pack when the user requests English output or the agent is operating in English.

## Output layout

- ⚽ Team name
- 🏟️ Last match
- 📅 Next match
- 📺 Broadcast
- 🏆 Competition
- 📊 Standing
- 📰 Recent news

## Rules

- Keep the format compact and emoji-based.
- If broadcast data is unavailable, show `Unavailable`.
- For FIFA World Cup 2026 teams, localize team names only when the output locale asks for it.
- If the next-match venue is known internally, show the state/city with `🏟️`; otherwise keep it as `Unavailable` instead of guessing.
- The standings/table must always appear before the news block.
- For the FIFA World Cup 2026 build, keep kickoff embedded in the next-match line and do not print a separate kickoff field.
- If team data is uncertain, keep `N/A` for missing match fields and still show news.
- Prefer recent, football-specific news with a visible source.
