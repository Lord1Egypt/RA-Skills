---
name: ai-video-remix
description: AI-driven video remix generator that uses ShotAI semantic search + LLM planning + Remotion rendering to produce styled video compositions from a user's local video library. Use when the user asks to create a video remix, highlight reel, travel vlog, sports highlight, nature montage, or any styled video cut from their library. Triggers on requests like "帮我做一个混剪", "make a travel vlog from my library", "create a sports highlight", or "generate a video with my footage". Requires ShotAI (local MCP server) to be running. Works with any OpenAI-compatible LLM API or falls back to heuristic mode with no API key.
source: https://github.com/abu-ShotAI/ai-video-remix
homepage: https://github.com/abu-ShotAI/ai-video-remix
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - node
      env:
        - SHOTAI_URL
        - SHOTAI_TOKEN
    primaryEnv: SHOTAI_TOKEN
---

# AI Video Remix Skill

> This is an **instruction-only skill** — it provides guidance and reference documentation for the AI Video Remix CLI tool. The runtime source code lives in the [GitHub repository](https://github.com/abu-ShotAI/ai-video-remix) and must be cloned separately (see Quick Start below).

Generate styled video compositions from a local ShotAI video library using natural language.

## Important: Video Library Requirement

This skill can **only** search and use videos that have been imported into ShotAI. Videos simply stored on your hard drive are **not** searchable — they must be added to a ShotAI collection and fully indexed first.

Before using this skill, make sure you have:
1. Opened [ShotAI](https://www.shotai.io) and created a collection
2. Added your video files or folders to the collection
3. Waited for indexing to complete (shot detection + semantic analysis — progress is shown in ShotAI)

If the search returns no results or low-quality matches, the most common reason is that the relevant videos have not been imported into ShotAI yet.

## Prerequisites

See [references/setup.md](references/setup.md) for full installation instructions, including:
- ShotAI download and setup
- ffmpeg installation
- yt-dlp installation (for auto music)
- Node.js dependencies

## Quick Start

> **Note:** This skill does not bundle runtime code. Clone the source repository first.

```bash
git clone https://github.com/abu-ShotAI/ai-video-remix.git
cd ai-video-editor
npm install
cp .env.example .env    # fill in SHOTAI_URL, SHOTAI_TOKEN, and optionally AGENT_PROVIDER
npx tsx src/skill/cli.ts "帮我做一个旅行混剪"
```

## Pipeline (8 steps)

1. **Agent: parseIntent** — LLM extracts theme, selects composition, optionally overrides music style
2. **Agent: refineQueries** — LLM rewrites per-slot search terms to match library content
3. **ShotAI: pickShots** — Semantic search per slot via local ShotAI MCP server (localhost only), best shot selected
4. **Music: resolveMusic** — Uses local MP3 via `--bgm` (recommended), or optionally downloads from YouTube via yt-dlp
5. **ffmpeg: extractClip** — Each shot trimmed to independent `.mp4` clip file (local processing only)
6. **Agent: annotateClips** — LLM assigns per-clip visual effect params (tone, dramatic, kenBurns, caption)
7. **File Server** — Localhost-only HTTP server (127.0.0.1) serves clips to Remotion renderer within the same machine
8. **Remotion: render** — Composition rendered to final MP4

## CLI Usage

After cloning the repository and running `npm install`:

```bash
npx tsx src/skill/cli.ts "<request>" [options]

Options:
  --composition <id>   Override composition (skip LLM selection)
  --bgm <path>         Local MP3 path (skip YouTube search)
  --output <dir>       Output directory (default: ./output)
  --lang <zh|en>       Output language: zh Chinese (default) / en English
                       Affects: video title, per-clip captions & location labels, attribution line
  --probe              Scan library first, let LLM plan slots from actual content
```

## Compositions

| ID | Label | Best For |
|----|-------|----------|
| `CyberpunkCity` | 赛博朋克夜景 | Neon city, night scenes, sci-fi |
| `TravelVlog` | 旅行 Vlog | Multi-city travel with location cards |
| `MoodDriven` | 情绪驱动混剪 | Fast/slow emotion cuts |
| `NatureWild` | 自然野生动物 | BBC nature documentary style |
| `SwitzerlandScenic` | 瑞士风光 | Alpine/scenic travel with captions |
| `SportsHighlight` | 体育集锦 | ESPN-style with goal captions |

## Modes

**Standard mode** (default): LLM picks composition + generates search queries from registry templates.

**Probe mode** (`--probe`): Scans library videos first (names, shot samples, mood/scene tags), then LLM generates custom slots tailored to what actually exists.

Choose probe mode when: library content is unknown, user wants "best of my library", or standard slots return low-quality shots.

## Environment Variables

See [references/config.md](references/config.md) for all environment variables and LLM provider setup.

## Troubleshooting & Quality Tuning

See [references/tuning.md](references/tuning.md) for solutions to:
- Clip boundary flicker / 1–2 frame flash at cuts
- Red flash artifact in CyberpunkCity (GlitchFlicker on short clips)
- Low-quality or off-topic shots
- Music download failures

**Recommended `.env` defaults for best quality:**
```env
MIN_SCORE=0.5    # filter short/low-quality shots
```

## Writing ShotAI Search Queries

ShotAI uses semantic search powered by AI-generated tags and embedding vectors. Query quality is the single biggest factor in shot relevance — invest time here.

### Query construction rules

**Always write full sentences or rich phrases, never bare keywords.**

The search engine understands semantic similarity (`"ocean"` matches `"sea"`, `"waves"`, `"shoreline"`), so richer context produces better recall.

| Quality | Example | When to use |
|---------|---------|-------------|
| ⭐ Detailed description | `"A white seagull with spread wings gliding smoothly over calm blue ocean water, golden sunset light reflecting on the waves"` | Best precision — use for hero shots |
| ⭐ Full sentence | `"A seagull flying gracefully over the ocean at sunset"` | Good balance of precision and recall |
| Short phrase | `"seagull flying over ocean"` | Acceptable fallback |
| Single keyword | `"seagull"` | Avoid — low precision, noisy results |

### What to include in a query

Describe the **visual content** of the ideal shot across these dimensions:

- **Subject**: what/who is in frame (`a lone hiker`, `city traffic at night`, `athlete celebrating`)
- **Action**: what is happening (`walking slowly through fog`, `speeding through intersection`, `jumping with arms raised`)
- **Environment**: location, setting, time of day (`rain-soaked Tokyo street`, `mountain meadow at golden hour`, `empty stadium under floodlights`)
- **Mood / atmosphere**: emotional tone (`melancholic`, `tense`, `euphoric`, `serene`)
- **Camera feel**: implied movement or framing (`wide establishing shot`, `tight close-up`, `slow pan`, `handheld shaky`)

Not all dimensions are needed every time — include whichever are most distinctive for the shot you want.

### The refineQueries step

When the agent runs `refineQueries`, it rewrites the composition's default slot queries to better match the user's actual library. Apply these principles:

1. **Start from the slot's semantic intent** — what emotional or narrative role does this shot play in the composition?
2. **Incorporate any context from the user's request** — location names, event names, specific subjects mentioned
3. **Expand synonyms** — if the slot says `"water"`, try `"river flowing through forest"` or `"lake reflecting mountains"` based on what the library likely contains
4. **Avoid negations** — `"not indoors"` does not work; instead describe the positive version (`"outdoor daylight scene"`)
5. **One query per slot** — make it specific rather than trying to cover multiple scenarios

### Examples: slot query → refined query

```
Slot default: "city at night"
User request: "帮我做一个东京旅行混剪"
Refined:      "Neon-lit Tokyo street at night, pedestrians crossing under glowing signs, rain reflections on pavement"

Slot default: "nature landscape"
User request: "trip to Patagonia last month"
Refined:      "Dramatic Patagonia mountain landscape, snow-capped peaks under stormy clouds, vast open wilderness"

Slot default: "athlete in action"
User request: "basketball highlight from last game"
Refined:      "Basketball player driving to the hoop, explosive movement, crowd in background blurred"
```

## Adding a New Composition

See [references/composition-guide.md](references/composition-guide.md) to add a new Remotion composition to the registry.

## Safety and Fallback

### Network & credential scope
- **All credentials stay local.** `SHOTAI_TOKEN` is sent only to the local ShotAI MCP server (`127.0.0.1`). LLM API keys (if configured) are sent only to their respective provider endpoints — never to ShotAI, YouTube, or any other service.
- **The clip file server binds to `127.0.0.1` only** (default port 8080). It is not accessible from other machines on the network. It serves temporary clip files to the Remotion renderer running on the same machine and shuts down after rendering completes.
- **yt-dlp is optional.** Use `--bgm /path/to/local.mp3` to skip all YouTube network access. When yt-dlp is used, it only downloads a single background music track — no other data is sent to YouTube.
- **LLM access is optional.** Set `AGENT_PROVIDER=none` to run in heuristic mode with zero external network calls (aside from the local ShotAI MCP server).

### Error handling
- If `SHOTAI_URL` or `SHOTAI_TOKEN` is unset, display a warning: "ShotAI MCP server is not configured. Set `SHOTAI_URL` and `SHOTAI_TOKEN` in your `.env` file. Download ShotAI at https://www.shotai.io."
- If the ShotAI MCP server returns an error (connection refused, HTTP 4xx/5xx), display the error message and stop — do not fabricate shot results.
- Never fabricate video file paths, shot timestamps, or similarity scores.
- If music download fails (yt-dlp error or network unreachable), suggest using `--bgm <local.mp3>` to provide a local audio file instead.
- If Remotion render fails, display the error output and suggest checking Node.js version (18+) and that all clip files were extracted successfully.
- If the LLM provider is unreachable, fall back to heuristic mode: use composition default queries directly without refinement, and skip `annotateClips` (use composition default effect params).

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
See https://spdx.org/licenses/MIT-0.html
