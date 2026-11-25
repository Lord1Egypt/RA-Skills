# Pipeline recipes and gotchas

## Environment
- The venv is at `~/.cache/claw-editing/venv` (`scripts/setup.sh`): mlx-whisper on Apple Silicon or faster-whisper elsewhere (see `scripts/asr.py`), skia-python, pillow, numpy.
- ffmpeg/ffprobe: from PATH (`brew install ffmpeg`) or `OPENCLAW_FFMPEG`. The build must include prores_ks and libx264; `render.py` finds it automatically.
- If the shell is **zsh**:
  - `for a in "x 1" …; do set -- $a` does not word-split. Feed `name time` pairs through a bash heredoc or `while read` (see examples).
  - A glob with no matches (`rm dir/*` on an empty dir) aborts the whole command line. Use `rm -rf dir && mkdir dir`.
- Scratchpads can be wiped between sessions. Keep plans and scripts in the project's `Motion Graphics/source/`.

## Frame-accurate cutting (edit.py)
- Convert source seconds to frames (`round(t × fps)`) and cut both picture and audio from the same `-ss` per segment, so they stay locked.
- 8 ms afade in/out at every splice prevents clicks.
- **Leading silence:** this ffmpeg build silently drops `adelay` when `apad` follows it, which once left the audio unshifted and out of sync. Build silence with `aevalsrc=0|0:d=…` and `concat` instead.
- **Denoiser latency:** `afftdn` adds exactly 1200 samples (25 ms at 48 kHz). Measure it by cross-correlating raw against denoised and `atrim=start_sample=` it away, then re-measure (want 0).
- Loudness: two-pass `loudnorm` (I = −16, TP = −2, LRA = 11, `linear=true`). Results land around −15.7 to −16.2 LUFS.
- Python's `wave` can't read 24-bit WAVE_FORMAT_EXTENSIBLE. Decode through `ffmpeg -f f32le -` pipes instead.

## Choosing cut points
- Whisper word starts are often 0.1–0.4 s early. Use `envelope.py` (20 ms dB steps): speech is above about −25 dB, room tone below about −40 dB.
- Cut inside a dip. If the next word starts within about 50 ms, cut at the dip just after the last word (e.g. 249.73), not where Whisper says the next word begins.
- Validate a splice by transcribing the joined audio of both candidate edges. A leaked syllable shows up as an extra word ("We've external backups").

## Overlays
- Place each clip with `setpts=PTS-STARTPTS+<frame>/<fps>/TB` and `overlay=eof_action=pass:format=yuv444:repeatlast=0`, chained.
- ProRes 4444 encode from RGBA: `scale=out_color_matrix=bt709:out_range=tv,format=yuva444p10le`, `-profile:v 4444 -alpha_bits 16`. Un-premultiply Skia's premultiplied RGBA before writing (`overlays.unpremul`).
- An opaque card that must hide a burned-in card should reach alpha 1.0 on or before the old card's first frame. Find that frame by luma (`signalstats`) and check it.

## Replacing burned-in overlays with a clean source
1. Cross-correlate the audio of the overlay version against the clean file at several points (1-second windows). A constant offset means the same edit; a jump means an internal cut, so bisect to find it.
2. Match frames with 64×36 grayscale thumbnails (mean absolute difference below about 1 is a match). The clean file may be VFR, so use `fps=30` before `trim`.
3. Patch only the frames where the old overlay is visible (find them by diffing the band where the overlay sits), keeping the user's version everywhere else (`composite.py` `patches`).

## Thumbnails
- Convert to 1920×1080 (lanczos), saved as `.png` and `.jpg`.
- Hold it as the first `round(fps)` frames (concat before the body), plus 1 s of silence via `aevalsrc`+`concat`. The audio must then be re-encoded (AAC 192k).
- Embed it as cover art: map the jpg as a second video stream with `-c:v:1 mjpeg -disposition:v:1 attached_pic`, and use stream-specific options (`-frames:v:0`, `-c:v:0`, `-r:v:0`).
- Verify: the first frame and the attached_pic should both differ from the thumbnail by only a few levels; audio should still correlate at 0 ms lag (offset by 1 s).

## Render times on his M5 Max
- Clip encodes are about real-time per clip; run 8–10 in parallel with `xargs -P`.
- Composite of a 22-min 1080p30 video with about 22 overlays: about 15–20 min (run in background). Shorts: under a minute.

## Delivery
- Give the full output path. On a Mac with a GUI session, `open -R "<file>"` reveals it in Finder. Over a messaging channel, send the contact sheet as a preview; the video is usually too large to send.
