---
name: crypto-content-crafter
description: >
  Generate all NFT/crypto collection content from a single product name. Use when user needs
  NFT collection descriptions, roadmap content, Twitter threads, Discord welcome messages, or
  any crypto/NFT marketing copy. Triggers: create NFT collection content, write crypto
  collection description, NFT drop content, generate crypto twitter thread, NFT roadmap,
  crypto launch content, NFT marketing copy
---

# Crypto Content Crafter

Generate complete NFT/crypto collection launch content from a single product name and description.

## Quick Start

Load the reference templates, then use the generate script or craft content directly.

## Workflow

1. Load reference templates: `references/templates.md`
2. Gather: collection name, tagline, theme, mint price, supply, mint date
3. Generate each content piece using templates as guides
4. Output all pieces in a single organized response

## Generated Content Pieces

| Piece | Description |
|-------|-------------|
| Collection Description | 150-300 word landing page copy |
| Short Description | 1-2 sentence pitch |
| Twitter Thread | 5-7 tweet thread for launch |
| Discord Welcome | Onboarding message for new holders |
| Roadmap | 4-phase timeline content |
| Tokenomics Blurb | Supply/utility explanation |

## Script Usage

```bash
uv run python scripts/generate_content.py --name "CyberPunk Zebras" --tagline "Neon meets nature" --supply 5555 --price 0.05 --date "2026-06-01"
```

For interactive mode (prompts for all values):
```bash
uv run python scripts/generate_content.py --interactive
```

## Tips

- Always ask for collection theme/vibe if not provided
- Include floor price history references for similar collections
- Add urgency elements for mint date countdown
- Tailor Twitter thread to build community, not just sell
