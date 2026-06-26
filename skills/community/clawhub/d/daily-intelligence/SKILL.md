---
name: daily-intelligence
description: Fully automated daily intelligence briefing system. Searches news, generates high-res infographics (3600px), creates voice narration (edge-tts), uploads to Feishu/Lark docs, and delivers via cron. Battle-tested through 14+ days of continuous production use.
metadata:
  openclaw:
    requires:
      bins: ["python3", "playwright"]
    install:
      - id: python-edge-tts
        kind: pip
        package: edge-tts
        label: Install edge-tts for voice generation
---

# Daily Intelligence Briefing System

A complete, production-ready system for generating and delivering daily AI/tech intelligence briefings autonomously.

## What It Does

This skill automates the entire daily intelligence workflow:

1. **News Search** — Multi-source search (Tavily, Brave, RSS) for AI/tech news
2. **Content Curation** — Filter, rank, and summarize top stories into 5 modules
3. **Infographic Generation** — Python + Playwright to create 3600px high-res long images with logo, dark tech theme
4. **Voice Narration** — edge-tts (XiaoxiaoNeural) generates Chinese MP3 voiceover
5. **Document Creation** — Auto-create Feishu/Lark doc, upload infographic + text + voice link
6. **Delivery** — Send doc link + voice file to specified recipients
7. **Scheduling** — cron-based automation with isolated sessions

## Quick Start

```
Generate today's daily intelligence briefing for AI/tech news
```

```
Create a daily briefing infographic with 5 modules: world news, OPC trends, tech applications, new skills, and core recommendation
```

## Output Format (5 Modules)

1. 🌍 **World News** — AI breakthroughs + personalized product trends
2. 🏢 **OPC/One-Person Company** — Solo entrepreneur dynamics + policy
3. 🚀 **Tech Applications** — Actionable technology for your business
4. ⚡ **Agent Capabilities** — New skills and automation updates
5. 💡 **Core Recommendation** — One actionable insight for the day

## Infographic Specifications

- Width: 3600px (3x resolution)
- Theme: Dark tech style with gradient backgrounds
- Logo: Embedded base64 with gold gradient frame + glow effect
- Template: Fixed layout, daily content swap only
- Font: System fonts with calculated line heights

### Logo Integration

```css
.logo-wrapper {
  padding: 10px;
  background: linear-gradient(135deg, rgba(255,215,0,0.7), rgba(255,140,0,0.4));
  border-radius: 36px;
  box-shadow: 0 0 40px rgba(255,215,0,0.4);
}
```

## Voice Generation

```bash
python3 -m edge_tts --voice zh-CN-XiaoxiaoNeural --file content.txt --write-media output.mp3
```

## Cron Configuration

For automated daily delivery:

```json
{
  "name": "Daily Intelligence",
  "cron": "0 0 22 * * *",
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "deliver": true
  },
  "wakeMode": "now"
}
```

**⚠️ Critical**: Must use `isolated` session + `agentTurn` payload. `main` + `systemEvent` will NOT trigger full execution.

## Error Prevention System

This skill includes battle-tested safeguards:

| Error | Root Cause | Prevention |
|-------|-----------|------------|
| Cron runs but no output | `systemEvent` payload | Always use `agentTurn` |
| Images can't be opened by recipient | Direct message attachment | Upload to doc, send link |
| Logo rendering failure | Base64 too large | Resize to 90px width first |
| Infographic too small | 1x resolution | Always use 3x (3600px) |
| Voice missing | Skipped step | Mandatory checklist before delivery |

## Delivery Checklist

Before sending, verify:

- [ ] Infographic is 3600px wide
- [ ] Logo renders correctly with gold frame
- [ ] Voice MP3 generated and accessible
- [ ] Feishu doc created with image + text + voice link
- [ ] Doc link sent (NOT direct image)
- [ ] Voice file sent separately as attachment

## Customization

- **Logo path**: Set in your workspace (e.g., `workspace/scripts/logo.jpg`)
- **Template**: Customize `gen-template.py` for your brand
- **Voice**: Change `--voice` parameter for different languages/tones
- **Modules**: Adjust the 5 modules to your industry
- **Delivery target**: Set recipient Feishu/TG/WhatsApp ID

## Files Structure

```
workspace/
├── scripts/
│   ├── logo.jpg              # Your brand logo
│   └── daily-push-checklist.md
├── reports/                   # Generated images (whitelisted for upload)
├── /tmp/
│   └── gen-template.py       # HTML generation template
└── skills/
    └── daily-intelligence/
        └── SKILL.md          # This file
```

## Requirements

- Python 3.x
- Playwright (`pip install playwright && playwright install`)
- edge-tts (`pip install edge-tts`)
- Pillow (`pip install Pillow`) for image processing
- Feishu/Lark integration (for doc creation)

## License

MIT
