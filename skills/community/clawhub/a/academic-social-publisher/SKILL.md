---
name: academic-social-publisher
description: Generate platform-optimized academic content from papers for ResearchGate, LinkedIn, and WeChat. Activated when Chopin shares a paper/article and wants to create social posts, or when composing a new research announcement. Can optionally generate a video introduction script and produce a video (requires AI video API key). Use when Chopin wants to amplify academic influence, share published papers, or create research awareness campaigns.
---

# Academic Social Publisher

Transform academic papers into engaging social media content for ResearchGate, LinkedIn, and WeChat. Optionally generate a video.

## Input

Provide or forward the paper with:
- Title
- Authors
- Abstract / key points
- Publication venue / conference
- Link to paper
- (Optional) Specific angle or highlight to emphasize

## Output Platforms

### 1. ResearchGate Post

- **Tone:** Academic, formal
- **Length:** 300-500 words
- **Content:** Full abstract highlight + methodology punchline + link
- **Includes:** Hashtags (#FormationControl #EventTriggered #MultiAgentSystems etc.)

### 2. LinkedIn Post

- **Tone:** Professional but conversational, storytelling-driven
- **Length:** 150-300 words (shorter for feed algorithm)
- **Content:** Hook opener → key contribution → why it matters → CTA (read paper / connect)
- **Format:** Short paragraphs, emoji sparingly, line breaks for readability

### 3. WeChat Article (公众号风格)

- **Tone:** Chinese, semi-formal, accessible to educated non-specialists
- **Length:** 800-1500 characters
- **Content:** 标题 (catchy) → 背景 → 核心贡献 → 亮点解读 → 结语
- **Style:** Use "我们" for warmth, include 2-3 emoji, technical terms with brief explanations

### 4. Video Introduction Script (Optional — always generated, video production depends on config)

- **Length:** 60-90 seconds narration (~150-200 words)
- **Structure:**
  - Opening hook (1 sentence, intriguing question or surprising fact)
  - What this paper is about (1-2 sentences)
  - Why it matters (1 sentence)
  - Key contribution (1-2 sentences)
  - Closing CTA
  - Scene/slideshow suggestions for visuals
- **Output:** Always produces a complete narration script

## Video Production (Optional — requires config)

Video generation is **opt-in and requires setup**. Without an API key, the skill still produces the full script for manual use.

### Option A: Full AI Video Pipeline (requires API key)

Requires one of:
- **HeyGen** — text-to-video with avatar, best for presenter-style research talk
- **Runway / Pika / Kling** — AI video clips from text/image prompts
- **ElevenLabs** — already configured for TTS voice

Pipeline:
1. Generate narration audio via ElevenLabs (or configured TTS)
2. Generate slide/image assets via image generation
3. Compose video via ffmpeg
4. (Optional) Enhance with HeyGen/Runway API

### Option B: Script-Only Mode (no API key needed)

Even without video API keys, always:
- ✅ Generate full video narration script with scene directions
- ✅ Suggest slide content and visual layout
- ✅ Provide timing cues

User can take the script and produce the video manually or with their own tools.

## Workflow

1. Parse paper info (title, authors, abstract, venue)
2. Identify 3 key talking points
3. Draft ResearchGate version
4. Adapt to LinkedIn voice
5. Adapt to WeChat Chinese style
6. Generate video narration script (always)
7. If video API configured: produce audio/video
8. Output all versions clearly separated

## Configuration

To enable video generation, add to your skill config or environment:

```yaml
# Example: TTS only (already has sag/ElevenLabs)
video:
  enabled: true
  tts: elevenlabs  # uses existing sag tool
  # Generate slides as images

# Example: Full pipeline
video:
  enabled: true
  tts: elevenlabs
  video_api: heygen  # or runway/pika/kling
  api_key: YOUR_KEY
```

If `video.enabled: false` or no API key, skip video production and deliver script only.

## Platform Best Practices

See `references/platform-guides.md` for detailed character limits, hashtag strategies, and posting tips per platform.
