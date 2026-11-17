# Bundled meme pack

`official-001/` ships:

| File | Purpose |
|------|---------|
| `memes/<tag>/*` | Sticker images |
| `index.db` | Captions + FTS + **embedding-3 vectors** (portable relative paths) |
| `manifest.json` | Category metadata |
| `CREDITS.md` | Upstream image credits |

Install scripts copy this pack to `$MEME_HOME/meme-packs/official-001/` when missing.
Scripts also fall back to this directory if no local pack is configured.

Images: [astrbot-meme-pack-official-01](https://github.com/anka-afk/astrbot-meme-pack-official-01).
