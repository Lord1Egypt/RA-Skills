# 🐝 Bumblebee — Talk Through Music

An OpenClaw skill that lets your AI agent communicate through music.

**Two modes:**

### Bumblebee Mode 🐝
Your agent speaks through exact lyric clips — chaining song lines into sentences, like Bumblebee from Transformers talking through the radio.

> *"aquí me tienes"* → *"no te fallaré"* → *"contigo yo quiero envejecer"*

### R2-DJ Mode 🎧
Your agent reads the room — time of day, recent listening, current vibe — and curates the perfect queue. Five frequency profiles: Architect (focus), Dreamer (synthwave), Mexican Soul (heritage), Seeker (healing/sleep), Cinephile (film scores).

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) installed
- Spotify Premium account
- Node.js 18+

## Quick Install

```bash
# Clone into your skills directory
git clone https://github.com/swats-ai/bumblebee.git ~/.openclaw/workspace/skills/bumblebee
```

Then follow the [Spotify Setup Guide](SETUP.md) to connect your account.

## Usage

Once installed, just talk to your agent:

| You say | What happens |
|---------|-------------|
| *"Play music"* | R2-DJ auto-detects the vibe and queues tracks |
| *"Say it with music"* | Bumblebee chains lyrics into a message |
| *"Play something to focus"* | Architect frequency (C418, Jarre, Vangelis) |
| *"Wind me down"* | Seeker frequency (528Hz, singing bowls, ambient) |
| *"What's playing?"* | Current track info |

## Files

```
├── SKILL.md              # Agent instructions (read by OpenClaw)
├── SETUP.md              # Spotify setup walkthrough
├── scripts/
│   ├── bumblebee.js      # Intent-based playback
│   ├── r2-dj.js          # Contextual DJ engine
│   ├── lyric-engine.js   # Lyric search + clip playback
│   ├── lyric-index.json  # Indexed lyrics database
│   └── lyrics-db.json    # Full lyrics store
└── references/
    └── song-library.md   # Curated song catalog
```

## How Bumblebee Works

1. Agent searches the lyric index for lines that literally say what it means
2. Chains 2-4 clips with exact Spotify timestamps
3. Plays each clip on your active device with brief pauses between
4. Presents the lyrics with translations

## How R2-DJ Works

1. Checks the time of day + your recent Spotify history
2. Auto-detects which frequency profile fits the moment
3. Searches Spotify for matching tracks
4. Queues 10-15 tracks on your active device

## License

MIT

---

*Built with 🤖 by [SWATS.ai](https://swats.ai) — Your AI, Your Rules*
