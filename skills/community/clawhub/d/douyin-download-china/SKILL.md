---
name: "douyin-download"
description: "抖音视频下载工具。当用户要求下载抖音（豆包）短视频时使用此 skill。支持短链接（如 v.douyin.com/xxx）和完整视频页面链接，自动解析并下载到本地。下载视频为 720p 带水印版本。"
agent_created: true
---

# douyin-download

Download Douyin (TikTok China) videos to local disk without needing yt-dlp, cookies, or login.

## Workflow

Execute all steps in order.

### Step 1 — Resolve Short URL

If the URL is a short link (`v.douyin.com/xxx`), resolve it first:

```bash
curl -sI "https://v.douyin.com/<ID>/" | grep -i location
```

Extract the full URL from the `location:` header. The numeric ID in `/video/<ID>/` is the `video_id_str` (e.g. `7634389140783615232`).

### Step 2 — Fetch Mobile Page & Extract video_id

Fetch the mobile Douyin page and extract the internal `video_id`:

```bash
curl -sL "https://www.iesdouyin.com/share/video/<video_id_str>/" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15" \
  -H "Referer: https://www.douyin.com/" \
  -o /tmp/dy_page.html
```

Extract `video_id` from the HTML:

```bash
grep -o 'video_id[^"]*"[^"]*"' /tmp/dy_page.html
```

This returns something like `video_id=v0d00fg10000d7pc7dvog65j2bpvg940`. The part after `=` is the `internal_video_id`.

### Step 3 — Download Video

Construct the snssdk play URL and download:

```bash
curl -L "https://aweme.snssdk.com/aweme/v1/playwm/?video_id=<internal_video_id>&ratio=720p&line=0" \
  -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15" \
  -H "Referer: https://www.douyin.com/" \
  -o ~/Downloads/<output_filename>.mp4
```

- `playwm` = 720p with Douyin watermark
- To get no-watermark version: replace `playwm` with `play` and append `&watermark=0` (may need additional signature handling)
- Save to `~/Downloads/` using the video title as filename

### Step 4 — Verify

Check file size and format:

```bash
ls -lh ~/Downloads/<output_filename>.mp4 && file ~/Downloads/<output_filename>.mp4
```

## Key Notes

- **No login required** — the mobile endpoint (`iesdouyin.com`) works without authentication
- **Download speed** — typically reaches 10–15 MB/s on stable connections; a 100MB video finishes in ~10 seconds
- **If download fails** with 403/redirect: retry with a fresh `curl -L` (follow redirects) and verify the `video_id` is correct
- **Watermark** — `playwm` always includes Douyin watermark; getting no-watermark requires the `play` endpoint with signed parameters (complex, not covered here)
- **Supported URLs**: `v.douyin.com/xxx` short links and `www.iesdouyin.com/share/video/<ID>/` direct links

## Reference

See `references/douyin_api.md` for detailed endpoint documentation and troubleshooting.
