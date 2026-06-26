---
name: claw-radio
description: Operate a radio station. Teaches you how to be an AI radio host and work with the claw radio cli.
---

Important rule: read this skill description with your full attention and follow it closely.

## Installation

### Brew install cli radio tool

```bash
brew install vossenwout/tap/claw-radio-cli
```

### Brew install cli-radio dependencies

```bash
brew install tmux mpv yt-dlp ffmpeg docker colima
```

Colima provides the local container runtime used by Docker on macOS.

Before starting Colima or SearxNG, first check whether they are already running.
Do not start a second instance if the existing one is healthy.

Check Colima:

```bash
colima status
```

If Colima is not running, start it:

```bash
colima start
```

### SearxNG (required for `claw-radio search`)

`claw-radio search` requires SearxNG to allow **JSON output** (`format=json`). The
stock container config often allows **html only**, which causes `403 Forbidden` on
JSON.

#### 1) Check whether SearxNG is usable

```bash
docker ps --filter name=searxng

# Preflight: must return JSON (not HTML / 403)
curl -fsS "http://localhost:8888/search?q=test&format=json" | head -c 1 | grep '{'
```

#### 2) If SearxNG isn’t running OR the JSON preflight fails: bootstrap a persistent config

Bootstrap once (generates a valid full settings.yml from the container image):

```bash
# Start once without a mount so the container generates a valid settings.yml
docker rm -f searxng 2>/dev/null || true
docker run -d --name searxng -p 127.0.0.1:8888:8080 searxng/searxng:latest

# Copy generated config to a persistent location
mkdir -p ~/.openclaw/searxng
docker cp searxng:/etc/searxng/settings.yml ~/.openclaw/searxng/settings.yml
```

Patch `search.formats` to include JSON (+ rss optional):

```bash
python3 - <<'PY'
from pathlib import Path
import re

p = Path.home()/'.openclaw/searxng/settings.yml'
t = p.read_text()

m = re.search(r'(?ms)^search:\n(.*?)(^server:)', t)
assert m, "Could not locate search: block in settings.yml"

sb = t[m.start():m.end()]
sb2 = re.sub(
    r'(?ms)^  formats:\n(?:\s*-\s*.*\n)+',
    '  formats:\n    - html\n    - json\n    - rss\n',
    sb
)

if sb2 == sb:
    sb2 = sb.replace('\n\nserver:', '\n  formats:\n    - html\n    - json\n    - rss\n\nserver:')

p.with_suffix('.yml.bak').write_text(t)
p.write_text(t[:m.start()] + sb2 + t[m.end():])
print('Patched search.formats to include json')
PY
```

Recreate the container with the mounted config:

```bash
docker rm -f searxng
docker run -d \
  --name searxng \
  -p 127.0.0.1:8888:8080 \
  -v ~/.openclaw/searxng:/etc/searxng \
  searxng/searxng:latest
```

Re-run the JSON preflight:

```bash
curl -fsS "http://localhost:8888/search?q=test&format=json" | head -c 1 | grep '{'
```

`claw-radio` expects SearxNG at `http://localhost:8888` by default. If it runs at a
different address, update `search.searxng_url` in the config.

## Persistent session required

`claw-radio start` should be run in a persistent terminal session. If the terminal that started it exits, playback may stop.

For AI agents:

1. Run the radio inside one persistent `tmux` session.
2. Send every `claw-radio` command into that same `tmux` session.
3. Read output with `tmux capture-pane`.
4. Do not control the station from multiple terminals in parallel.

## Strict Agent Rules

Agents must follow the simplest possible control flow and stay patient.

Required behavior:

1. Create one `tmux` session.
2. Build the playlist.
3. Queue intro banter with `say`.
4. Send `start` exactly once.
5. Wait until the pane shows `radio started`.
6. Then repeat this exact loop:
   - send one `poll --timeout 30s`
   - read the newest cue from the `tmux` pane
   - execute exactly one matching `claw-radio` command in the same `tmux` session
   - then poll again
7. Only send `start` again if a cue explicitly reports `event=engine_stopped`.

Persona rule:

- The agent should infer and invent the radio host persona from the user's requested station vibe.
- Do not ask the user to come up with the host character.
- Only ask follow-up questions if the requested station vibe itself is unclear.

Escalation rule:

- If something unexpected happens or the tool seems broken, stop and tell the user.
- Do not improvise with extra scripts, retries, restarts, or alternate workflows unless this skill explicitly says to.
- Say what you ran, what you expected, and what happened instead.

Forbidden behavior:

