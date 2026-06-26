---
version: "1.0.0"
name: bumblebee
description: "Two modes: (1) BUMBLEBEE — Communicate through music by playing exact lyric lines on Spotify, like Bumblebee from Transformers speaking through radio snippets. (2) R2-DJ — Contextual music curation that reads the moment (time, mood, recent listening, activity) and builds the perfect queue. Use when: expressing something through song lyrics, playing music for the current vibe, curating a playlist for a mood/activity, responding to 'play music' or 'what should I listen to', DJ requests, or any music playback control (play, pause, skip, volume, search). Requires: Spotify Premium with active device, OAuth tokens in projects/spotify/."
---

# Bumblebee + R2-DJ — Talk Through Music & Curate the Vibe 🐝🎧

# Bumblebee + R2-DJ — Talk Through Music & Curate the Vibe 🐝🎧

Two sides of the same coin:
- **Bumblebee** speaks through exact lyric clips — chaining song lines into sentences
- **R2-DJ** reads the room and curates the perfect queue for the moment

## Prerequisites

- Spotify Premium account with an active device (phone, desktop, speaker)
- OAuth tokens at `projects/spotify/tokens.json` (auto-refreshes)
- Spotify app credentials at `projects/spotify/.env` (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`)
- **Your own lyric index** — see `scripts/build-lyric-index.md` for how to build one. Lyrics are copyrighted and not included in this skill. You'll need to curate your own `lyric-index.json` and optionally `lyrics-db.json`.

## Core Workflow

### 1. Find the Right Lyrics

Search the lyric index for lines that literally say what you mean:

```bash
node scripts/lyric-engine.js search "phrase to find"
```

Returns matching lines with IDs, timestamps, and scores. **Use literal phrases** — search for what the lyrics actually say, not metaphors.

### 2. Play Lyric Clips

Send specific lyric lines to the active Spotify device:

```bash
node scripts/lyric-engine.js speak "artist::track::lineNum" "artist::track::lineNum"
```

Each clip plays its exact timestamp window, then advances to the next with a brief pause. Chain multiple IDs to build a sentence.

### 3. Check Devices

```bash
node scripts/bumblebee.js devices
```

Verify an active Spotify device exists before attempting playback. 🟢 = active.

## Composing Messages — The Art of Speaking Through Music

Bumblebee doesn't paraphrase — it finds lyrics that **literally say the words**. The goal is chaining real song lines into a coherent sentence or feeling that the listener can understand.

### Auto-Compose (Recommended)

Give the engine a message and it finds the best lyric chain:

```bash
node scripts/lyric-engine.js compose "I miss you and I want to see you"
```

Returns a chain of clips with a ready-to-use `speak` command. The engine uses greedy phrase-matching: longest matching phrase first, then fills gaps.

### Manual Composition (Agent-Driven)

For more nuanced messages, the agent should:

1. **Rephrase the feeling as literal words someone would sing.** "Tell her I love her" → search for "te quiero", "I love you", "eres lo que más quiero"
2. **Search for 2-4 key phrases** that build the message:
   ```bash
   node scripts/lyric-engine.js search "I need you"
   node scripts/lyric-engine.js search "come back"
   node scripts/lyric-engine.js search "I'll be waiting"
   ```
3. **Pick the best line from each search** — prefer lines where the matching phrase IS the whole line (not buried in a long verse)
4. **Chain them into a speak command:**
   ```bash
   node scripts/lyric-engine.js speak "artist::track::3" "artist::track::12" "artist::track::7"
   ```

### Composition Rules

- **Literal over metaphorical.** Search for the actual words, not the feeling. "I'm sorry" → search "I'm sorry", not "regret".
- **Shorter lines > longer lines.** A 5-word lyric that matches perfectly beats a 20-word verse where 3 words match.
- **Variety across songs.** Don't chain 3 clips from the same song — it sounds like you're just playing the song. Mix artists.
- **Build an arc.** Setup → core message → punctuation. Like a sentence: subject, verb, exclamation.
- **2-4 clips is the sweet spot.** 1 clip = too simple. 5+ = loses the listener.
- **Present it.** After playing, show the listener what was said — the lyric text, the song, and optionally a translation if bilingual.
- **Hidden messages work too.** You can spell out a name, an acronym, or a secret message by picking lines whose first words chain together.

## Managing the Library

- **Add a song:** `node scripts/lyric-engine.js index "Artist" "Track"`
- **Batch-index starter library:** `node scripts/lyric-engine.js batch-index`
- **View all indexed songs:** `node scripts/lyric-engine.js catalog`
- **Song details and moods:** See [references/song-library.md](references/song-library.md)

## Intent-Based Playback (Legacy)

The original `bumblebee.js` supports mood-based playback from a curated clips database:

```bash
node scripts/bumblebee.js play greeting
node scripts/bumblebee.js say greeting motivation celebration
```

Available intents: greeting, motivation, freedom, empathy, celebration, goodnight, warning, pride, lets_go.

## Tips — Bumblebee

- **Always check devices first** — "No active device" is the most common failure
- **Bilingual library** — index has English and Spanish songs; search in either language
- **Clip duration** — clips auto-trim to vocal length (~130ms per character). Short, punchy.
- **Present the lyrics** — after playing, show the user what was said with translations if needed
- **Build emotional arcs** — start soft, build to the punchline (e.g., setup → commitment → crescendo)
- **The agent is the composer** — the engine finds lyrics, but YOU pick the best chain. Think like a DJ cutting between radio stations to form a sentence.
- **Index more songs = better vocabulary.** The more songs indexed, the more phrases available. Run `batch-index` to start, then add songs that match your user's taste.
- **When compose fails**, try rephrasing with common song vocabulary: "baby", "tonight", "forever", "hold on", "let me", "I need", "don't stop"

---
version: "1.0.0"

# R2-DJ — Contextual Music Curation 🎧🤖

An AI DJ that reads the moment and plays the right music. Knows 5 frequency profiles that map to different states of mind and times of day.

## Frequency Profiles

| Frequency | Vibe | Time | Key Artists |
|---|---|---|---|
| **Architect** | Solo builder, focus, flow state | 9AM-5PM, 10PM-2AM | C418, Jarre, Tangerine Dream, Vangelis |
| **Dreamer** | Synthwave, retro-futurism, night cruising | 8PM-3AM | Kavinsky, M83, Com Truise, Perturbator |
| **Mexican Soul** | Heritage, roots, identity | Anytime | José José, Vicente, Natalia, Café Tacvba |
| **Seeker** | Post-midnight processing, healing | 11PM-6AM | Solfeggio, 528Hz, 639Hz, ambient |
| **Cinephile** | Film scores, thinking, reflecting | 7PM-2AM | Jóhannsson, Zimmer, Richter, Greenwood |

## Core Commands

### Auto-Vibe (Let R2 Pick)

```bash
node scripts/r2-dj.js vibe
```

Reads time of day + recent listening → detects the right frequency → builds and plays a queue. Outputs a JSON summary for the agent's reply.

### Force a Frequency

```bash
node scripts/r2-dj.js vibe --frequency seeker
node scripts/r2-dj.js vibe --frequency architect --device iPhone
```

### Playback Control

```bash
node scripts/r2-dj.js now        # What's playing
node scripts/r2-dj.js pause      # Pause
node scripts/r2-dj.js skip       # Next track
node scripts/r2-dj.js volume 50  # Set volume
node scripts/r2-dj.js play "Nils Frahm Says"        # Search + play
node scripts/r2-dj.js play spotify:track:xxx         # Play URI directly
node scripts/r2-dj.js search "ambient electronic"    # Search tracks
```

### Context & Info

```bash
node scripts/r2-dj.js context      # Time, recent plays, detected frequency, devices
node scripts/r2-dj.js frequencies   # List all frequency profiles
node scripts/r2-dj.js history       # Recent listening history
node scripts/r2-dj.js devices       # Spotify devices
```

## How the Agent Should Use R2-DJ

1. **"Play music" / "what should I listen to"** → `r2-dj.js vibe` (auto-detect)
2. **"I need to focus"** → `r2-dj.js vibe --frequency architect`
3. **"Something for the drive"** → `r2-dj.js vibe --frequency dreamer`
4. **"Wind me down"** → `r2-dj.js vibe --frequency seeker`
5. **"Play [specific song]"** → `r2-dj.js play "song name"`
6. **Mood descriptions** → Pick the closest frequency, then `vibe --frequency <key>`

## Tips — R2-DJ

- Auto-vibe uses time + recent listening to pick the frequency — it's smart, trust it
- The agent can also manually build curated queues with inline Spotify API calls for special moments
- Frequencies aren't rigid — if recent listening suggests Architect at midnight, that wins over time-based detection
- **Present the tracklist** after playing — show what you queued and why
- JSON summary after `---JSON_SUMMARY---` is for agent parsing, not user display
