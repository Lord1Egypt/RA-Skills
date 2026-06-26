# Audio-Video Skill — Feature Overview

A complete reference of every capability in this skill, organized by section.

---

## SECTION A — Format Conversion & Transcoding

Convert and transcode between any video format or codec. Handles the full range from modern codecs (AV1, HEVC) to universal compatibility (H.264), with hardware acceleration on all major platforms.

**Capabilities:**
- Transcode to H.264, H.265/HEVC, AV1, VP9/WebM
- Hardware-accelerated encoding: VideoToolbox (macOS), NVENC (NVIDIA), QSV (Intel)
- Container remux (MP4 ↔ MKV ↔ MOV) without re-encoding via stream copy
- Convert PNG/JPEG image sequences into video
- Extract video frames as image sequences (all frames, at specific fps, keyframes only)

**Key tools:** `libx264`, `libx265`, `libaom-av1`, `libvpx-vp9`, `h264_videotoolbox`, `h264_nvenc`, `-c copy`, `-crf`, `-preset`, `-movflags +faststart`

**Example Use Cases:**

1. **Uploading to a platform that only accepts MP4/H.264** — Transcode any source (MKV, MOV, AVI, HEVC) to a universally compatible H.264 MP4 with one command.

2. **Archiving at smaller file sizes** — Re-encode old H.264 files to H.265 or AV1 to cut file size by 40–60% at the same visual quality. Useful for long-term storage where disk space matters.

3. **Changing containers without re-encoding** — Remux MKV to MP4 (or vice versa) in seconds via stream copy. No quality loss, no waiting — just restructures the container around the existing streams.

4. **Creating a video from a photo sequence** — Convert a timelapse or animation render (PNG sequence) into a video file, controlling the output fps independently of the input frame count.

5. **Extracting frames for machine learning or review** — Pull every frame, every Nth frame, or only keyframes from a video as individual images for dataset building or manual review.

---

## SECTION B — Audio Processing

Extract, convert, filter, and analyze audio from any media file. Covers everything from simple format conversion to EBU R128 broadcast-standard loudness normalization.

**Capabilities:**
- Extract audio tracks as AAC, MP3, FLAC, WAV, or Opus
- Convert between audio formats; downmix multi-channel to stereo; change sample rate
- EBU R128 loudness normalization (two-pass, broadcast standard)
- Audio filters: volume adjustment, high-pass, low-pass, noise reduction, dynamic range compression, fade in/out, stereo↔mono
- Advanced: remove silence, change speed with pitch preservation (0.5–2.0×), pitch shift without tempo change, generate waveform stats, generate spectrogram PNG

**Key tools:** `libmp3lame`, `loudnorm`, `highpass`, `lowpass`, `anlmdn`, `acompressor`, `afade`, `silenceremove`, `atempo`, `showspectrumpic`

**Example Use Cases:**

1. **Extracting audio from a video for a podcast or music release** — Pull the audio track from any video as MP3, AAC, FLAC, or WAV without touching the video stream.

2. **Normalizing loudness before publishing a podcast** — Apply EBU R128 two-pass normalization so every episode hits the same loudness target (-16 LUFS for Apple Podcasts, -14 LUFS for Spotify) regardless of how it was recorded.

3. **Cleaning up a noisy recording** — Chain high-pass (remove low rumble/hum), `anlmdn` noise reduction, and dynamic range compression to make a poor-quality microphone recording more listenable.

4. **Speeding up an audiobook or lecture** — Use `atempo` to play back at 1.5× or 2× speed with pitch preserved, producing a natural-sounding faster version rather than a chipmunk effect.

5. **Generating a spectrogram for audio QA** — Visualize the frequency content of an audio file as a PNG to spot noise floors, clipping, or encoding artifacts before delivery.

---

## SECTION C — Video Editing

The full editing toolkit: cut, join, resize, rotate, crop, overlay, and color grade — all without leaving FFmpeg.

**Capabilities:**
- **Trim & cut:** Fast keyframe-accurate trim (stream copy) or frame-accurate trim (re-encode); remove specific time ranges
- **Concatenation:** Join same-codec files without re-encoding; join different codecs/resolutions with re-encode
- **Scaling:** Resize to exact dimensions or platform targets (4K, 1080p, 720p, 480p); preserve aspect ratio with padding
- **Frame rate:** Change fps; smooth slow-motion via frame interpolation (`minterpolate`)
- **Rotation & flipping:** 90°/180° rotation, horizontal/vertical flip, auto-rotate from phone metadata
- **Cropping:** Crop to coordinates, square center crop, auto-detect and remove black bars (`cropdetect`)
- **Overlays & watermarks:** Image watermark, text watermark with custom font/color/alpha, timed animated overlays, picture-in-picture (PiP)
- **Color grading:** Brightness, contrast, saturation, gamma; LUT (`.cube`) color grading; curves (S-curve); hue/saturation shift

