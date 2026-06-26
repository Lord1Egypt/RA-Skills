# AI Product Space — OpenClaw Skill

> 一张白底产品图，AI 自动生成电商全套素材

Upload a single product photo and generate a full suite of ecommerce assets: main images, scene shots, feature posters, marketing copy, and 8-second showcase videos.

## Features

| Capability | Description |
|------------|-------------|
| Full Pipeline | One-click generation of 20+ product images and marketing copy |
| Scene Images | AI-generated lifestyle and contextual product shots |
| Feature Posters | Selling-point highlight images with text overlays |
| Marketing Copy | Multi-paragraph product descriptions and ad copy |
| Video | 8-second product showcase video from still images |
| 10 Languages | zh, en, ja, ko, fr, de, es, pt, ar, ru |

## Installation

### From ClawHub (Recommended)

```bash
clawhub install ai-product-space
```

Or ask OpenClaw directly:

> "帮我安装 ai-product-space 技能"

### Manual Installation

```bash
git clone https://github.com/renshevy/ai-product-space.git
cd openclaw-skill
npm install && npm run build
cp -r . ~/.openclaw/workspace/skills/ai-product-space
```

## Authorization

### OAuth One-Click (Recommended)

On first use, OpenClaw automatically opens a browser window for you to log in and authorize. Click **"Allow"** and you're connected — no API keys to copy.

### Manual API Key (Offline / Headless)

1. Log in to your AI Product Space instance
2. Go to **Settings > API Keys** and create a new key
3. Add to your OpenClaw config:

```json
{
  "APS_BASE_URL": "https://renshevy.com",
  "APS_API_KEY": "aps_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `create_space` | Create a new product workspace |
| `upload_product_image` | Upload a product photo (local file or URL) |
| `run_ecommerce_pipeline` | Run full asset generation pipeline |
| `generate_single_image` | Generate custom scene/style images from prompt |
| `generate_video` | Generate 8-second showcase video |
| `get_space_status` | Check workspace and pipeline progress |
| `list_assets` | Browse generated assets |

## Quick Start

```
You: 帮我生成蓝牙耳机的电商素材

→ create_space("蓝牙耳机")
→ upload_product_image(space_id, "earbuds.jpg")
→ run_ecommerce_pipeline(space_id, language="zh")

Result: 22 product images + 6 marketing copy segments generated
```

See the `examples/` directory for more detailed conversation flows.

## Permissions

| Permission | Why |
|------------|-----|
| `network` | Calls AI Product Space API over HTTPS for all generation operations |
| `filesystem` | Reads local image files when user provides a file path for upload |

## Requirements

- OpenClaw >= 0.8.0
- Node.js >= 18
- An [AI Product Space](https://renshevy.com) account with available credits

## Development

```bash
npm install
npm run build      # Compile TypeScript
npm run dev        # Watch mode
```

## License

MIT
