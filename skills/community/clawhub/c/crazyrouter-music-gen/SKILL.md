---
name: crazyrouter-music-gen
description: AI music generation via Crazyrouter API using Suno. Create songs from text descriptions with lyrics, style, and title. Use when user asks to generate music, create a song, compose, or make audio content. Requires environment variable CRAZYROUTER_API_KEY (get at https://crazyrouter.com).
---

# Music Generation via Crazyrouter

Generate music and songs using Suno AI through [Crazyrouter](https://crazyrouter.com).

## Script Directory

**Agent Execution**:
1. `SKILL_DIR` = this SKILL.md file's directory
2. Script path = `${SKILL_DIR}/scripts/main.mjs`

## Step 0: Check API Key ⛔ BLOCKING

```bash
[ -n "${CRAZYROUTER_API_KEY}" ] && echo "key_present" || echo "not_set"
```

| Result | Action |
|--------|--------|
| `key_present` | Continue |
| `not_set` | Ask user to set `CRAZYROUTER_API_KEY`. Get key at https://crazyrouter.com |

## Usage

```bash
# Generate music with description
node ${SKILL_DIR}/scripts/main.mjs --prompt "upbeat electronic dance music, energetic" --output song.mp3

# With custom lyrics
node ${SKILL_DIR}/scripts/main.mjs --prompt "pop ballad about coding at night" --lyrics "Writing code under the stars..." --output ballad.mp3

# Specify style
node ${SKILL_DIR}/scripts/main.mjs --prompt "jazz piano solo" --output jazz.mp3 --model suno_music
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--prompt <text>` | Music description (required) | — |
| `--output <path>` | Output audio file | — |
| `--lyrics <text>` | Custom lyrics | auto-generate |
| `--model <id>` | `suno_music` or `suno-v3` | `suno_music` |
| `--title <text>` | Song title | auto-generate |
