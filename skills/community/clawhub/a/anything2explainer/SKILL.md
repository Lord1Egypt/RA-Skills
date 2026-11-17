---
name: anything2explainer
description: "Turn any topic into animated explainer videos — Remotion-driven, TTS voiceover, bilingual (Chinese/English)"
version: 1.0.0
author: Vincentwei1021 | Weekly Discovery
license: PolyForm Noncommercial
platforms: [linux, macos]
metadata:
  hermes:
    tags: [video, animation, remotion, tts, explainer]
---

# Anything2Explainer

Transform any topic into animated explainer videos with TTS voiceover, subtitles, and chapter progress bars. Bilingual support (Chinese/English).

## Source

- GitHub: https://github.com/Vincentwei1021/anything2explainer
- Stars: ~711 (2026-09)
- License: PolyForm Noncommercial (commercial use requires license)

## Trigger Conditions

- Need to convert technical concepts into visual videos
- Need to generate educational/science popularization explainer videos
- Need batch generation of topic introduction videos
- Process both Chinese and English content

## Core Features

### Full Pipeline Automation
1. **Research** — scrape and synthesize information from web sources
2. **Script** — generate structured script with chapters
3. **Storyboard** — create visual descriptions for each scene
4. **Render** — generate frames using Remotion
5. **QC** — quality check and refine output

### Bilingual Support
- Chinese and English prompts and output
- TTS voiceover in both languages (edge-tts / kokoro)
- Subtitle generation for both languages

### Technical Stack
- **Framework**: Remotion (React + TypeScript)
- **Rendering**: Frame-by-frame code-drawn animations
- **Voice**: edge-tts or kokoro for TTS
- **Output**: 1-3 minute videos, 1-3 hours generation time

## Installation

```bash
# Prerequisites
npm install -g remotion
npm install

# Clone and setup
git clone https://github.com/Vincentwei1021/anything2explainer.git
cd anything2explainer
npm install
```

## Usage

```bash
# Generate video from topic
npx remotion render src/index.ts AnyTopic --props '{"topic":"Quantum Computing"}'

# With Chinese content
npx remotion render src/index.ts AnyTopic --props '{"topic":"量子计算简介"}'

# Batch generation
node scripts/batch-generate.js topics.json
```

## Project Structure

```
anything2explainer/
├── src/
│   ├── components/     # Remotion components
│   ├── steps/          # Pipeline steps (research, script, storyboard)
│   └── index.ts        # Entry point
├── scripts/
│   ├── batch-generate.js
│   └── qc-check.js
└── package.json
```

## Pitfalls

- **License restriction** — PolyForm Noncommercial; contact author for commercial use
- **Generation time** — 1-3 minutes video takes 1-3 hours to render
- **Node.js required** — must have Node.js 18+ and FFmpeg installed
- **TTS quality** — edge-tts free tier has limits; consider paid TTS for production
- **Memory usage** — rendering large projects may require 8GB+ RAM

## Verification

```bash
# Quick test with simple topic
npx remotion render src/index.ts Test --props '{"topic":"Hello World"}' --length 1

# Check output
ls output/
```

## References

- GitHub: https://github.com/Vincentwei1021/anything2explainer
- Remotion Docs: https://docs.remotion.dev/
