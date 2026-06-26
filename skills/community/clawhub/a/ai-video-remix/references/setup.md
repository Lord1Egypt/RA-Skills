# Setup Guide

## 1. ShotAI (Required)

ShotAI is the local video asset management system that powers semantic shot search.

**Download**: https://www.shotai.io — available for Mac and Windows.

After installation:
1. Open ShotAI and add your video files/folders to a collection
2. Wait for indexing to complete (ShotAI processes each video: detects shots, generates embeddings)
3. Enable the MCP server: **Settings → MCP Server → Enable**
4. Note your **MCP URL** (default: `http://127.0.0.1:23817`) and **MCP Token**

The MCP server uses SSE transport (not REST). The token is shown in ShotAI settings.

## 2. ffmpeg (Required)

Used for clip extraction and keyframe brightness analysis.

```bash
# macOS
brew install ffmpeg

# Windows
winget install ffmpeg

# Verify
ffmpeg -version
ffprobe -version
```

## 3. yt-dlp (Optional — for auto music)

Used to search and download background music from YouTube. **Optional** — skip if using `--bgm` with a local MP3 file.

```bash
# macOS
brew install yt-dlp

# Windows
winget install yt-dlp

# Verify
yt-dlp --version
```

## 4. Node.js (Required)

Node.js 18+ required (LTS recommended, tested on Node 18–22).

```bash
# macOS
brew install node

# Windows
winget install OpenJS.NodeJS

node --version  # should be 18+
npm --version
```

## 5. Project Setup

```bash
git clone https://github.com/abu-ShotAI/ai-video-remix.git
cd ai-video-editor
npm install
cp .env.example .env
```

Edit `.env` with at minimum:

```env
SHOTAI_URL=http://127.0.0.1:23817
SHOTAI_TOKEN=<your-token-from-shotai-settings>
```

## 6. Verify Everything Works

After cloning the repository (`git clone https://github.com/abu-ShotAI/ai-video-remix.git`) and running `npm install`:

```bash
# Test skill (heuristic mode, no LLM needed)
AGENT_PROVIDER=none npx tsx src/skill/cli.ts "test run" --composition TravelVlog
```

If this produces a rendered video in `./output/`, the setup is complete.
