# Optimization Guide

## Title Optimization Strategy
- **Standard Structure**: `[Brand] + [Core Keyword] + [Feature] + [Spec]`
- Avoid "Hot Search" markers and keyword stuffing.
- Choose 2‑3 top hot keywords and embed naturally.
- Example:
  - ❌ `Blue Buffalo Hot Search: wet cat food, dry cat food`
  - ✅ `Blue Buffalo Tastefuls Flaked Wet Cat Food, High Protein Natural Ingredients with Real Fish, 3 oz Cans (Pack of 24)`

## Image Generation Prompts
Generate **5** scene‑based images per product using Taobao MCP.
| Position | Scene | Prompt Highlights |
|---|---|---|
| Main Image | Cozy Living Room | Modern home, soft lighting, product in use |
| Detail 1 | Bedroom Bedside | Warm morning light, relaxed atmosphere |
| Detail 2 | Close‑up | Showcase material texture, quality |
| Detail 3 | Pet Usage | Happy pet interacting, lifestyle vibe |
| Detail 4 | Sunny Reading Corner | Golden hour, contemporary décor |
| Detail 5 | Reuse Main Image | Consistency with main visual |

## CTR Monitoring Details
- **Threshold**: 5 % CTR (adjustable)
- **Schedule**: Daily at 10:00 AM
- **Report**: Summarize total products, count below threshold, and recommend new main images.
- **Action**: Flag low‑CTR items for image regeneration.

## Dependencies
- **MCP Service**: Taobao `opc` service ID `19cf03a191f`
- **Python Packages**: `requests>=2.28.0`, `beautifulsoup4>=4.11.0`
