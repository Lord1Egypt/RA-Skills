# Video Quality Tuning Guide

## Known Artifacts and Fixes

### 1. Clip Boundary Flicker (1–2 frames)

**Symptom**: A flash or color jitter appears at the cut point between clips.

**Root cause**: ShotAI's `startTime`/`endTime` values include a few transition/fade frames at each shot boundary. These edge frames are often blurred or contain the previous shot bleeding through.

**Fix**: `orchestrator.ts` applies an 80ms head/tail trim (`TRIM = 0.08`) to every extracted clip:

```typescript
const TRIM = 0.08; // seconds to cut from each end
const rawDur = shot.endTime - shot.startTime;
const trimStart = shot.startTime + (rawDur > TRIM * 3 ? TRIM : 0);
const trimEnd   = shot.endTime   - (rawDur > TRIM * 3 ? TRIM : 0);
```

- Only applied when the clip is long enough (`rawDur > TRIM * 3` = 240ms minimum) to avoid over-trimming very short clips.
- If boundary flicker persists, increase `TRIM` to `0.12` or `0.15`.

---

### 2. Flash Artifact in CyberpunkCity (GlitchFlicker on short clips)

**Symptom**: A bright red flash appears mid-video, typically at a short clip.

**Root cause**: `GlitchFlicker` triggers a red glitch overlay at frames `[3, 4, dur-5, dur-4]`. For a clip of ~48 frames (1.6s), frames 43–44 fall very close to the head of the clip, making the tail-glitch appear immediately after the head-glitch — producing a rapid double-flash.

**Fix**: `CyberpunkCity.tsx` now only triggers tail glitch on clips longer than 30 frames (1s at 30fps):

```typescript
const glitchFrames = dur > 30
  ? [3, 4, dur - 5, dur - 4]
  : [3, 4];  // short clips: head-glitch only
```

**Prevention**: Set `MIN_SCORE=0.5` in `.env` to keep very short clips out of the pipeline entirely.

---

### 3. Low-Quality / Off-Topic Shots

**Symptom**: Rendered video contains obviously wrong or blurry shots.

**Remedies** (in order of preference):

1. **Raise `MIN_SCORE`** (`.env`): Start at `0.50`, go up to `0.70` for very selective output.
2. **Use probe mode** (`--probe` flag): Scans the library first, LLM generates queries tailored to actual content instead of generic template queries.
3. **Explicit composition** (`--composition <id>`): Skip LLM inference and target a specific composition whose shot-slots match your library.
4. **Refine queries manually**: Edit `src/skill/registry.ts` shot-slot `query` fields to better match your library's naming conventions.

---

### 4. Music Not Found / yt-dlp Fails

**Symptom**: Pipeline hangs or errors at the "resolve music" step.

**Remedies**:
- Provide a local BGM: `--bgm /path/to/music.mp3` (skips YouTube search entirely)
- Set `BGM_PATH=/path/to/music.mp3` in `.env` as a permanent default
- Update yt-dlp: `pip install -U yt-dlp`
- Check network: YouTube CDN may be blocked; use a proxy or local file

---

## Performance Notes

- **Remotion render time**: ~30–90s for a 60s video on an M-series Mac. GPU acceleration is automatic.
- **ShotAI search latency**: ~1–3s per slot depending on library size and MCP server load.
- **ffmpeg extraction**: ~0.5s per clip (hardware-accelerated on macOS with `-hwaccel videotoolbox`).