**Key tools:** `fps`, `minterpolate`, `transpose`, `vflip`, `hflip`, `crop`, `cropdetect`, `overlay`, `drawtext`, `eq`, `lut3d`, `curves`, `hue`, `scale`, `filter_complex`

**Example Use Cases:**

1. **Trimming a highlight clip from a long recording** — Cut a specific segment from a 2-hour recording in seconds using stream copy (no re-encode, instant output). Use frame-accurate trim when you need to cut on an exact frame rather than the nearest keyframe.

2. **Joining multiple recordings into one file** — Concatenate episodes, segments, or daily recordings into a single file. Same-codec files join without re-encoding; mixed sources are handled with automatic re-encode.

3. **Resizing for a specific platform** — Scale a 4K master down to 1080p, 720p, or any platform target while automatically preserving the aspect ratio and padding with black bars if needed.

4. **Fixing a video shot in portrait mode on a phone** — Auto-rotate using the metadata flag (`-metadata:s:v rotate=0`) or transpose filter to correct sideways or upside-down footage.

5. **Adding a branded watermark to every video** — Overlay a logo PNG at a fixed position with configurable opacity. Apply to a single file or use with batch processing (Section I) to brand an entire library.

6. **Color grading with a LUT** — Apply a `.cube` LUT from any color grading tool (DaVinci Resolve, Lightroom exports, free LUT packs) to give footage a consistent look without a GUI editor.

---

## SECTION D — Subtitles & Captions

Add, remove, convert, and embed subtitle tracks in any format.

**Capabilities:**
- Burn subtitles permanently into video (hard subtitles, not removable)
- Add soft subtitle tracks that viewers can toggle on/off
- Extract subtitle tracks from MKV, MP4, and other containers
- Convert between SRT and ASS/SSA formats
- Tag subtitle tracks with language metadata

**Key tools:** `subtitles` filter, `mov_text`, `-c:s`, `-metadata:s:s:0 language=`

**Example Use Cases:**

1. **Burning subtitles for social media** — Hard-burn SRT or ASS subtitles into the video so they always show regardless of player or platform — essential for silent autoplay on Instagram, TikTok, and LinkedIn.

2. **Adding soft subtitles for a streaming platform** — Embed toggleable subtitle tracks in MKV or MP4 without burning them in, so viewers can turn them on/off. Add multiple language tracks to the same file.

3. **Extracting subtitles from a downloaded MKV** — Pull the subtitle track out as a standalone `.srt` or `.ass` file for editing or translation.

4. **Converting subtitle formats** — Convert SRT to ASS for advanced styling (custom fonts, colors, positioning) or back to SRT for platforms that only accept plain subtitles.

---

## SECTION E — Thumbnails & Screenshots

Extract frames and generate thumbnails for any use — preview images, video players, web galleries.

**Capabilities:**
- Extract a single frame at any timestamp
- Generate high-quality PNG thumbnails
- Auto-select the "best" frame (highest scene complexity)
- Sprite sheets / contact sheets: multiple thumbnails tiled into a grid image
- Extract one thumbnail every N seconds (for timeline preview strips)

**Key tools:** `-ss`, `-vframes 1`, `thumbnail` filter, `scale`, `tile`, `fps`

**Example Use Cases:**

1. **Generating a YouTube upload thumbnail** — Extract the best-looking frame from a video automatically, or pull from a specific timestamp, as a high-quality PNG ready for upload.

2. **Building a video preview strip** — Extract one frame every 10 seconds and tile them into a contact sheet. Used by video players and streaming platforms to show a timeline preview when hovering over the progress bar.

3. **Creating a preview image for a web gallery** — Auto-select the highest-quality frame (avoiding black fades and blurry motion) so the thumbnail actually represents the content.

4. **Extracting a still from a specific moment** — Pull a single frame at an exact timestamp for use in documentation, blog posts, or as a reference image.

---

## SECTION F — Streaming & Adaptive Bitrate

Produce industry-standard streaming outputs — HLS, DASH, and live RTMP — from any source.

**Capabilities:**
- **HLS:** Generate segments + `.m3u8` playlist; multi-bitrate ABR ladder (1080p/720p/480p) with master playlist
- **DASH:** Generate `.mpd` manifest with segmented output for MPEG-DASH delivery
- **RTMP live streaming:** Stream to Twitch, YouTube, or any RTMP endpoint; screen capture to RTMP

**Key tools:** `-hls_time`, `-hls_playlist_type`, `-hls_segment_filename`, `-var_stream_map`, `-master_pl_name`, `-f dash`, `-seg_duration`, `-f flv`, `-re`, `-g`

**Example Use Cases:**

