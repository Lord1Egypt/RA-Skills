# Codec & Container Compatibility Matrix

## Video Codecs

| Codec | Encoder | Quality | Speed | Compatibility | Use Case |
|-------|---------|---------|-------|--------------|----------|
| H.264 | `libx264` | Good | Fast | Universal | Web, social, broadcast |
| H.265/HEVC | `libx265` | Better | Slow | Modern devices | 4K, archival, streaming |
| AV1 | `libaom-av1`, `libsvtav1` | Best | Very slow | Chrome, Firefox, Android | Web (future-proof) |
| VP9 | `libvpx-vp9` | Very Good | Medium | Chrome, Firefox | Web, YouTube |
| VP8 | `libvpx` | OK | Fast | Wide browser | Legacy web |
| ProRes | `prores_ks` | Lossless-like | Fast | macOS/Apple | Post-production |
| DNxHD/DNxHR | `dnxhd` | Lossless-like | Fast | Avid | Post-production |
| FFV1 | `ffv1` | Lossless | Medium | Open source | Archival |
| MJPEG | `mjpeg` | Variable | Fast | Wide | Capture cards |
| Theora | `libtheora` | OK | Medium | Open source | Legacy web |

## Audio Codecs

| Codec | Encoder | Bitrate Range | Compatibility | Use Case |
|-------|---------|--------------|--------------|----------|
| AAC | `aac`, `libfdk_aac` | 64-320k | Universal | Standard output |
| MP3 | `libmp3lame` | 32-320k (VBR q0-9) | Universal | Legacy/podcast |
| Opus | `libopus` | 6-510k | Modern browsers | Web, VoIP, streaming |
| FLAC | `flac` | Lossless | Wide | Archival, audiophile |
| WAV/PCM | `pcm_s16le`, `pcm_s24le` | Uncompressed | Universal | Editing, broadcast |
| Vorbis | `libvorbis` | 45-500k | Browsers | Web (WebM) |
| AC3 | `ac3` | 32-640k | Broadcast/Blu-ray | Surround sound |
| DTS | `dca` | Variable | Blu-ray/Disc | Surround sound |
| ALAC | `alac` | Lossless | Apple | Apple ecosystem |

## Container Formats

| Container | Extension | Video Codecs | Audio Codecs | Subtitles | Notes |
|-----------|-----------|-------------|-------------|-----------|-------|
| MP4 (MPEG-4) | `.mp4`, `.m4v` | H.264, H.265, AV1 | AAC, MP3 | mov_text | Most compatible |
| MKV (Matroska) | `.mkv` | Any | Any | SRT, ASS, PGS | Best flexibility |
| MOV (QuickTime) | `.mov` | H.264, ProRes | AAC, PCM | mov_text | Apple native |
| WebM | `.webm` | VP8, VP9, AV1 | Vorbis, Opus | WebVTT | Web-only |
| AVI | `.avi` | DivX, MPEG-2 | MP3, PCM | None | Legacy |
| FLV | `.flv` | H.264 | AAC, MP3 | None | RTMP streaming |
| TS (MPEG-TS) | `.ts` | H.264, H.265 | AAC, AC3 | DVB | Broadcast, HLS |
| M2TS | `.m2ts` | H.264, H.265 | AC3, DTS | PGS | Blu-ray |
| OGV | `.ogv` | Theora | Vorbis | None | Open source |
| F4V | `.f4v` | H.264 | AAC | None | Adobe Flash |
| 3GP | `.3gp` | H.263, H.264 | AAC, AMR | None | Mobile |

## Codec Selection Guide

### For maximum compatibility (must play everywhere):
```
Video: libx264, profile:v high, level 4.0, pix_fmt yuv420p
Audio: aac, 192k
Container: .mp4 with -movflags +faststart
```

### For best quality at smallest size (modern platforms):
```
Video: libx265 (H.265) or libaom-av1 (AV1)
Audio: libopus 128k
Container: .mp4 (H.265) or .webm (AV1)
```

### For post-production (preserve quality for editing):
```
Video: prores_ks (profile 3=HQ) or dnxhd
Audio: pcm_s24le (24-bit WAV)
Container: .mov (ProRes) or .mxf (DNxHD)
```

### For web streaming (fastest to start playback):
```
Video: libx264 with -movflags +faststart
Audio: aac 128k
Container: .mp4
```

### For lossless archival:
```
Video: ffv1 (lossless, open standard)
Audio: flac (lossless)
Container: .mkv
```

## Pixel Formats
- `yuv420p` — 4:2:0, most compatible, required for H.264 in MP4
- `yuv422p` — 4:2:2, better chroma, used in ProRes/DNxHD
- `yuv444p` — 4:4:4, best chroma, professional only
- `yuvj420p` — legacy JPEG YUV, avoid in new work
- `rgb24` — uncompressed RGB, for image sequences
- `rgba` — uncompressed RGBA with alpha channel

## FFmpeg Codec Availability Check
```bash
# List all available encoders
ffmpeg -encoders 2>&1

# Check if specific encoder is available
# macOS / Linux
ffmpeg -encoders 2>&1 | grep libx265
ffmpeg -encoders 2>&1 | grep libfdk_aac

# Windows (PowerShell)
ffmpeg -encoders 2>&1 | Select-String libx265
ffmpeg -encoders 2>&1 | Select-String libfdk_aac

# List available decoders
ffmpeg -decoders 2>&1

# List available formats
ffmpeg -formats 2>&1
```
