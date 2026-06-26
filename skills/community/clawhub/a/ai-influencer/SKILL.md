---
name: ai-influencer
description: Create an AI clone video (talking head) from a single reference photo, a text script, and a cloned voice. Automates the pipeline of image generation (Gemini), voice cloning (ElevenLabs), and lip-sync video animation (Kling AI).
---

# AI Influencer Agent Skill

This skill allows OpenClaw to automatically generate photorealistic talking-head videos (AI clones) without you ever needing to record. It orchestrates a 3-step pipeline:

1.  **Identity Lock (Visuals):** Takes a base photo and prompt to generate a 4K studio-quality portrait (mocked/orchestrated via Gemini/Nano Banana Pro).
2.  **Voice Cloning (Audio):** Takes your text script and generates a natural voice track using ElevenLabs.
3.  **Lip Sync & Animation (Video):** Takes the static image and the audio track, and runs them through Kling AI's advanced Avatar/Lip-Sync pipeline to create a seamless, talking video.

## Prerequisites

To use this pipeline, you must have the following API keys set in your environment:
-   `ELEVENLABS_API_KEY`: For generating the voice track.
-   `KLING_ACCESS_KEY` & `KLING_SECRET_KEY`: For animating the final video.

## Usage

When a user asks to generate an AI Influencer video or "run the influencer pipeline", use this script:

```bash
uv run {baseDir}/scripts/influencer_pipeline.py \
    --image "/path/to/reference.png" \
    --prompt "A man sitting at a desk looking at the camera, subtle natural movement, calm, talking head" \
    --text "This is the script that the AI avatar will speak." \
    --voice-id "YOUR_ELEVENLABS_VOICE_ID"
```

## How It Works

This script acts as a high-level orchestrator. In a real-world scenario, it sequentially calls the ElevenLabs API for audio generation, and the Kling AI API (`identify-face` -> `advanced-lip-sync`) for final rendering. 

*Note: Video generation via Kling API can take 5-10 minutes. Inform the user that the process runs asynchronously and requires sufficient Developer API credits on Kling.*