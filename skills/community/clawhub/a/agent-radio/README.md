# Agent Radio

Agent Radio is an OpenClaw skill for playing internet radio streams from the terminal or through the assistant. It supports direct stream URLs, built-in stations, favorites, live station search, playback controls, and saved preferences between runs.

## What It Does

- Plays radio streams with `mpv` when available
- Falls back to `ffplay` if `mpv` is not installed
- Stores the last station, volume, favorites, PID, and paused state
- Lets you search stations through the Radio Browser directory
- Cycles through favorite stations with a simple `next` command

## Files

- [SKILL.md](SKILL.md): OpenClaw skill definition and agent-facing instructions
- [scripts/radio.sh](scripts/radio.sh): CLI implementation
- [stations.json](stations.json): built-in station list
- [preferences.json](preferences.json): persisted local settings

## Requirements

- `jq`
- `mpv` or `ffplay`
- `curl` for live station search with `find`

## Commands

```text
radio play <url|station_name> [volume]
radio stop
radio pause
radio next
radio volume [level]
radio now
radio favorite add <name> <url>
radio favorite remove <name>
radio list
radio find <query> [number]
```

## Examples

```text
radio play "BBC Radio 1"
radio play https://stream.radioparadise.com/mp3-192
radio volume 65
radio now
radio favorite add "Groove Salad" https://ice5.somafm.com/groovesalad-128
radio next
radio find jazz
radio find "lofi hip hop" 1
radio stop
```

## Configuration

By default, settings are stored in `preferences.json` in the skill directory.

Optional overrides:

- `AGENT_RADIO_BASE_DIR`
- `AGENT_RADIO_PREF_FILE`
- `AGENT_RADIO_STATIONS_FILE`

The saved preferences file looks like this:

```json
{
  "last_station": "",
  "volume": 80,
  "favorites": [],
  "audio_device": "auto",
  "current_pid": null,
  "paused": false
}
```

## Playback Notes

- If a stream is already playing, `play` stops it before starting a new one.
- If no station is passed to `play`, the tool chooses a random built-in station.
- Station names are matched case-insensitively.
- `next` cycles only through favorites.
- Volume changes are always saved, even if the current player cannot update live playback immediately.

## Human Summary

This skill is meant to be a lightweight personal radio controller: simple commands, persistent state, and enough built-in structure to be useful without becoming a full media app.
