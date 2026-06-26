---
name: football-tracker
description: Track football teams and return last match, next match, kickoff time, broadcasters, standings, and recent news in a compact emoji-formatted summary.
---

# Football Tracker AI

Track football teams and the FIFA World Cup 2026 in a compact, emoji-friendly format.

This skill is bilingual:

- English is supported for instructions and output.
- Portuguese (pt-BR) remains supported for the existing Telegram style.
- The agent can force a locale with `locale=en`, `lang=en`, `locale=pt`, or `lang=pt`.

## Usage

- One team: `vasco`
- Multiple teams: `vasco, chelsea, bournemouth`
- Force English output: `locale=en Chelsea`
- Force Portuguese output: `locale=pt Chelsea`
- World Cup team by name only: `Brazil`
- World Cup team plus locale: `locale=pt Brazil`
- National teams from FIFA World Cup 2026 can be requested by name only, without API key, for example: `Brasil`, `Japão`, `Noruega`

## Expected output

For each team, return:

- team name
- last match
- next match
- when available, the next match venue prefixed with `🏟️`
- broadcasters / where-to-watch info for the next match when available
- competition
- standings
- recent news

For FIFA World Cup 2026 teams:

- team-name-only lookup should work for national teams the same way it works for clubs
- the internal 2026 schedule base is fully populated for all 104 matches, all 12 groups, all venue/date entries, and the knockout placeholders
- during the group stage, also show the group table for the selected team
- always keep the table/standings block before the news block
- keep the knockout path internal: round of 32, round of 16, quarter-finals, semi-finals, bronze final, and final
- use the internal 2026 schedule data first instead of re-searching the web for the fixed tournament structure
- when the output is pt-BR, localize World Cup team names to Portuguese
- show the next-match venue as state/city when the internal FIFA schedule has it; otherwise keep the venue line as unavailable instead of guessing

## Dependencies

- No extra Python packages are required.
- Uses only the Python standard library.
- Requires a valid `API_KEY` from `football-data.org` in `storage/user_config.json`.

## First Use

- If no API key is stored for the user, ask for `set_api_key SUA_KEY` only for club lookups.
- National teams from the FIFA World Cup 2026 must work without any API key prompt.
- Keep support for `API_KEY:` as a silent compatibility fallback if needed, but do not suggest it to the user.
- Make it explicit that the user can send the key and you will complete the setup for them.
- Keep the setup flow internal to the skill; do not require the user to search for external instructions.
- After the key is stored, continue with the normal team lookup flow.

## Notes

- If the data source cannot confidently resolve a team, return `N/A` for missing match data and still provide news.
- Keep the user-facing output in the requested locale and preserve the emoji-based layout.
- Always show kickoff time in the local timezone plus UTC.
- Always include the weekday in the kickoff timestamp.
- If a World Cup venue is available, show it on the next-match block with a `🏟️` prefix.
- If broadcaster data is unavailable, say so rather than guessing.
- News results should prefer recent, high-signal football reporting. Exclude previews, lineups, kickoff-time posts, where-to-watch articles, and generic hub pages.
- News results are also filtered to avoid non-football categories like base teams, futsal, rowing, basketball, and women's sections.
- Append a localized beta notice and the current version at the end of every result.
- For the World Cup 2026 build, show the kickoff embedded in the next-match line and do not print a separate kickoff field.
- This build focuses on bug fixes and discovery improvements.
- If timezone detection is unavailable, fall back to the machine/system timezone.

## Language packs

- `references/locales/en.md` for the English output pack
- `references/locales/pt-br.md` for the Portuguese output pack
