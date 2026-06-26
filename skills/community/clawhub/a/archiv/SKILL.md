
---
name: roon
description: >
  Controls your Roon music system — searching the library and TIDAL, playing
  tracks, queuing playlists, adjusting volume, skipping tracks, and answering
  questions about the music library. Use this skill any time the user mentions
  Roon, wants to play music, create a playlist, control playback, adjust volume,
  skip a track, asks what's playing, or wants music recommendations based on
  their library. Trigger even for casual requests like "put something on",
  "skip this", "turn it up", or "play something relaxing" — this skill has
  full knowledge of your zones, library, and the API needed to act immediately.
---

# Roon Music Controller

Your Roon system is controlled via a REST API running in LCX container on Proxmox server.

## API Base

```
http://roonext2.home:3001/api
```

## CRITICAL: How to make API calls

**GET:**
```bash
curl -s 'http://roonext2.home:3001/api/status'
```

**POST:**
```bash
curl -X POST http://roonext2.home:3001/api/find-and-play \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": "YOUR_ZONE_ID",
    "query": "stool pigeon",
    "type": "Tracks",
    "action": "Play Now"
  }'
```

---

## Zones

Replace this table with your own zones. Get them by calling `/api/zones`.

| Zone | ID |
|------|----|
| Schlafzimmer| `1601dcef8115529daf4cd6807753971fae3e` |
| Wohnzimmer| `160124b4c2dcc52aa8478e05110f7ed25120` |

**How to find your zone IDs:**
```bash
curl -s 'http://roonext2.home:3001/api/zones'
```

---

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/status` | All zones, playback state, now playing |
| GET | `/api/zones` | Zone list with IDs |
| GET | `/api/search?q=<query>[&type=Tracks\|Albums\|Artists]` | Search library + TIDAL |
| POST | `/api/find-and-play` | **Main play endpoint** — search + play in one session |
| POST | `/api/transport` | Playback control (play/pause/skip etc.) |
| POST | `/api/volume` | Volume control |
| GET | `/api/queue/<zone_id>` | View current queue |
| POST | `/api/playlist` | Queue multiple tracks in order (save as playlist in Roon app) |
| GET | `/api/inspect?q=<query>` | Debug: show Roon's exact action names for a track |
| POST | `/api/shuffle` | Enable or disable shuffle for a zone |
| POST | `/api/play-album` | **Play an entire album** — natively queues all tracks in order |

---

## play-album (album playback)

**Use this endpoint when the user asks to play an album.** Do NOT use `find-and-play` for albums — it only plays the first track.

```json
{ "zone_id": "...", "query": "Artist Album", "action": "Play Now" }
```

Searches for the album, navigates Roon's full browse hierarchy (Search → Albums → Album page → Play Album → action), and triggers album-level playback. All tracks are queued natively in the correct album order.

Supports the same action strings: `Play Now`, `Queue`, `Add Next`, `Start Radio`.

```bash
curl -X POST http://roonext2.home:3001/api/play-album \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": "YOUR_ZONE_ID",
    "query": "white city a novel",
    "action": "Play Now"
  }'
```

---

## find-and-play (single track playback)

```json
{ "zone_id": "...", "query": "...", "type": "Tracks", "action": "Play Now" }
```

### CRITICAL — Roon's exact action labels

These are the real strings Roon uses internally. Wrong names silently fall back to Play Now.

| Want to... | Use this string |
|------------|----------------|
| Play immediately (clears queue) | `Play Now` |
| Add to end of queue | `Queue` ← **NOT** "Add to Queue" |
| Play after current track | `Add Next` ← **NOT** "Play Next" |
| Start Roon Radio | `Start Radio` |

---

## transport

```json
{ "zone_id": "...", "action": "next" }
```

Valid actions: `play`, `pause`, `stop`, `next`, `previous`, `toggle_play_pause`

---


---

## shuffle

```json
{ "zone_id": "...", "shuffle": true }
```

Set `shuffle` to `true` to enable, `false` to disable.

```bash
curl -s -X POST http://roonext2.home3001/api/shuffle \
  -H 'Content-Type: application/json' \
  -d '{"zone_id": "1601dcef8115529daf4cd6807753971fae3e", "shuffle": true}'
```

## volume

```json
{ "zone_id": "...", "how": "absolute", "value": 40 }
```

Range 0–100. `how`: `absolute`, `relative`, `relative_step`

---

## Playlist pattern

### Option A — /api/playlist (recommended for multi-track lists)

Queues all tracks in one API call. First track plays immediately, rest are queued.
To save as a permanent Roon playlist: **Queue → ⋮ → Save Queue as Playlist**.

> **Note:** Roon's Extension API does not expose "Add to Playlist" to third-party
> extensions — only playback actions are available. The queue-then-save workflow
> is the supported path.

```json
POST /api/playlist
{
  "name": "My 1988 Mix",
  "zone_id": "YOUR_ZONE_ID",
  "tracks": [
    { "query": "Song One Artist One" },
    { "query": "Song Two Artist Two" },
    { "query": "Song Three Artist Three" }
  ]
}
```

```bash
curl -s -X POST http://roonext2.home:3001/api/playlist \
  -H 'Content-Type: application/json' \
  -d '{"name":"My Playlist","zone_id":"YOUR_ZONE_ID","tracks":[{"query":"Song One Artist"},{"query":"Song Two Artist"}]}'
```

### Option B — individual find-and-play calls (for short lists or fine control)

First track → `Play Now` (starts playback, clears existing queue).
All subsequent tracks → `Queue`. Use `delay 2` between calls.

```bash
ZONE="YOUR_ZONE_ID"
API="http://roonext2.home:3001/api/find-and-play"

tracks=(
  "Song One Artist One|Play Now"
  "Song Two Artist Two|Queue"
  "Song Three Artist Three|Queue"
)

for track in "${tracks[@]}"; do
  query="${track%%|*}"
  action="${track##*|}"
  curl -s -X POST "$API" \
    -H 'Content-Type: application/json' \
    -d "{\"zone_id\":\"$ZONE\",\"query\":\"$query\",\"type\":\"Tracks\",\"action\":\"$action\"}"
  sleep 2
done
```

---

## Your library and taste profile

Edit this section to describe your own library and musical taste. Cowork uses
this to make smart recommendations and playlist choices on your behalf.

```
YOUR_STREAMING_SERVICE is connected — any track can be played.

Local library includes:
- Artist — albums

Taste profile: describe your taste here so Cowork can recommend music you'll enjoy.
```

---

## Roon authorisation

If the API returns `"Not connected to Roon Core"`, you need to re-authorise:

Roon → Settings → Extensions → Enable **"Cowork Controller"**

## Learnings

* **verify.artist_match** – check that the artist of a track or album matches the requested artist before adding to the queue. This prevents mismatches like Bobbi Humphrey for a Commodores request.
* Embedding future learnings here ensures they are only loaded when the roon‑controller skill is used.