1. **Self-hosting video on your own server** — Generate HLS segments and a `.m3u8` playlist so any browser can stream your video natively via `<video>` without a CDN or third-party video host.

2. **Multi-bitrate adaptive streaming** — Produce an ABR ladder (1080p, 720p, 480p) with a master playlist so the player automatically switches quality based on the viewer's connection speed — the same approach used by Netflix and YouTube.

3. **Going live to Twitch or YouTube** — Stream a local video file or screen capture directly to any RTMP endpoint with a single ffmpeg command — no OBS required for simple use cases.

4. **DASH delivery for cross-platform compatibility** — Generate an MPEG-DASH `.mpd` manifest for platforms or players that prefer DASH over HLS (common in Android and browser-based players).

---

## SECTION G — Screen & Webcam Capture

Record your screen and webcam natively on every platform — no third-party tools needed.

**Capabilities:**
- **Screen recording:** macOS (AVFoundation), Linux (x11grab / PipeWire), Windows (gdigrab) — with audio capture
- **Webcam capture:** macOS (AVFoundation), Linux (v4l2), Windows (dshow) — custom resolution and framerate
- List available input devices on each platform

**Key tools:** `-f avfoundation`, `-f x11grab`, `-f pipewire`, `-f gdigrab`, `-f v4l2`, `-f dshow`

**Example Use Cases:**

1. **Recording a screen tutorial without installing software** — Capture your screen with system audio directly via ffmpeg on any platform. No OBS, Loom, or QuickTime required.

2. **Capturing webcam footage for a talking-head recording** — Record directly from a webcam at a specific resolution and framerate, with audio, into any output format.

3. **CI/CD pipeline screen capture** — Automate screen recording in a headless Linux environment (x11grab) for visual regression testing or demo generation.

4. **Discovering available input devices** — List all cameras and audio inputs on the system before writing a capture command, so you know the exact device name to use.

---

## SECTION H — GIF & Animated Images

Convert video to high-quality animated GIFs and WebP. FFmpeg's two-pass palette approach produces GIFs that are far smaller and sharper than naive conversion.

**Capabilities:**
- Video → GIF with two-pass palette generation (palettegen → paletteuse) for optimal color accuracy and small file size
- GIF → video conversion (MP4/WebM)
- WebP animation with custom fps and resolution

**Key tools:** `palettegen`, `paletteuse`, `dither` modes, `-loop 0`, `-fps_mode passthrough`

**Example Use Cases:**

1. **Creating a GIF for a README or documentation** — Convert a short screen recording or demo clip into a looping GIF. FFmpeg's two-pass palette approach produces GIFs that are dramatically sharper and smaller than tools like Giphy or ezgif.

2. **Converting a GIF to a proper video for social media** — Platforms like Twitter and Slack auto-convert GIFs to video internally anyway — convert to MP4 or WebM first for better quality and smaller file size.

3. **Generating an animated WebP for web use** — Produce an animated WebP (smaller than GIF, supports alpha channel) for modern browsers where GIF bandwidth cost is a concern.

---

## SECTION I — Batch Processing & Scripting

Process entire directories of files automatically. Supports both shell scripting (macOS/Linux) and PowerShell (Windows), with parallel processing and progress reporting.

**Capabilities:**
- Batch convert all files in a directory (bash/zsh loop, PowerShell loop)
- Parallel batch processing with GNU parallel (4+ jobs simultaneously)
- Machine-readable progress output with duration-aware percentage display
- Two-pass encoding for precise target bitrate control

**Key tools:** `-progress pipe:1`, `-nostats`, ffprobe duration extraction, `-pass 1`/`-pass 2`, GNU `parallel`

**Example Use Cases:**

1. **Converting an entire media library overnight** — Loop over hundreds of files and transcode them all to a new format (e.g. H.264 → H.265) unattended. On Linux/macOS use a bash loop; on Windows use a PowerShell loop.

2. **Saturating a multi-core machine for faster throughput** — Use GNU parallel to run 4–8 ffmpeg jobs simultaneously, one per CPU core, instead of encoding files one at a time.

3. **Monitoring progress on a long encode** — Use `-progress pipe:1` with ffprobe to calculate and display a real-time percentage so you know how much time remains on a large batch job.

4. **Hitting an exact target file size** — Use two-pass encoding when you need output to fit under a specific size (e.g. email attachments, upload limits) — pass 1 analyzes, pass 2 hits the bitrate precisely.

---

## SECTION J — Advanced Filtergraphs

Complex multi-input filter chains that go beyond single-stream processing.

**Capabilities:**
- Side-by-side video comparison (`hstack`)
- Vertical stacking (`vstack`)
- 2×2 grid layout from 4 inputs
- Ken Burns zoom/pan effect (`zoompan`)
- Vignette effect
- Full-frame and selective region blur (`boxblur`, `overlay`)
- Audio/video sync repair via stream offset (`-itsoffset`)

