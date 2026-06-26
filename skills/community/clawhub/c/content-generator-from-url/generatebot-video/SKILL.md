---
name: generatebot-video
description: Create short-form video reels and social media videos (TikTok, Instagram Reels, YouTube Shorts) from any topic or article via the GenerateBot API. Builds slides with images, captions, text-to-speech voiceover, background music, and custom styling. Use when the user wants to make a video, create a reel, turn an article into a video, generate video content, or produce short-form video for social media.
emoji: 🎬
homepage: https://generatebot.com
metadata:
  openclaw:
    primaryEnv: GENERATEBOT_API_KEY
    requires:
      env:
        - GENERATEBOT_API_KEY
---

## GenerateBot Video - Create Video Reels

Base URL: `https://generatebot.com/api/v1`

Authentication: Bearer token in the Authorization header.
```
Authorization: Bearer GENERATEBOT_API_KEY
```

All request and response bodies use JSON. Set `Content-Type: application/json`.

---

### Overview

This skill creates short-form video reels (9:16 portrait, 1080x1920) with AI voiceover from content you have generated.

- **Cost:** 200 credits per video
- **Endpoint:** POST /api/v1/videos
- **Max concurrent renders:** 2 (extra requests return 429)
- **Typical render time:** 60-180 seconds

---

### Prerequisites

Before creating a video, you need **completed pipeline results**. Run a content pipeline first (see Core skill):
```
POST /api/v1/pipelines
{ "pipelineType": "content-analyzer", "url": "https://example.com/article" }
```
Poll until status is "completed", then extract these three things:

1. **Carousel slides:** `results.data.agents.carouselGenerator.carousel.slides`
   ```json
   [{ "slideNumber": 1, "text": "Key takeaway from the article" }, ...]
   ```

2. **Images:** `results.data.agents.imageFinder.foundImages`
   ```json
   [{ "imageUrl": "https://...", "altText": "...", "suggestedUse": "hero" }, ...]
   ```

3. **Hook:** `results.data.agents.scriptGenerator.scripts[0].hook`
   ```json
   "Breaking news you need to know!"
   ```

4. **Pipeline Run ID:** The `pipelineRunId` from the pipeline POST response.

---

### Step 1: Build Video Slides

Each carousel slide becomes one video slide. Map them like this:

```json
{
  "text": "<carousel slide text>",
  "imageUrl": "<image URL from imageFinder>",
  "highlight": ["key", "words"]
}
```

**Pairing rules:**
- Use the `suggestedUse: "hero"` image for slide 1
- Use remaining images for subsequent slides
- Each slide MUST have a unique `imageUrl` -- never reuse the same image across slides
- `text` is max 200 characters

**The `text` field is both the on-screen caption AND the voiceover narration.** Write it as spoken language:
- Numbers in words: "25 million dollars" not "$25M"
- Use "A.I." not "AI" (TTS pronounces it better)
- Add ellipsis for dramatic pauses: "And then... everything changed."

---

### Step 2: Image Display Modes

The `imageMode` field controls how images appear in the 9:16 portrait frame:

| Mode | Behavior | Best For |
|------|----------|----------|
| *(omit)* | **Auto-detect:** landscape (w/h > 1.2) uses overlay, else background | Most cases -- recommended |
| `"overlay"` | Image shown as 16:9 PiP inset (top 12%) over blurred/darkened version of itself | Landscape images, real estate, group photos |
| `"background"` | Full-screen cover-crop fills the entire frame | Portrait images, close-ups |
| `"background_with_overlays"` | Primary image full-bleed + `extraImages` as PiP insets | Multiple detail shots over a main image |

**Recommendation:** Omit `imageMode` in most cases. Auto-detection handles landscape vs portrait correctly. Only set it explicitly to override.

---

### Step 3: Extra Images and Word-Synced Timing

Add related images as overlays that appear synced to specific words in the narration:

```json
{
  "text": "A stunning property in Brisbane with a resort style pool",
  "imageUrl": "https://cdn.example.com/mansion-exterior.jpg",
  "extraImages": [
    "https://cdn.example.com/mansion-aerial.jpg",
    "https://cdn.example.com/mansion-pool.jpg"
  ],
  "extraImageTimings": [
    { "showAtWordIndex": 2 },
    { "showAtWordIndex": 7 }
  ]
}
```