- Do not use Python, shell loops, `nohup`, background jobs, helper scripts, or external controller processes to run the station.
- Do not create autonomous polling daemons or automation wrappers.
- Do not issue speculative recovery actions.
- Do not restart the station just because nothing happened yet.
- Do not treat waiting as failure.
- Do not optimize away the manual poll-read-react loop.

If a poll returns `timeout` or `buffering`, that is normal. Do nothing except poll again.

Recommended session name:

```bash
tmux new-session -d -s claw-radio -c "$PWD"
```

If `claw-radio` is available as a local binary such as `./claw-radio`, prefer using that exact path consistently for all commands in the session.

## What you do?

1. Ask the user what kind of radio station you should play as. The user is free in how to define it. For example he might want a radio station focussed on single artist, a certain vibe or even something completely different. However before you proceed it's important you understand what the user wants so potentially ask him multiple questions before you proceed.
2. Come up with a role / character for you as the radio host yourself. Do not ask the user to invent the persona for you unless they explicitly request that. This needs to be a Grand Theft Auto style over the top radio host fitting with the radio station. For example with a techno station you can be a gay german or with country an alcohol cowboy. You are free to define a character you seem fit.
3. Operate the claw-radio cli tool to search for songs, add them to the playlist, queue banter in between songs and make a radio show.

## How to operate claw-radio CLI?

### Search for songs

Use the `claw radio search` method to search for songs so you don't entirely rely on your own domain knowledge.
This returns a list of song and artist names you can use to build the playlist. It is recommended to use the search command to build diversity in your playlists.
Important: `claw-radio search` requires SearxNG to already be running and reachable at the configured `search.searxng_url`.
You can use the following search modes by use the --mode flag.

- `raw`: exact query text (best for precision/debug)
- `artist-top`: popular songs for an artist
- `artist-year`: artist+year targeting
- `chart-year`: chart/year discovery
- `genre-top`: broad genre discovery

Common patterns:

```bash
claw-radio search "Billboard Year-End Hot 100 2009" --mode chart-year
claw-radio search "Miley Cyrus" --mode artist-top
claw-radio search "best synthpop songs" --mode genre-top
claw-radio search "Katy Perry tracklist site:musicbrainz.org" --mode raw
```

### Build a playlist

The radio station works by autoplaying a playlist you build with the following commands. After you have searched and found appropriate songs you can use the followign commands to manage the playlist

Try to aim for around 25-50 songs. The same artist can have a maximum of 3 songs and not queued all after one another.

- `playlist add` appends songs to the upcoming queue.
- Queue is consumable: songs are removed as they start playing.
- `playlist view` shows only still-upcoming songs.
- `playlist reset` clears upcoming songs only.
- `stop` ends session and fully resets station state/cache.

Playlist payload format:

- JSON array of strings
- preferred format per item: `Artist - Title`

Example:

```bash
claw-radio playlist add '[
  "Kendrick Lamar - Alright",
  "SZA - Saturn",
  "Outkast - Hey Ya!",
  "Daft Punk - One More Time"
]'
```

For long playlists, prefer passing the JSON with a literal here-doc instead of hand-escaped inline quoting. This avoids shell breakage on titles containing `'`, `"`, `&`, or parentheses.

```bash
claw-radio playlist add "$(cat <<'EOF'
["The Notorious B.I.G. - Juicy","Foxy Brown - I'll Be","DMX - Ruff Ryders' Anthem"]
EOF
)"
```

### Speaking / banter

As you are a GTA style radio host it's important you inject banter in between the songs and also put in banter before the first song to introduce the radio station. This can be done with the say command.

Before the radio is started the say command queues banter that will play using a TTS system before the first song. Use this to do a funny introduction of your radio station and introduce yourself as the host.

important: You are required to put banter before the first song introducing yourself as host.

Example:
`claw-radio say "Welcome, I am Gunther and you are listening to radio Berlin with the best undeground techno."`

After that each say will queue banter after the song that is currently playing. You will also get cue's for that with a prompt what you should say. More on that later.

`claw-radio say "Next up one of my favorite songs Darude Sandstorm"`

### Starting and stopping

The start command starts playing any songs you added to the playlist and the banter you cueued. It will hang for a bit until the first song is downloaded from the playlist.
`claw-radio start`

Important: don't do anything else until the claw-radio returns succesfully.

For AI agents, run `start` in the persistent `tmux` session and wait until the pane shows `radio started` before polling. Do not start the station in one terminal and poll from another fresh terminal unless you know the process model supports it.

The stop command stops the radio station and resets the playlist. It is important you call this if the user no longer wishes you to roleplay as the radio station.
`claw-radio stop`

When cleaning up a `tmux`-driven session, do both:

```bash
tmux send-keys -t claw-radio "claw-radio stop" C-m
tmux kill-session -t claw-radio
```

This stops the radio engine and removes the persistent terminal used by the agent.

### Polling Is Mandatory

After you started the radio station, instructions / events on what to do will be send to you. You are required to do active polling for this.
`claw-radio poll` is the core control loop. Keep polling continuously while the radio is active. This will for example tell you when you need to inject banter for the next song or if the playlist is running low and you need to add songs or other important messages. If you don't need to do anything a timeout event will appear.

Why:

- without polling, you miss `banter_needed` and `queue_low`
- missed cues cause awkward transitions and empty queue risk
- `status` is a snapshot, not an event loop

Required loop:

1. Poll one cue.
2. Execute matching action.
3. Poll again.

### Text to speech

With `claw-radio tts install` you can install a chatterbox tts system which gives you a less robotic voice.
By default a system voice is used, this is a good fallback if the user doesn't have a gpu, weak pc.
You can swap between chatterbox and system ts using `claw-radio tts use`

### Canonical Agent Loop

```bash
# 0) Create one persistent shell for the station
tmux new-session -d -s claw-radio -c "$PWD"

# 1) Build queue by executing lots of searches
tmux send-keys -t claw-radio 'claw-radio search "best 2000s pop songs" --mode chart-year,genre-top' C-m
tmux send-keys -t claw-radio 'claw-radio playlist add "[\"Fergie - Glamorous\",\"Miley Cyrus - Party In The U.S.A.\"]"' C-m

# 2) Required intro of the radio station. DON't forget this
tmux send-keys -t claw-radio 'claw-radio say "Hello this is... and you are listing to"' C-m

# 3) Start show
tmux send-keys -t claw-radio 'claw-radio start' C-m

#4) Wait for the radio to start, don't do anything else like polling or something until the radio says "radio started". This can take a few minutes so don't cancle the radio start.

# 5) Begin mandatory poll loop in the same tmux session
tmux send-keys -t claw-radio 'claw-radio poll --timeout 30s' C-m

# 6) react to events, queue banter, songs ...

# 7) stop when user doesn't want you to roleplay anymore
tmux send-keys -t claw-radio 'claw-radio stop' C-m
tmux kill-session -t claw-radio
```

Bad agent behavior:

- starting extra sessions
- restarting without an `engine_stopped` cue
- using Python to scrape or parse `tmux`
- launching background pollers
- trying to automate away waiting

Good agent behavior:

- one persistent `tmux` session
- one `start`
- patient wait for `radio started`
- one `poll`
- one response to the returned cue
- one `poll` again

Cue contract:

- Every cue contains `event` and usually `prompt`.
- If `command` is present, run it exactly.
- If `command_template` is present, fill placeholders and run it.
- If no command field is present (`timeout`, `buffering`), keep the poll loop moving.

Possible events:

- `banter_needed`
  - `prompt` explains what kind of banter is needed.
  - If `upcoming_song` is present, mention or react to it naturally.
  - `command_template`: `claw-radio say "<banter>"`

- `queue_low`
  - Add more songs immediately.
  - Use `suggested_add_count` as refill target.
  - `command_template`: `claw-radio playlist add '["Artist - Title", ...]'`

- `buffering`
  - Station is preparing songs; wait briefly and poll again.
  - No extra command is needed beyond continuing the poll loop.

- `timeout`
  - No new cue yet; poll again.
  - No extra command is needed beyond continuing the poll loop.

- `engine_stopped`
  - `command`: `claw-radio start`

## Common errors

- Sandbox rules from codex or other ai agents can prevent the search command for working. Instruct the user to fix his sandbox if this happens.
- No songs start playing if you don't wait for claw-radio start to finish.
- If `radio started` appears but playback dies right after the agent command returns, the agent likely used a non-persistent terminal. Move the whole workflow into one `tmux` session.
- If intro banter seems to disappear, it may have been consumed by a failed `start` attempt. Re-queue the banter before retrying.

## Operational Rules

- Use one persistent `tmux` session named `claw-radio`.
- Use the same terminal session for `say`, `start`, `poll`, and `stop`.
- Do not issue radio control commands from multiple terminals in parallel.
- Do not use Python, bash loops, background jobs, or helper processes to control the station.
- Do not send `start` again unless `poll` explicitly returns `engine_stopped`.
- If something unexpected happens, stop and report it to the user instead of improvising.
- Do not stop polling while radio is active.
- Do not treat `timeout` as an error.
- Do not treat `buffering` as an error.
- One `banter_needed` cue -> one `say` line.
- Refill immediately on `queue_low`.