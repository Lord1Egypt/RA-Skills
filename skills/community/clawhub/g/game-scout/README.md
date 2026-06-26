# Game Scout

A video game strategy specialist. Game Scout amalgamates tactics, builds, and guides from across the web — Reddit, YouTube creators, gaming wikis, Twitter/X, and game databases — to unlock a higher gaming experience. It finds what the best players are doing right now, validates it across multiple sources, and delivers it ready to use.

## What You Can Ask

- "What are the best SMG builds in Marathon right now?"
- "Is bleed still meta in Elden Ring after the latest patch?"
- "What does the Xenotech Gauntlet do?"
- "What are pros running in Valorant?"
- "Best budget weapons in Marathon?"
- "How does crit work in Path of Exile 2?"

Works with any game — just ask naturally.

## What You Get

- **Current meta, not stale guides** — pulls from live community discussion, not cached articles from three patches ago
- **Video guide intel without the videos** — extracts the actual builds and strategies from 20-minute YouTube guides in seconds
- **Community-validated** — cross-references Reddit, pro players, and guide creators so you know what's actually working
- **Patch-aware** — flags outdated info before you waste time on a nerfed build
- **Ready to use** — exact loadouts, stat breakdowns, and step-by-step strategies

## Setup

Requires API keys from [Exa AI](https://exa.ai) and [Bright Data](https://brightdata.com) (both have free tiers). Add them to `~/.openclaw/.env`:

```bash
EXA_API_KEY=your-key
BRIGHTDATA_API_KEY=your-key
BRIGHTDATA_ZONE=your-zone-name
```

For `BRIGHTDATA_ZONE`, create a Web Unlocker zone in your [Bright Data dashboard](https://brightdata.com/cp/zones) and use its name.

Also needs `yt-dlp` for YouTube transcripts: `brew install yt-dlp`

## License

MIT