**How word indexing works:**
Count words in `text` starting from 0, split on whitespace. Punctuation stays attached.

For the text above: A(0) stunning(1) property(2) in(3) Brisbane(4) with(5) a(6) resort(7) style(8) pool(9)

- The aerial shot appears at word 2 ("property")
- The pool shot appears at word 7 ("resort")
- Each overlay stays visible until the next one starts or the slide ends

**When to use extraImages:**
- Landscape images that lose detail when cropped to 9:16
- Multiple angles of the same subject (exterior + pool + interior)
- You CAN reuse the main `imageUrl` in `extraImages` for blurred-bg + clear-overlay effect

**Limits:** Max 5 extra images per slide. If you omit `extraImageTimings`, overlays distribute evenly (less precise).

---

### Step 4: Highlights

The `highlight` field is an array of words from `text` to emphasize visually (rendered in accent color with glow effect):

```json
"highlight": ["25 million", "mansion"]
```

- Pick 1-3 key words or phrases that appear in the `text`
- Max 10 items
- If omitted, the API auto-generates 2 highlights (prefers numbers and capitalized words)

---

### Step 5: Per-Slide Style Overrides (Optional)

Each slide can override global styles:

| Field | Type | Range |
|-------|------|-------|
| `fontSize` | number | 12-120 |
| `fontWeight` | string | "normal" or "bold" |
| `textColor` | string | hex, e.g. "#FFFFFF" |
| `backgroundColor` | string | hex, e.g. "#000000" |
| `textAlign` | string | "left", "center", "right" |
| `textPosition` | string | "top", "center", "bottom" |
| `imageOpacity` | number | 0-1 |
| `textWidthPercent` | number | 10-100 |
| `imageScale` | number | 0.1-5 (zoom level) |
| `imagePositionX` | number | horizontal offset |
| `imagePositionY` | number | vertical offset |

**Advanced text styling** (`textStyle` object, all fields optional):
```json
{
  "textStyle": {
    "fontFamily": "Inter",
    "letterSpacing": 1.2,
    "lineHeight": 1.4,
    "textTransform": "uppercase",
    "shadow": { "enabled": true, "offsetX": 2, "offsetY": 2, "blur": 4, "color": "#000000" },
    "outline": { "enabled": true, "width": 2, "color": "#000000" },
    "background": { "enabled": true, "color": "#000000", "opacity": 0.7, "paddingX": 12, "paddingY": 8, "borderRadius": 8 },
    "glow": { "enabled": true, "blur": 10, "color": "#75F30F", "intensity": 0.8 }
  }
}
```
- `textTransform`: "none", "uppercase", "lowercase", "capitalize"
- `shadow`: Drop shadow behind text
- `outline`: Stroke around text characters
- `background`: Colored box behind text (like a caption box)
- `glow`: Colored glow effect around text

---

### Step 6: Set the Hook

```json
"hook": "<scriptGenerator.scripts[0].hook>"
```

- Max 200 characters
- This is the opening text shown before slides begin
- No separate `script` field needed -- the API auto-builds TTS narration from all slide texts

---

### Step 7: Configure Global Style (Optional)

```json
"style": {
  "accentColor": "#FF5500",
  "captionStyle": "outlined",
  "captionPosition": "center",
  "fontSize": 48,
  "colorGrade": "cinematic",
  "filmGrain": { "enabled": true, "opacity": 0.025, "fps": 8 }
}
```

| Field | Options | Default |
|-------|---------|---------|
| `accentColor` | Hex color | #75F30F |
| `captionStyle` | "default", "outlined", "boxed", "marker" | "outlined" |
| `captionPosition` | "center", "lower-third", "top" | "lower-third" |
| `fontSize` | 24-96 | 52 |
| `colorGrade` | "cinematic", "warm", "cool", "vibrant", "none" | none |
| `filmGrain` | `{ enabled, opacity (0-0.1), fps (1-30) }` | disabled |

---

### Step 8: Configure Voice (Optional)

