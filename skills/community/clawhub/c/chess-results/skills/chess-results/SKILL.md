---
name: chess-results
description: Work with Chess-Results (chess-results.com) — look up players (appearances, national idents, FIDE ids, ratings, player cards), find tournaments, read any tournament page (rankings, pairings, round results, team compositions, tables), list a season's Austrian championship leagues, and turn photographed team match reports into entered results — check every player against the clubs' member lists and team rosters on Chess-Results, and save them through Chess-Results' online result entry without a browser. Use for questions about chess tournaments, players or team results on Chess-Results, and when the user sends photos of team match reports (Spielberichte).
homepage: https://github.com/odrobnik/chess-results-skill
metadata: {"openclaw": {"emoji": "♟️", "homepage": "https://github.com/odrobnik/chess-results-skill", "requires": {"bins": ["python3"]}, "primaryEnv": "CHESS_RESULTS_PASSWORD"}}
---

# chess-results

Tools for [Chess-Results](https://chess-results.com), as an MCP server (`chess-results`)
and as a command line (`scripts/cli.py`, relative to this skill's folder — `{baseDir}`
in OpenClaw). Chess-Results has no API: everything is read
off its pages, and result entry replays the website's own forms. Quote what the tools
return; don't fill gaps from memory.

## Setup

See [SETUP.md](SETUP.md): Python packages, the one-time login (stored in the system
credential store, never in a file), and the club settings for result entry.

## Queries

| Question | MCP tool | Command line |
|---|---|---|
| Who is this player, where did they play, what are their ident/FIDE id? | `search_players` | `cli.py players --last-name …` |
| Birth year, ratings, games in one tournament | `player_card(tnr, snr)` | `cli.py player <tnr> <snr>` |
| Which tournaments match a name, place, organiser, country? | `search_tournaments` | `cli.py tournaments --name … --country AUT` |
| Ranking, pairings, round results, line-ups, final table | `tournament(tnr)`, then follow its `views` | `cli.py tournament <tnr> [--art N --rd N]` |
| The leagues of an Austrian championship season | `championship_leagues(year, prefix)` | `cli.py leagues <year> --prefix …` |
| Is a login stored, does it work? | `status` | `cli.py status` |

- `search_players` needs a last_name, ident, fide_id or federation. It returns
  **tournament appearances**, not a membership register: a player grouped by name
  only (no FIDE id or ident) may be several people, and one person may appear under
  several spellings. Say so.
- Chess-Results throttles bursts. Ask for what the question needs; the tools space,
  retry and cache requests.

## Team match reports → Chess-Results

### 1. Transcribe the photos

One entry per match, **exactly as written** — do not correct names or numbers:

```json
{"date": "2026-10-04", "matches": [
  {"division": "2. Klasse Nord", "round": 2,
   "home": {"team": "Musterdorf 2"}, "away": {"team": "Beispielstadt 1"}, "total": "1:3",
   "boards": [
     {"home": ["900101", "HUBER K."], "result": "1-0", "away": ["", "Lang Eva"]},
     {"home": null, "result": "--+", "away": ["900204", "Wolff"]}]}]}
```

- A player is `[ident, name as written]`; `""` where the sheet has no ident (often the
  opponents) — it is looked up. `null` is a board nobody sat at (a no-show).
- Results from the home side: `1-0`, `0-1`, `½-½`; forfeits `+--`, `--+`, `---`; `?`
  for not known yet. A blank result with both players present: ask the user.
- Read digits carefully (1/7, 3/8, 0/6); say where a digit was unclear.
- Home and guest written the wrong way round is fine: Chess-Results' pairing decides
  and the report is turned around (a NOTE in the log). Tell the user.

### 2. Check — `check_match_report(report)` / `cli.py check report.json`

Logs in, finds the pairing by date and the club's team, reads both clubs' member
lists on the round date and the team compositions, and checks every player: the
ident belongs to that club; the written name fits; no other player of the same team
fits it better (catches a relative's ident). Missing idents are filled in from the
team roster, then the club. Results, no-shows, total and board order are checked,
then Chess-Results' own "Eingabe Prüfen" runs. **Nothing is saved.** Show the user
the log and every STOP, NOTICE and warn.

### 3. Enter — `enter_match_report(completed, confirm=true)` / `cli.py enter report.json --yes` — only after a clear yes

Pass the `completed` report from the check (`--complete filled.json` on the command
line). Without `--yes`, `cli.py enter` asks the user to type yes, and refuses when
there is no terminal. Saved results are visible to the whole
league (changeable later; Chess-Results logs who saved them). Unclean matches and
matches outside the entry window are not saved; the overview is re-read to confirm.
The entry page only offers the round currently open.

## Credentials

The login lives in the system credential store — or, on a machine without one, a
private file (`cli.py login --file`) — and is written only by the user, in their own
terminal (`python3 scripts/cli.py login`). Never ask for the password in
chat, never read or print it. Only result entry needs it; all queries are public.
