# Royalty-Free Music Sources for marathon-clip

The default track is from archive.org and is CC/PD licensed. Other reliable sources for swap-in music:

## archive.org (direct mp3 download works)
Use the `ia*.us.archive.org` mirror, not `archive.org/download/...` (the latter often returns 500 from server IPs).

```bash
# Discover files in a collection
curl -sL "https://archive.org/metadata/<identifier>" | jq '.files[] | select(.name | endswith(".mp3"))'

# Download (use the dir field for the mirror)
curl -sL -A "Mozilla/5.0" -o music-full.mp3 \
  "https://ia<NNN>.us.archive.org/<server>/items/<identifier>/<filename>.mp3"
```

Useful collections:
- `UpbeatAndHappyBackgroundMusic` — used as default
- `jamendo-418443` — DepasRec "Upbeat positive motivational electronic"
- `jamendo-564783` — DHDMusic "Corporate Upbeat Motivation 30sec Loop"
- `freemusicarchive` — the FMA collection mirror

## Free Music Archive
https://freemusicarchive.org/ — needs HTML scraping for the actual `.mp3` URL.

## Pixabay / Chosic / Mixkit
Blocked from server IPs (Cloudflare / hotlinking). Download locally and `scp` to the server, or use a residential proxy.

## Trim + fade with ffmpeg

```bash
ffmpeg -y -i source.mp3 -ss 0 -t 30 \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=28.5:d=1.5" \
  -ac 2 -ar 44100 -b:a 192k music.mp3
```

Place the result at `~/.openclaw/workspace/projects/sahi-video/public/music.mp3` (the Remotion `staticFile()` path).

## Licensing checklist before using

- Confirm CC0 / CC-BY / PD on the source page
- For CC-BY: add a credit line in the video outro or caption
- Re-check yearly — public-domain claims sometimes get challenged