| Field | Description | Default |
|-------|-------------|---------|
| `voiceId` | ElevenLabs voice ID | (default Australian male) |
| `ttsModel` | "eleven_v3", "eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_turbo_v2_5" | "eleven_v3" |
| `speedFactor` | 0.5-3.0, post-render speed multiplier | 1.35 |

---

### Step 9: Assemble and Submit

**POST /api/v1/videos** (200 credits)

```json
{
  "hook": "$25M mansion hits the market!",
  "slides": [
    {
      "text": "A 25 million dollar mansion in Brisbane is up for grabs.",
      "imageUrl": "https://cdn.example.com/mansion-exterior.jpg",
      "highlight": ["25 million", "mansion"],
      "extraImages": ["https://cdn.example.com/mansion-aerial.jpg"],
      "extraImageTimings": [{ "showAtWordIndex": 4 }]
    },
    {
      "text": "Spanning 1400 square meters with five bedrooms and eight bathrooms.",
      "imageUrl": "https://cdn.example.com/mansion-pool.jpg",
      "highlight": ["1400", "bathrooms"]
    }
  ],
  "sourcePipelineRunId": "<pipelineRunId from pipeline POST>",
  "style": {
    "accentColor": "#75F30F",
    "captionStyle": "outlined",
    "captionPosition": "center"
  }
}
```

**Field constraints:**
- `hook`: 1-200 chars, required
- `slides`: 1-15 slides, required (4-7 recommended)
- `slides[].text`: 1-200 chars, required
- `slides[].imageUrl`: HTTPS URL, required
- `slides[].highlight`: max 10 items, optional
- `slides[].extraImages`: max 5 URLs, optional
- `watermark`: small text in corner, max 100 chars, optional
- `watermarkLogoUrl`: HTTPS URL to a logo image for the watermark, optional
- `watermarkPosition`: position string (max 50 chars), optional
- `cta`: `{ "text": "Follow for more!", "url": "example.com" }`, optional
- `sourcePipelineRunId`: UUID, **strongly recommended** -- links video to source content

Response:
```json
{
  "jobId": "uuid",
  "contentId": "uuid",
  "status": "queued",
  "creditsConsumed": 200,
  "statusUrl": "/api/v1/videos/{jobId}"
}
```

---

### Step 10: Poll for Completion

**GET /api/v1/videos/{jobId}** every 5 seconds.

Status progression: `queued` -> `generating_audio` -> `rendering` -> `uploading` -> `completed`

- **queued**: 10-30s while render worker starts. Normal.
- **generating_audio**: TTS is being generated. Progress, not a stall.
- **rendering**: Video frames being composed. Longest phase.
- **completed**: `videoUrl` contains the download URL.
- **failed**: `error` field contains the error message.

**Keep polling up to 5 minutes.** Do NOT stop on intermediate statuses. Do NOT report failure until status is "failed" or you have polled the maximum duration.

---

### Step 11: Post the Video

The video response includes a `contentId`. Use it directly with POST /api/v1/social/post (see Publish skill):

```json
{
  "contentId": "<contentId from video response>",
  "platforms": [{
    "accountId": "<from GET /api/v1/social/accounts>",
    "platform": "instagram",
    "contentType": "video",
    "caption": "Check out our latest video!"
  }]
}
```

---

### Render Time Estimates

| Slides | Approximate Time |
|--------|------------------|
| 3-5 | 60-90 seconds |
| 6-10 | 90-150 seconds |
| 11-15 | 150-180 seconds |

Audio generation adds 10-20 seconds. Upload adds 5-10 seconds.

---

### Error Handling

| HTTP Status | Meaning |
|-------------|---------|
| 402 | Insufficient credits (need 200) |
| 429 | Too many concurrent renders (max 2) -- wait and retry |
| 400 | Invalid request body -- check error details |

---

### Other GenerateBot Skills

- **Core Skill** (`generatebot-core`): Search for content, run pipelines, manage content library. **Required before creating videos.**
- **Publish Skill** (`generatebot-publish`): Post completed videos to social media, publish articles to CMS.
- **Templates Skill** (`generatebot-templates`): Design and render canvas-based post image templates.
- **Workflow Skill** (`generatebot-workflows`): End-to-end workflow examples and patterns.