**Key tools:** `hstack`, `vstack`, `zoompan`, `vignette`, `boxblur`, `overlay`, `-filter_complex`, `-itsoffset`

**Example Use Cases:**

1. **Side-by-side codec comparison** — Stack the original and re-encoded version horizontally to visually compare quality loss, banding, or blur at different CRF values before committing to a setting.

2. **Creating a highlight reel from multiple cameras** — Stack or grid multiple camera angles into a single frame for a multi-cam overview layout (interviews, sports, events).

3. **Adding a cinematic Ken Burns effect to a still image** — Animate a photo with a slow zoom and pan using `zoompan` to create a moving video from a static image — common in documentary and slideshow production.

4. **Blurring a face or license plate** — Apply a selective region blur using an `overlay` with a `boxblur` limited to specific coordinates, for privacy compliance before publishing footage.

5. **Creating a vignette for a cinematic look** — Add a soft darkened border around the frame to draw attention to the center and give footage a film-like aesthetic.

---

## SECTION K — Quality Analysis & Verification

Measure perceptual and mathematical video quality, and validate that output files are correct before delivery.

**Capabilities:**
- **PSNR** (Peak Signal-to-Noise Ratio) — mathematical fidelity metric
- **SSIM** (Structural Similarity Index) — perceptual similarity metric
- **VMAF** (Netflix perceptual quality model) — industry standard for encode quality comparison
- Output validation: verify duration, size, bitrate, stream count, codec, frame rate
- Detect corrupt packets in any file

**Key tools:** `psnr`, `ssim`, `libvmaf`, `-f null`, ffprobe stream inspection

**Example Use Cases:**

1. **Choosing the right CRF before a large encode** — Run VMAF on a short sample encoded at different CRF values (e.g. 18, 23, 28) to find the lowest bitrate that still looks good to the human eye — saving hours of re-encoding later.

2. **Validating a transcoded file before delivery** — Verify the output has the expected duration, resolution, frame rate, bitrate, and stream count before sending to a client or publishing. Catch problems before they become complaints.

3. **Comparing two encoding pipelines objectively** — Use SSIM or PSNR to numerically compare the output of two different encoders or settings, rather than relying on subjective eyeballing.

4. **Detecting corruption before archiving** — Run ffmpeg's error detection on a file to confirm it has no corrupt packets before committing it to long-term storage.

---

## SECTION L — Platform-Specific Presets

Ready-to-use ffmpeg commands tuned to the exact specs each platform requires. No guessing at bitrates or codec settings.

**Platforms covered (20+):**

| Category | Platforms |
|----------|-----------|
| Video platforms | YouTube 1080p, YouTube Shorts, Vimeo, TikTok, Instagram Reels, Instagram Feed (1:1 / 4:5), Twitter/X, Facebook |
| Live streaming | Twitch (RTMP 6000kbps), OBS Virtual Camera |
| Mobile | iOS (H.264 max compat), Android (H.264 / VP9) |
| Post-production | Apple ProRes 422 HQ, Apple ProRes 4444 (alpha), Avid DNxHD 185, Lossless Archival (FFV1+FLAC/MKV) |
| Web/HTML5 | Web MP4 (H.264 faststart), Web WebM (VP9), Optimized GIF |
| Messaging | Discord (≤8MB), WhatsApp (≤16MB / ≤3min) |
| Audio | Podcast MP3 (stereo 192kbps), Audiobook (mono, loudness-normalized) |

**Example Use Cases:**

1. **Uploading to YouTube without rejection** — Use the YouTube preset to hit the exact specs YouTube recommends (H.264, CRF 18, 48kHz AAC, 29.97fps) so the platform doesn't re-encode your video and degrade quality.

2. **Preparing a vertical video for TikTok or Instagram Reels** — The preset automatically pads landscape footage to 9:16 with black bars and enforces the platform's max duration and bitrate limits.

3. **Exporting for a video editor's ingest format** — Use the ProRes 422 HQ or DNxHD preset to produce an editing-ready master that any NLE (Premiere, Final Cut, Resolve) will accept without transcoding on import.

4. **Compressing a clip to fit Discord's 8MB limit** — The Discord preset uses two-pass encoding to calculate the exact bitrate needed to hit under 8MB for the given duration, without guessing.

5. **Archiving footage in a lossless format** — Use the FFV1+FLAC/MKV archival preset to store footage with zero quality loss and full bit-for-bit reproducibility, suitable for long-term institutional archives.

---

## SECTION M — Video Stabilization

Stabilize shaky footage from handheld cameras, drones, or action cameras. Uses a two-pass approach: pass 1 analyzes motion, pass 2 applies correction. Common use cases: vloggers, event videographers, drone footage, sports and action cameras (GoPro, DJI).

