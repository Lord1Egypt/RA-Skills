# Platform-Specific Encoding Presets

Ready-to-use ffmpeg commands for 20+ platforms. Replace `"input.mp4"` with your source file.

## Video Platforms

### YouTube (1080p, high quality)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 18 -preset slow -profile:v high -level 4.0 \
  -c:a aac -b:a 384k -ar 48000 -ac 2 \
  -pix_fmt yuv420p -r 29.97 \
  -movflags +faststart \
  "youtube_1080p.mp4"
```

### YouTube Shorts (Vertical 9:16, 60s max)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 256k -ar 48000 \
  -pix_fmt yuv420p -t 60 \
  -movflags +faststart \
  "youtube_short.mp4"
```

### Vimeo (1080p, excellent quality)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 16 -preset slow -profile:v high \
  -c:a aac -b:a 320k -ar 48000 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "vimeo_1080p.mp4"
```

### TikTok (9:16, H.264, max 4GB / 60min)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 192k -ar 44100 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "tiktok.mp4"
```

### Instagram Reels (9:16, max 90s, 4GB)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 192k -ar 44100 \
  -pix_fmt yuv420p -t 90 \
  -movflags +faststart \
  "instagram_reel.mp4"
```

### Instagram Feed (1:1 square or 4:5 portrait)
```bash
# 1:1 Square
ffmpeg -i "input.mp4" \
  -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -crf 23 -preset slow \
  -c:a aac -b:a 192k -ar 44100 \
  -pix_fmt yuv420p -t 60 \
  -movflags +faststart \
  "instagram_square.mp4"
```

### Twitter/X (max 512MB, 2:20 duration, 1280x720)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -b:v 5000k -maxrate 5000k -bufsize 10000k \
  -c:a aac -b:a 192k -ar 44100 \
  -pix_fmt yuv420p -t 140 \
  -movflags +faststart \
  "twitter.mp4"
```

### Facebook (1080p, H.264)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 -preset slow -profile:v high \
  -c:a aac -b:a 256k -ar 44100 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "facebook.mp4"
```

## Streaming Services

### Twitch Live (RTMP, 6000kbps recommended)
```bash
ffmpeg -re -i "input.mp4" \
  -c:v libx264 -preset veryfast -b:v 6000k -maxrate 6000k -bufsize 12000k \
  -pix_fmt yuv420p -g 60 -keyint_min 60 \
  -c:a aac -b:a 160k -ar 44100 \
  -f flv "rtmp://live.twitch.tv/app/STREAMKEY"
```

### OBS Virtual Camera Output (high quality, low latency)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -preset ultrafast -tune zerolatency -crf 18 \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  "obs_output.mp4"
```

## Mobile Platforms

### iOS (H.264, AAC, MP4 — maximum compatibility)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -profile:v high -level 4.0 -crf 23 \
  -c:a aac -b:a 192k -ar 44100 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "ios_compatible.mp4"
```

### Android (H.264 or VP9)
```bash
ffmpeg -i "input.mp4" \
  -c:v libvpx-vp9 -crf 33 -b:v 0 \
  -c:a libopus -b:a 128k \
  "android.webm"
```

## Professional / Post-Production

### Apple ProRes 422 HQ (editing, macOS)
```bash
ffmpeg -i "input.mp4" \
  -c:v prores_ks -profile:v 3 \
  -c:a pcm_s16le \
  "prores_hq.mov"
```

### Apple ProRes 4444 (with alpha channel)
```bash
ffmpeg -i "input_with_alpha.mov" \
  -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le \
  -c:a pcm_s16le \
  "prores_4444.mov"
```

### Avid DNxHD 185 (1080p/29.97, editing)
```bash
ffmpeg -i "input.mp4" \
  -c:v dnxhd -b:v 185M \
  -c:a pcm_s16le \
  "dnxhd_185.mxf"
```

### Lossless Archival (FFV1 + FLAC in MKV)
```bash
ffmpeg -i "input.mp4" \
  -c:v ffv1 -level 3 -coder 1 -context 1 -g 1 -slices 24 \
  -c:a flac \
  "archive_lossless.mkv"
```

## Web / HTML5

### Web MP4 (H.264, maximum compatibility)
```bash
ffmpeg -i "input.mp4" \
  -c:v libx264 -crf 23 -preset slow -profile:v high -level 4.0 \
  -c:a aac -b:a 128k \
  -pix_fmt yuv420p \
  -movflags +faststart \
  "web.mp4"
```

### Web WebM (VP9, Chrome/Firefox)
```bash
ffmpeg -i "input.mp4" \
  -c:v libvpx-vp9 -crf 33 -b:v 0 \
  -c:a libopus -b:a 128k \
  "web.webm"
```

### Optimized GIF (web, under 5MB)
```bash
# Step 1: palette
ffmpeg -i "input.mp4" -ss 0 -t 10 \
  -vf "fps=12,scale=400:-1:flags=lanczos,palettegen=stats_mode=diff" \
  -y palette.png

# Step 2: encode
ffmpeg -i "input.mp4" -i palette.png -ss 0 -t 10 \
  -filter_complex "fps=12,scale=400:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5" \
  -y "output.gif"
```

## Messaging Platforms

### Discord (max 8MB for free users)
```bash
# Auto-calculate bitrate for 8MB target
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "input.mp4")
VBR=$(python3 -c "print(int(8*1024*8 / $DURATION - 128))")
ffmpeg -i "input.mp4" \
  -c:v libx264 -b:v "${VBR}k" -pass 1 -an -f null - && \
ffmpeg -i "input.mp4" \
  -c:v libx264 -b:v "${VBR}k" -pass 2 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  "discord.mp4"
```

### WhatsApp (max 16MB, max 3min)
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=640:-2" \
  -c:v libx264 -b:v 500k -pass 1 -an -f null - && \
ffmpeg -i "input.mp4" \
  -vf "scale=640:-2" \
  -c:v libx264 -b:v 500k -pass 2 \
  -c:a aac -b:a 64k \
  -t 180 \
  "whatsapp.mp4"
```

## Podcast / Audio Only

### Podcast MP3 (stereo, 192kbps)
```bash
ffmpeg -i "input.wav" \
  -c:a libmp3lame -q:a 2 -ac 2 \
  -metadata title="Episode Title" \
  -metadata artist="Podcast Name" \
  "podcast.mp3"
```

### Audiobook (mono, loudness-normalized)
```bash
# Pass 1: measure — run this first and note the JSON values printed at the end
ffmpeg -i "input.mp3" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json" \
  -f null - 2>&1 | tail -n 20

# Pass 2: apply — replace measured_* values with the numbers from Pass 1 output
ffmpeg -i "input.mp3" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=<measured_I>:measured_TP=<measured_TP>:measured_LRA=<measured_LRA>:measured_thresh=<measured_thresh>:offset=<target_offset>:linear=true" \
  -ac 1 -ar 22050 \
  -c:a libmp3lame -q:a 4 \
  "audiobook.mp3"
# Note: Pass 2 requires the actual measured values from Pass 1.
# Using linear=true without them falls back to single-pass estimation.
```
