# FFmpeg Flag Reference

## Global Options (before all -i inputs)

| Flag | Values | Description |
|------|--------|-------------|
| `-y` | — | Overwrite output without asking |
| `-n` | — | Never overwrite (skip if exists) |
| `-loglevel` | `quiet`, `error`, `warning`, `info`, `verbose`, `debug` | Log verbosity (default: `info`) |
| `-v` | same as loglevel | Alias for `-loglevel` |
| `-hide_banner` | — | Suppress build info banner |
| `-stats` | — | Print encoding progress stats |
| `-nostats` | — | Suppress encoding progress |
| `-progress url` | `pipe:1`, file path | Machine-readable progress output |
| `-benchmark` | — | Show CPU time at end |
| `-threads` | integer | Number of CPU threads (0=auto) |
| `-cpuflags` | flags | Set CPU feature flags |

## Input Options (before -i)

| Flag | Values | Description |
|------|--------|-------------|
| `-i` | path/URL | Input file (required) |
| `-ss` | `HH:MM:SS[.ms]` or seconds | Start position (BEFORE -i = fast keyframe seek) |
| `-t` | `HH:MM:SS[.ms]` or seconds | Duration to read |
| `-to` | `HH:MM:SS[.ms]` or seconds | End position |
| `-itsoffset` | seconds | Shift input timestamps |
| `-r` | fps | Override input frame rate |
| `-f` | format name | Force input format |
| `-re` | — | Read at native frame rate (for streaming) |
| `-stream_loop` | -1, 0, N | Loop input: -1=infinite, N=N times |
| `-analyzeduration` | microseconds | Max time to analyze (increase for broken files) |
| `-probesize` | bytes | Max data to probe (increase for broken files) |

## Output Video Options

| Flag | Values | Description |
|------|--------|-------------|
| `-c:v` / `-vcodec` | codec name | Video encoder (`copy`, `libx264`, `libx265`, etc.) |
| `-crf` | 0–51 (H.264), 0–63 (VP9) | Constant Rate Factor (quality; lower=better) |
| `-b:v` | e.g. `2M`, `500k` | Target video bitrate |
| `-maxrate` | e.g. `4M` | Maximum bitrate (use with `-bufsize`) |
| `-bufsize` | e.g. `8M` | Rate control buffer size |
| `-preset` | `ultrafast`→`veryslow` | Speed/compression trade-off (x264/x265) |
| `-tune` | `film`, `animation`, `grain`, `stillimage`, `fastdecode`, `zerolatency` | Content-specific optimization |
| `-profile:v` | `baseline`, `main`, `high` | H.264 profile (compatibility) |
| `-level` | e.g. `4.0`, `4.1`, `5.1` | H.264/H.265 level |
| `-pix_fmt` | `yuv420p`, `yuv422p`, etc. | Pixel format |
| `-r` | fps | Output frame rate |
| `-s` | `WxH` | Output resolution (prefer `-vf scale` instead) |
| `-aspect` | `16:9`, `4:3` | Set display aspect ratio |
| `-vf` | filter string | Video filter chain |
| `-vn` | — | No video stream in output |
| `-vframes` | integer | Number of video frames to encode |
| `-g` | integer | GOP size (keyframe interval) |
| `-keyint_min` | integer | Minimum keyframe interval |
| `-sc_threshold` | integer | Scene change threshold |
| `-pass` | `1` or `2` | Two-pass encoding |
| `-passlogfile` | path | Two-pass stats file prefix |

## Output Audio Options

| Flag | Values | Description |
|------|--------|-------------|
| `-c:a` / `-acodec` | codec name | Audio encoder (`copy`, `aac`, `libmp3lame`, etc.) |
| `-b:a` | e.g. `192k`, `320k` | Audio bitrate |
| `-q:a` | 0–9 | VBR quality (MP3: 0=best, 9=worst) |
| `-ar` | Hz | Audio sample rate (e.g. `44100`, `48000`) |
| `-ac` | integer | Audio channels (1=mono, 2=stereo, 6=5.1) |
| `-af` | filter string | Audio filter chain |
| `-an` | — | No audio stream in output |
| `-vol` | 0–256 | Audio volume (256=normal, 512=double) |
| `-channel_layout` | `stereo`, `5.1`, etc. | Set channel layout |

## Stream Mapping

| Flag | Values | Description |
|------|--------|-------------|
| `-map` | `input:stream` | Select specific streams |
| `-map 0` | — | All streams from first input |
| `-map 0:v:0` | — | First video stream from first input |
| `-map 0:a:0` | — | First audio stream from first input |
| `-map 0:s:0` | — | First subtitle stream from first input |
| `-map -0:s` | — | Exclude all subtitles from input 0 |
| `-map_metadata` | `0`, `-1` | Copy or strip metadata |
| `-map_chapters` | `0`, `-1` | Copy or strip chapters |

## Container/Mux Options

| Flag | Values | Description |
|------|--------|-------------|
| `-f` | format name | Force output format |
| `-movflags +faststart` | — | Move moov to front (MP4 web streaming) |
| `-movflags +frag_keyframe` | — | Fragmented MP4 (streaming) |
| `-fflags +genpts` | — | Generate missing PTS values |
| `-avoid_negative_ts` | `make_zero` | Fix negative timestamps |
| `-copyts` | — | Copy input timestamps unchanged |
| `-start_at_zero` | — | Shift timestamps to start at 0 |

## Subtitle Options

| Flag | Values | Description |
|------|--------|-------------|
| `-c:s` | codec name | Subtitle codec (`copy`, `mov_text`, `srt`, `ass`) |
| `-sn` | — | No subtitle streams |

## Metadata

| Flag | Values | Description |
|------|--------|-------------|
| `-metadata key=value` | string | Set metadata (title, artist, etc.) |
| `-metadata:s:v:0 key=value` | string | Set stream-level metadata |

## HLS Options

| Flag | Values | Description |
|------|--------|-------------|
| `-hls_time` | seconds | Segment duration |
| `-hls_list_size` | integer | Number of segments in playlist (0=all) |
| `-hls_playlist_type` | `vod`, `event` | Playlist type |
| `-hls_segment_filename` | pattern | Segment filename template |
| `-hls_flags` | `delete_segments`, `append_list` | HLS behavior flags |

## CRF Quality Guides

### H.264 (`libx264`)
- `18` — Visually lossless (large files)
- `23` — Default, good balance
- `28` — Acceptable for web/social
- `32+` — Noticeable quality loss

### H.265 (`libx265`)
- `24` — Visually lossless
- `28` — Default, ~50% smaller than x264@23
- `32` — Acceptable quality
- `36+` — Noticeable quality loss

### VP9 (`libvpx-vp9`)
- `31` — High quality
- `33` — Default good balance
- `40+` — Reduced quality

### AV1 (`libaom-av1`)
- `23` — Very high quality
- `30` — Good balance
- `40+` — Reduced quality