**Capabilities:**
- Two-pass stabilization: `vidstabdetect` (motion analysis) → `vidstabtransform` (correction)
- Tunable shakiness level (1–10) and smoothing radius
- Optional zoom to hide black border artifacts from stabilization
- `unsharp` pass to restore sharpness lost during warp correction

**Key tools:** `vidstabdetect`, `vidstabtransform`, `unsharp`

**Supports:** macOS, Linux, Windows (requires ffmpeg built with `--enable-libvidstab`)

**The Problem Solved in this section M:**

Handheld cameras, drones, action cameras, and phone footage often has unwanted shake — small jitters, rolling motion, or larger bumps.
Normally you'd fix this with a physical gimbal during shooting, but that's not always possible. Section M lets you stabilize in post,
after the fact, on any existing footage.

How the Two-Pass Approach Works

Pass 1 — Analysis (`vidstabdetect`):
FFmpeg reads every frame and tracks how the camera moved between them, writing a transforms file (.trf) to disk. Nothing is output yet
— this pass is pure analysis. You tune two parameters:
- `shakiness` (1–10): how much camera movement to expect — higher for drone or action cam footage
- `accuracy` (1–15): how precisely to track motion — 15 is maximum, recommended for best results

Pass 2 — Correction (`vidstabtransform`):
FFmpeg reads the original video and the transforms file, then applies the inverse of the detected motion to each frame — effectively
counteracting the shake. Key parameters:
- `smoothing`: how many frames to average when computing the correction. Higher = smoother but more aggressive crop.
- `zoom`: extra zoom-in to hide the black borders that appear at the edges when frames are shifted

An optional `unsharp` filter is added after stabilization to restore sharpness, since the warping process softens the image slightly.

Parameter Tuning by Use Case

┌─────────────────────┬────────────────────────────────────────────┐
│      Scenario       │                Settings                    │
├─────────────────────┼────────────────────────────────────────────┤
│ Mild handheld shake │ `shakiness=3`,` smoothing=10`              │
├─────────────────────┼────────────────────────────────────────────┤
│ Typical vlog/event  │ `shakiness=5`, `smoothing=30`              │
├─────────────────────┼────────────────────────────────────────────┤
│ Drone / action cam  │ `shakiness=10`, `smoothing=30`, `zoom=2`   │
├─────────────────────┼────────────────────────────────────────────┤
│ Preserve full frame │ `zoom=0` (black borders will be visible)   │
└─────────────────────┴────────────────────────────────────────────┘

The `unsharp` Step:
After stabilization the frames are slightly soft because of the sub-pixel warping. The `unsharp=5:5:0.8:3:3:0.4` pass at the end sharpens
both luma and chroma back up — a small but noticeable improvement in the final output.

In Short, Section M is useful in one clear situation: you have shaky footage and no gimbal was used during shooting. Two ffmpeg commands and a
transforms file is all it takes — no third-party software, no plugins, no GUI needed.

---

## SECTION N — 360° / VR Video

Handle 360° footage from cameras like GoPro Max, Insta360, and Ricoh Theta. Without proper projection conversion and spherical metadata injection, platforms like YouTube VR and Facebook 360 won't recognize the file as 360° — it plays as a flat, distorted video.

**Capabilities:**
- Equirectangular → cubemap (3×2) conversion
- Cubemap → equirectangular conversion
- Extract a flat "normal" view from a 360° source (reframe with custom yaw/pitch/FOV)
- Inject spherical metadata for YouTube VR / Facebook 360 compatibility

**Key tools:** `v360` filter (`equirect`, `c3x2`, `flat`)

**Supports:** macOS, Linux, Windows (v360 is cross-platform)

**Example Usa Cases:**

1. Equirectangular ↔ Cubemap Conversion

Convert between the two projection formats using the v360 filter. Useful when:
- A game engine or VR app requires cubemap input but your camera outputs equirectangular
- You want to convert cubemap footage for YouTube (which needs equirectangular)

2. Inject Spherical Metadata

Tell platforms the video is 360° by embedding the right metadata tag. YouTube and Facebook read this to activate their 360° viewer.
Without it, the video plays flat regardless of the projection.

▎ For full YouTube VR compliance, Google's spatial-media tool injects a more complete XMP metadata atom — FFmpeg's injection is a good
fallback but the spatial-media tool is the authoritative approach for production uploads.

3. Reframe / Extract a Flat View

Take a 360° equirectangular source and extract a conventional flat video from it — choose any yaw (left/right), pitch (up/down), roll,
and field of view. Useful for:
- Creating a normal-looking highlight clip from 360° raw footage
- Reframing a shot in post without reshooting
- Generating a flat preview thumbnail from a 360° video

