---
slug: emergence-video-producer
name: Emergence Video Producer
version: 0.1.1
tags: [video, automation, webreel, slidev, ffmpeg]
description: |
  Automated video production pipeline for product demos and academic tutorials.
  Uses WebReel for browser recording, DashScope/Edge-TTS for narration, and FFmpeg for assembly.
---

# Skill: Emergence Video Producer 🎬

This skill transforms a Markdown "Video Script" into a polished tutorial video. It is designed for headless operation on cloud VMs, enabling agents to produce visual documentation autonomously.

## 1. Prerequisites

Ensure the following tools are in the path:
- `webreel` (for browser recording)
- `ffmpeg` (for assembly)
- `edge-tts` or `dashscope` credentials (for narration)
- `Pillow` (for frame extraction if WebP conversion is needed)

## 2. Interaction Model: The Interview

Unlike rigid CLIs, this skill starts with a **Human-in-the-Loop Interview**. 

### The Discovery Phase
The agent must proactively ask the following:
1.  **Objective**: "What is the primary goal of this video? (e.g., Feature Launch, Academic Summary, Onboarding)"
2.  **Mode**: "Should this be a **Browser Walkthrough** (WebReel) or a **PPT-style Presentation** (Slidev)?"
3.  **Tone**: "What is the desired persona? (e.g., Professional, Hype, Scientific)"
4.  **Target URL/Content**: "Which website are we recording, or what are the key slides?"

## 3. Workflow Phases

### Phase 1: Ideation & Storyboarding
Based on the interview, the agent drafts a `storyboard.md`. This is a negotiated artifact. 
- **DO NOT** ask the human to write the Markdown. 
- **DO** ask the human to "Review and Approve" the draft.

### Phase 2: Configuration & Asset Prep
Once approved, the agent automatically generates:
1.  **For Browser Mode**: A `webreel.config.json` with precise selectors and timings.
2.  **For Slide Mode**: A `slides.md` for Slidev rendering.
3.  **Audio**: Narration text synthesized into high-quality TTS.

### Phase 3: Production (The Engine)
The agent executes the headless recording and assembly. It handles:
- Browser automation (WebReel)
- Slide rendering (Slidev)
- Frame extraction and FFmpeg merging

### Phase 4: Taste Gate & Distribution
The agent presents the video for final "Taste Gate" approval before publishing to ClawHub or social platforms.

## 4. Usage Example

```bash
# Generate a video for the current project
hermes run emergence-video-producer --script video-script.md --output tutorial.mp4
```

---

## 5. Development Notes

- **Framerate Sync**: The assembly script automatically adjusts the framerate: `FPS = TOTAL_FRAMES / AUDIO_DURATION`.
- **Browser State**: Ensure the product is accessible via URL or a local dev server before recording.
