---
name: bnbot-mascot
description: Generate BNBOT lobster-bot mascot images in consistent style using reference images. Use when the user asks to generate mascot illustrations, character poses, tweet images, stickers, or any BNBOT branded artwork. Triggers on requests like "generate a mascot image", "make a BNBOT illustration", "create a tweet image with the lobster", "generate mascot sticker".
version: 0.1.0
homepage: https://github.com/jackleeio/bnbot-mascot-skill
metadata:
  openclaw:
    emoji: "\U0001F99E"
    os: [darwin, linux]
    requires:
      skills: [bnbot]
---

# BNBOT Mascot Generator

Generate BNBOT's lobster-bot mascot in various poses and scenarios while maintaining consistent character design, using existing reference images for style matching.

## How It Works

1. Takes a reference image from the pre-approved set (V6/V7/V8 candidates)
2. Sends it to Gemini as style reference along with the action prompt
3. Gemini generates a new image matching the style
4. Green-screen chromakey removes background for transparent PNG

## Prerequisites

- Python: `/Users/jacklee/Projects/BNBOT/backend/.venv/bin/python`
- Dependencies: `google-genai`, `numpy`, `Pillow` (already installed)
- API key: `GOOGLE_AI_API_KEY` in `/Users/jacklee/Projects/BNBOT/.env`
- Reference images in `~/.claude/skills/bnbot-mascot/references/`

## Usage

### Quick generation via CLI

```bash
/Users/jacklee/Projects/BNBOT/backend/.venv/bin/python \
  ~/.claude/skills/bnbot-mascot/scripts/generate_mascot.py \
  "waving hello cheerfully" \
  output.png \
  full-body-front
```

### In Python script

```python
import sys
sys.path.insert(0, "/Users/jacklee/.claude/skills/bnbot-mascot/scripts")
from generate_mascot import generate_mascot

# Full body mascot
result = generate_mascot(
    action="waving hello cheerfully",
    output_path="mascot_wave.png",
    reference="full-body-front",       # style reference
    background="transparent",           # or "black", "white"
)

# Logo/icon version (head + claws only)
result = generate_mascot(
    action="looking excited",
    output_path="mascot_icon.png",
    reference="logo-head-claws",
)
```

## Available References

| Reference | Description | Best for |
|-----------|-------------|----------|
| `full-body-front` | Front facing, symmetric, claws raised | General mascot, banners |
| `full-body-side` | Playful side pose, one claw up | Dynamic illustrations |
| `full-body-action` | Action pose, LED heart eye | Exciting/promo content |
| `full-body-cute` | Cute pose, CRT head, winking | Friendly/approachable content |
| `logo-head-claws` | Head + claws only, no body | Icons, logos, small sizes |

## Action Ideas

### For tweets / social media
- `waving hello cheerfully` - 打招呼
- `giving a thumbs up with one claw` - 点赞
- `holding a golden trophy` - 庆祝成就
- `sitting at a computer typing` - 工作中
- `wearing sunglasses, looking cool` - 耍酷
- `holding a megaphone, announcing something` - 宣传
- `celebrating with confetti` - 庆祝
- `thinking with one claw on chin` - 思考

### For stickers / reactions
- `laughing happily` - 开心
- `crying with pixel tears on screen` - 伤心
- `angry with pixel fire eyes` - 生气
- `sleeping with pixel ZZZ on screen` - 睡觉
- `shocked with pixel exclamation marks` - 惊讶
- `heart eyes, both eyes showing pixel hearts` - 喜爱

### For branded content
- `holding a sign that says BNBOT` - 品牌展示
- `standing next to the Twitter/X logo` - 社交媒体
- `emerging from a computer screen` - 科技感
- `riding a rocket` - 增长/发射

## Saving Output

For tweet images, save to a convenient location:
```python
result = generate_mascot(
    action="your action here",
    output_path="/Users/jacklee/Desktop/mascot_tweet.png",
    background="black",  # use "black" for tweet-ready images
)
```

## Character Identity (DO NOT MODIFY)

The mascot is a **Lobster Bot** with these immutable features:
- **Head**: Golden retro TV/monitor frame, dark screen
- **Face**: LED pixel style - pink heart left eye, golden dash right eye, pixel smirk
- **Antenna**: Two with golden ball tips
- **Claws**: Golden with gear joints (mechanical but clean)
- **Body**: Red-orange lobster, chibi proportions
- **Style**: Cartoon vector, cel-shaded, thick outlines, sticker art
- **Colors**: Gold #FFD700, Pink #FF4466, Red-orange #E85D3A, Dark screen #1A1A2E