**The Problem Solved in this section N:**
A 360° camera doesn't record a normal flat image — it records the entire sphere around it and maps that onto a flat rectangle using a
mathematical projection. The two most common are:

- Equirectangular — the full sphere stretched into a 2:1 rectangle (looks like a distorted world map). This is what YouTube VR,
Facebook 360, and most VR headsets expect.
- Cubemap (3×2) — the sphere mapped onto the 6 faces of a cube, arranged in a grid. Some cameras and engines use this natively.

If you upload an equirectangular video to YouTube without the right spherical metadata injected, YouTube just plays it as a flat
distorted video — it never activates the 360° viewer.

In Short, Section N matters in three situations: your 360° upload isn't activating the VR viewer on YouTube or Facebook (metadata injection),
you need to convert between projection formats for a specific platform or engine (v360 conversion), and you want to extract a usable
flat clip from 360° raw footage (reframing).

---

## SECTION O — HDR / Color Science

Modern phones and cameras shoot HDR by default (10-bit, bt2020, smpte2084). Without proper tone mapping, HDR footage looks washed out or blown out on SDR displays and platforms.

**Capabilities:**
- HDR10 → SDR tone mapping using `zscale` + `tonemap` (hable, reinhard, mobius, clip algorithms)
- Colorspace conversion for bt2020-tagged files that aren't true HDR (`colorspace` filter)
- Encode proper HDR10 output with display metadata (master display, MaxCLL, MaxFALL) using libx265
- Tag existing files with correct color space metadata without re-encoding

**Key tools:** `zscale`, `tonemap`, `colorspace`, `format=gbrpf32le`, libx265 `-x265-params`

**Supports:** macOS, Linux, Windows (requires ffmpeg with `--enable-libzimg`)

**Example Usa Cases:**

1. HDR10 → SDR Tone Mapping

The full conversion pipeline for genuine HDR10 content: linearize the signal, convert to a working color space, apply a tone mapping
curve to compress highlights into the SDR range, then output as standard bt709. Four tone mapping algorithms are available:

┌───────────┬──────────────────────────────────────────────────────┐
│ Algorithm │                      Character                       │
├───────────┼──────────────────────────────────────────────────────┤
│ hable     │ Filmic, preserves highlight detail — general purpose │
├───────────┼──────────────────────────────────────────────────────┤
│ reinhard  │ Simple global compression — fast previews            │
├───────────┼──────────────────────────────────────────────────────┤
│ mobius    │ Smooth and natural — good for skin tones             │
├───────────┼──────────────────────────────────────────────────────┤
│ clip      │ Hard cut at white — technical/broadcast use          │
└───────────┴──────────────────────────────────────────────────────┘

2. Colorspace Conversion (bt2020 → bt709)

Some files are tagged as bt2020 but aren't true HDR — just wide gamut SDR. A lighter conversion using the colorspace filter handles
these without the full HDR tone mapping pipeline.

3. Encode HDR10 Output

For archival or delivering to HDR-capable platforms, encode proper HDR10 with full display metadata — master display luminance,
MaxCLL, MaxFALL — using libx265. This is what makes the file play correctly on an HDR TV or pass Netflix/Apple HDR validation.

4. Tag Existing Files

Sometimes footage is encoded correctly but missing the color space tags, so players treat it as SDR. You can inject the correct
color_primaries, color_trc, and colorspace flags without re-encoding — stream copy with metadata only.

