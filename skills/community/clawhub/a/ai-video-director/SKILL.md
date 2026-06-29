---
name: AI Video Director
slug: ai-video-director
description: Full-stack AI video creation pipeline. Supports Sora/Kling/Runway/Pika/即梦/Luma/Vidu/海螺AI. From concept→storyboard→frame-level prompts→platform optimization→post-production. 100+ cinematic shot templates, 10+ video types (ads/shorts/microfilms/animations).
author: Marvis Studio
version: 1.0.0
tags: ["ai-video", "video-generation", "sora", "kling", "runway", "prompt-engineering", "storyboard", "content-creation"]
requires: []
metadata:
  emoji: 🎬
  category: "AI/Content Creation"
  pricing: "Free"
---

# AI Video Director

## Capabilities

| Capability | Description |
|------------|-------------|
| **Multi-platform support** | Sora, Kling, 可灵, Runway Gen-4, Pika 2.0, 即梦, Luma Dream Machine, Vidu, 海螺AI, PixVerse |
| **Video type templates** | 10 types: Ad TVC, Brand promo, Short video, Microfilm, Product showcase, Educational, MG animation, Holiday marketing, Plot twist, Visual masterpiece |
| **Professional storyboarding** | Shot-by-shot breakdown: shot number, scene, camera movement, duration, visual description, prompt, sound effect, voiceover |
| **Frame-level prompt precision** | 6-dimensional description: subject action, lighting, color, material, atmosphere, composition |
| **Platform parameter optimization** | Resolution, frame rate, duration, aspect ratio, motion intensity, consistency parameters |
| **Post-production guidance** | Editing rhythm, transition recommendations, BGM suggestions, subtitle styling |
| **Multi-version output** | Standard, Creative, Minimalist versions |

## Trigger Keywords
- "AI视频", "video制作", "分镜头", "storyboard", "AI动画", "Sora", "Kling", "Runway", "视频提示词", "video creation"

## Workflow

### Phase 1: Requirement Analysis
Identify video type, target platform, style preference, duration, brand tone.

### Phase 2: Creative Strategy
Develop narrative structure (flashback/parallel/progressive/suspense), determine visual style reference.

### Phase 3: Storyboard Generation
Output professional shot-by-shot storyboard table with 6D prompts and platform-specific parameters.

### Phase 4: Post-production Plan
Output editing rhythm suggestions, transition recommendations, BGM style recommendations, subtitle styling.

## Output Format
- **Storyboard Table** (Markdown table with columns: Shot#, Scene, Camera, Duration, Visual Description, Prompt, Sound, Voiceover)
- **Platform-specific Prompt Sets** (formatted for each target platform)
- **Parameter Recommendations** (JSON with resolution, fps, duration, etc.)
- **Post-production Checklist**

## Examples

**Example 1: Product Showcase Video**
```
Input: "Create a 30-second product showcase for a new smartphone"
Output: 
- Storyboard: 8 shots (intro→features→demo→call-to-action)
- Sora prompts (English, detailed frame descriptions)
- Platform: Sora, 1920x1080, 30fps, 30s
- BGM: Upbeat electronic
```

**Example 2: Brand Story Microfilm**
```
Input: "Tell a brand story about sustainability in 60 seconds"
Output:
- Narrative: Problem→Solution→Impact
- 12-shot emotional arc
- Kling prompts (Chinese preferred)
- Color grading: Natural, earthy tones
```

## Notes
- Different platforms have different prompt formats; automatically adapt
- Sora and Kling prompts work best in English
- Video duration should match platform characteristics (TikTok: 15-60s, YouTube: 30s-3min)
- Complex scenes should have at least 8 shots for proper storytelling
- Always include negative prompts to avoid unwanted elements

## Installation
```bash
npx clawhub install ai-video-director
```

## License
MIT-0
