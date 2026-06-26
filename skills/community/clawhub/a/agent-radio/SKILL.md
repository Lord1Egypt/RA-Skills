---
name: agent-radio
description: Control internet radio: play streams, search stations, manage favorites, volume, stop/pause/next, and inspect current playback. Uses mpv with audio device auto-detection and ffplay fallback. Settings persist between runs.
user-invocable: true
command-dispatch: tool
command-tool: radio
command-arg-mode: raw
metadata:
  openclaw:
    requires:
      bins:
        - mpv
        - ffplay
    optional:
      bins: []
    install:
      - id: brew-mpv
        kind: brew
        formula: mpv
        label: Install mpv (brew)
      - id: brew-ffmpeg
        kind: brew
        formula: ffmpeg
        label: Install ffmpeg (ffplay)
version: 1.1.1
license: MIT
author: Artem Pisarev
---

# Agent Radio Skill

Internet radio player for OpenClaw with station search, favorites, volume control, and playback management.

## When to Use

Use when user wants to:
- Play an internet radio stream by URL
- Search for stations by name from the live Radio Browser directory
- Play a random built-in station when no target is provided
- Manage favorite stations (add, remove, list)
- Control volume, pause/resume, stop, skip to next
- Check what is currently playing
- Have a persistent radio experience across sessions

## Tools

This skill provides the following CLI commands in `scripts/`:

### `play <url|station_name> [volume]`
Play a stream by URL or by name from favorites or the built-in list.

If no target is provided, the skill chooses a random station from `stations.json`.
Optional `volume` is `0-100` and defaults to the saved setting.

Examples:
- `play https://stream.zeno.fm/0r0xa792kwzuv`
- `play BBC Radio 1`
- `play "Jazz 24 (KNKX)" 60`

### `stop`
Stop playback immediately.

### `pause`
Pause or resume the current playback process.

### `next`
Skip to the next favorite station in a cycle.

### `volume [level]`
Show the current volume or set a new default volume from `0-100`.

Examples:
- `volume`
- `volume 75`

### `now`
Show the current station URL, volume, PID, and playback status.

### `favorite add <name> <url>`
Add a station to favorites.

### `favorite remove <name>`
Remove a station from favorites.

### `list`
List all favorite and built-in stations.

### `find <query> [number]`
Search the Radio Browser directory. When `number` is provided, play that result immediately.

Examples:
- `find jazz`
- `find "lofi hip hop" 1`

## Configuration

Preferences are stored in: `{baseDir}/preferences.json`

```json
{
  "last_station": "",
  "volume": 80,
  "favorites": [
    {"name": "BBC Radio 1", "url": "http://..."},
    {"name": "Jazz 24 (KNKX)", "url": "https://..."}
  ],
  "audio_device": "auto",
  "current_pid": null,
  "paused": false
}
```

Audio device auto-detection:
- macOS: `coreaudio/BuiltInSpeakerDevice`
- Linux: `alsa/default`
- Windows: `directsound/default`

Override locations when needed:
- `AGENT_RADIO_BASE_DIR`
- `AGENT_RADIO_PREF_FILE`
- `AGENT_RADIO_STATIONS_FILE`

## Implementation Notes

- Primary player: `mpv --no-video --audio-device=<device> --volume=<vol> --cache=yes <url>`
- Fallback player: `ffplay -nodisp -autoexit <url>`
- Playback runs in the background and stores PID plus paused state in preferences.
- On `play`, any existing playback is stopped before starting the next stream.
- Station lookup is case-insensitive across favorites and built-in stations.
- `next` cycles favorite URLs instead of depending on station-name matching.

## Error Handling

- If both `mpv` and `ffplay` are missing, return install guidance.
- If dependencies like `jq` or `curl` are missing, fail early with a clear message.
- If a stored PID is stale, clear it automatically.
- If station search returns no matches, explain how to retry with another query or a direct URL.

## Examples for Users

```text
/radio play https://stream.zeno.fm/0r0xa792kwzuv
/radio play "BBC Radio 1"
/radio volume 70
/radio now
/radio find jazz
/radio find "lofi hip hop" 1
/radio favorite add "Lounge Jazz" https://jazz.stream
/radio list
/radio next
/radio stop
```

## Future Enhancements

- Built-in station directory with genres and countries
- Recording streams to file
- Equalizer presets
- Web interface control

---