**The Problem Solved in this section O:**
iPhones, Android flagships, and most modern cameras now shoot HDR by default — 10-bit color, wide color gamut (bt2020), PQ transfer
curve (smpte2084). When that footage lands on an SDR platform, an SDR editing timeline, or an SDR display without proper conversion,
one of two things happens:
- Colors look washed out and flat (if the player tries to interpret HDR as SDR naively)
- Colors look blown out and oversaturated (if the wide gamut isn't mapped down)

This Section O fixes both.

In Short, Section O matters most in three situations: footage from a modern phone looks wrong after export (colorspace conversion), delivering
SDR versions of HDR masters for web (tone mapping), and archiving or delivering to HDR platforms (HDR10 encode with proper metadata).

---

## SECTION P — Advanced Streaming

Three distinct streaming capabilities beyond basic RTMP: low-latency SRT, multi-destination restreaming, and rolling DVR recording.

**Capabilities:**
- **SRT streaming:** Low-latency, packet-loss-resilient streaming over unstable connections (cellular, satellite). Supports caller and listener modes, configurable latency.
- **Multi-endpoint restreaming (tee muxer):** Stream to YouTube, Twitch, and Facebook simultaneously from one ffmpeg process — no external restreaming service needed.
- **Rolling window DVR:** Continuous loop recording in segments, keeping only the last N minutes. Ideal for security cameras and broadcast monitoring where storage is limited.

**Key tools:** `srt://` protocol, `-f tee`, `-f segment`, `-segment_time`, `-segment_wrap`, `-reset_timestamps`

**Supports:** macOS, Linux, Windows (SRT requires ffmpeg with `--enable-libsrt`, included in full builds)

**Example Usa Cases:**

1. SRT (Secure Reliable Transport)

Low-latency streaming protocol that actively compensates for packet loss and network jitter. Unlike RTMP which just drops frames on a
bad connection, SRT retransmits lost packets. Useful when streaming over unstable networks — cellular hotspots, satellite uplinks, or
long-distance contribution feeds (e.g. a remote reporter sending footage back to a studio).

2. Multi-endpoint Restreaming (tee muxer)

One ffmpeg command, one encoder, multiple destinations simultaneously. You can stream to YouTube + Twitch + Facebook at the same time
without running three separate encoder instances or paying for a restreaming service like Restream.io.

3. Rolling Window DVR

Continuous loop recording that writes segments to disk and automatically overwrites the oldest ones, keeping only the last N minutes.
You get a perpetual recording without ever filling up storage. Practical for:
- Security cameras (keep last 2 hours, discard older)
- Broadcast monitoring (capture a rolling window in case something needs to be reviewed)
- Game capture (record always-on, clip what you need later)

---

## SECTION Q — Repair & Recovery

Real-world files get corrupted — interrupted recordings, SD card failures, bad downloads. This section covers extracting usable video from files that media players and editors reject, and fixing the most common structural problems.

**Capabilities:**
- Recover from corrupt/truncated files by ignoring errors and discarding bad packets
- Force container format detection when the file header is unreadable
- Increase probe/analyze buffer sizes for files with damaged or missing moov atoms
- **VFR → CFR conversion:** Fix audio sync drift caused by variable frame rate footage (common from phones and screen recorders like OBS)
- Fix audio/video sync offset (advance or delay audio by milliseconds)
- Rebuild broken MP4 index (moov atom repositioning)

**Key tools:** `-err_detect ignore_err`, `-fflags +discardcorrupt`, `-analyzeduration 100M`, `-vsync cfr`, `-itsoffset`, `-movflags +faststart`

**Supports:** macOS, Linux, Windows

**Example Usa Cases:**

1. Corrupt / Truncated File Recovery

When a recording is interrupted — power cut, SD card yanked, app crash, bad download — the resulting file often won't open at all in
media players or editors. FFmpeg can attempt recovery by ignoring errors and discarding only the damaged packets, extracting as much
usable footage as possible from what remains.

Three escalating approaches:
- -err_detect ignore_err -fflags +discardcorrupt — ignore bad packets, keep the rest
- -analyzeduration 100M -probesize 100M — for files where the header/index is damaged
- -f mp4 (force container) — for files where FFmpeg can't even detect the format

2. VFR → CFR Conversion

This is one of the most common silent problems in video editing. Phones and screen recorders (OBS, Loom, QuickTime screen capture)
record in variable frame rate — the timestamp between frames isn't constant. Most editing software (Premiere Pro, DaVinci Resolve,
Final Cut) assumes constant frame rate internally, so VFR footage causes audio sync drift that gets worse over time — a 10-minute clip
might be half a second out of sync by the end.

Converting to CFR (-vsync cfr -r 30) before importing into your editor fixes this at the source. FFprobe can confirm whether a file is
VFR before you convert.

3. Audio/Video Sync Offset Fix

When audio and video are consistently offset by a known amount (e.g. a microphone that always introduces 200ms of delay), you can
correct it without re-encoding the video — just shift the audio stream. Works in both directions: delay or advance.

4. Rebuild Broken MP4 Index

The moov atom is the index at the start of an MP4 that tells players where everything is. If it's missing or at the wrong position,
the file won't seek properly or won't play at all in browsers. -movflags +faststart rebuilds and repositions it — fast, lossless, no
re-encode.

In short, Section Q is most useful in three real-world situations: something went wrong during recording (corrupt file recovery), footage from a
phone or screen recorder drifts out of sync in your editor (VFR→CFR), and an MP4 won't play in a browser or seek properly (moov atom rebuild).

---

## SECTION R — Metadata Management

Media files carry metadata that affects how they are displayed, organized, and distributed. This section covers reading, writing, and stripping metadata at the file, stream, and chapter level.

**Capabilities:**
- Embed key/value tags (title, artist, year, comment, album, track number)
- Strip all metadata for privacy (removes GPS coordinates, device info, user data)
- Add chapter markers with timestamps and titles (navigable in YouTube, VLC, media players)
- Embed cover art into MP3, M4A, and AAC audio files
- Tag audio/subtitle streams with language codes for international distribution
- Remove specific streams (e.g. unwanted audio tracks)
- Read and display all metadata from any file

**Key tools:** `-metadata`, `-map_metadata -1`, `-map_chapters`, `-disposition:v:0 attached_pic`, `-metadata:s:a:0 language=`, ffprobe JSON parsing

**Supports:** macOS, Linux, Windows

**Example Usa Cases:**

1. Embed Key/Value Tags

Add standard metadata tags — title, artist, year, album, comment, track number — to any video or audio file. These show up in file
browsers, media players, and streaming platforms. Essential for podcasts, audiobooks, and music files where the player displays this
info to the listener.

2. Strip All Metadata (Privacy)

Phones and cameras silently embed a lot of data into every file: GPS coordinates of where it was recorded, device model, serial
number, sometimes even user account info. Before publishing anything online, stripping this data is a basic privacy practice. One
ffmpeg flag (-map_metadata -1) removes everything.

3. Chapter Markers

Embed navigable chapter points with timestamps and titles directly into the file. YouTube automatically reads these and renders a
chapter timeline in the progress bar. VLC, QuickTime, and most media players also display them. Particularly valuable for:
- Long YouTube videos (tutorials, podcasts, lectures)
- Audiobooks (chapter navigation in every player)
- Training videos (jump to specific topics)

4. Cover Art

Embed a thumbnail image directly into MP3, M4A, or AAC files. Without this, every podcast app, music player, and audiobook app shows a
blank grey square. The cover travels with the file regardless of where it's played.

5. Multi-Language Track Management

Tag audio and subtitle streams with ISO language codes so players automatically select the right track based on the viewer's system
language. Also covers removing unwanted tracks (e.g. stripping a commentary audio track before delivery) and extracting specific
language tracks.

6. Read All Metadata

Dump everything embedded in a file — format tags, per-stream tags, chapter info — parsed from ffprobe's JSON output via Python. Useful
for auditing files before delivery.

In short, Section R matters most in three scenarios: privacy (strip before publishing), distribution (chapters + language tags for international content), 
and audio files (cover art + tags for podcasts/audiobooks).

---

## SECTION S — Testing & Debugging

Verify encoding pipelines, diagnose file-level problems, and benchmark your hardware before committing to long encodes.

**Capabilities:**
- **SMPTE color bars + tone:** Generate the broadcast-standard calibration signal (smptebars / smptehdbars) with a 1kHz sine tone to verify the full encoding pipeline end-to-end
- **Packet-level analysis:** Inspect every packet in a file — total count, keyframe positions, PTS/DTS gaps, and corruption detection — using ffprobe + Python
- **Encoding benchmark:** Compare H.264 presets (ultrafast → slow) on your hardware to understand the speed/size/quality tradeoff before a batch encode
- **Bit stream inspection:** Dump raw codec headers and H.264 NAL units with `trace_headers` to diagnose encoder-level issues
- **Streamability check:** Verify moov atom position (faststart) and file structure with ffprobe

**Key tools:** `smptebars`, `smptehdbars`, `sine` lavfi sources, `ffprobe -show_packets`, `-bsf:v trace_headers`, `-benchmark`, Python 3 benchmark script

**Supports:** macOS, Linux, Windows (Python 3 required for benchmark script)

**Example Usa Cases:**

1. SMPTE Color Bars + Tone

Generate the broadcast-standard calibration signal — color bars on screen, 1kHz sine tone on audio. Use this to verify your entire
encoding pipeline is working correctly before a live broadcast or before delivering a file to a client. If the bars look right and the
tone is at the correct level, your codec, color space, and audio settings are all good.

2. Packet-Level Analysis

When a file causes playback issues or crashes an editor, ffprobe -show_packets lets you go below the container level and inspect every
individual packet. You can find:
- Exactly where corruption starts in a file
- Where keyframes are missing (causing seek failures)
- PTS/DTS gaps that cause A/V desync
- Total packet count and duration span

The included Python script summarizes this into a readable report automatically.

3. Encoding Benchmark

Before committing to a 6-hour batch encode, run a quick benchmark to understand the tradeoff between preset speed, output file size,
and quality on your specific hardware. The Python script tests ultrafast through slow presets and prints a table showing encode time
and file size for each — so you can make an informed decision.

4. Bit Stream Inspection

Dump raw H.264 NAL units and codec headers using the trace_headers bitstream filter. This is for diagnosing encoder-level issues that
don't surface at the container level — things like missing SPS/PPS headers, wrong profile/level flags, or reference frame issues that
cause decoder failures on specific devices.

5. Streamability Check

Verify that an MP4's moov atom is at the front of the file (required for progressive web playback) and inspect file structure with
ffprobe.

In short, Section S is most useful when something is broken and you need to diagnose it, or when you're setting up a new encoding pipeline and
want to validate it before going live.
