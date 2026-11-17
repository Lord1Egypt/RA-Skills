# Platform exports

Platform limits drift. Verify the current official specification when the prompt names a platform; do not rely on remembered dimensions, formats, frame limits, or byte limits.

Export rules:

1. Keep `source/frames/`, `source/motion.json`, and `sticker.webp` unchanged.
2. Write every platform derivative beneath `exports/<platform>/`.
3. Preserve frame order and per-frame durations unless the platform rejects them.
4. Resize proportionally and retain a transparent safe area where the platform supports alpha.
5. If the platform requires GIF, inspect palette banding, matte color, edge halos, and text readability after conversion.
6. If a byte limit forces quality reduction, reduce metadata and redundant colors first, then dimensions or frame count; do not silently remove the semantic hold.
7. Record the verified source URL, verification date, export parameters, and resulting byte size in an export report.
8. Build animated GIF derivatives from the validated RGBA source frames, not from `sticker.webp`; transcoding an already compressed animation compounds artifacts.
9. Use one shared palette across GIF frames so stable surfaces do not change color between frames. Prefer the highest palette size that satisfies the platform byte limit.
10. Derive a required static preview from the longest semantic-hold frame unless the motion plan names a better representative frame. If the animation contains exact text, prefer a frame where that text is complete.
11. Require `technical_validation`, `visual_validation`, and `deliverable_ready` to pass before normal export. A partial report with only top-level `status: pass` is not enough.
12. Use authored keyframes by default. A high-frame render track is eligible only when `source/motion.json` declares its directory, numeric `target_fps`, frame count, per-frame durations, and total duration, and its separate report passes both validation types.
13. When both frame rate and palette may be reduced to meet a byte limit, declare an ordered frame-rate fallback and a minimum acceptable palette. Exhaust palette candidates down to that floor at the preferred frame rate before lowering the frame rate; never cross the floor silently.
14. Apply the resampling policy recorded in `source/motion.json`: `nearest` for native pixel art or another strict grid, `lanczos` for continuous-tone and illustrated raster work. Upscale only when the target platform requires a larger canvas.
15. Treat scripted constraint validation and visual export validation as separate gates. A normal export begins at `pending_visual_validation` and becomes deliverable only after its exact GIF and preview fingerprint receives passed visual validation.

Use `scripts/export_platform_gif.py` for constrained GIF plus optional preview PNG exports. It refuses incomplete validation by default and writes source validation states into a report beside each GIF, such as `01.export-report.json`, so batch exports do not overwrite one another. Require the official specification URL and its actual verification date on every invocation. `--allow-unvalidated` is a diagnostic escape hatch whose report status is `diagnostic_unvalidated`; it cannot become deliverable. Re-open the resulting GIF and preview at actual target size; a byte-limit pass alone does not validate palette banding, binary-Alpha edges, or text readability. Record visual validation in that export report with `scripts/record_visual_validation.py`; deliver only when `deliverable_ready` is true.

For a validated optional render track, pass `--frame-track render`, its `--track-report`, an ordered value such as `--fps-candidates 30,24,20,15`, and a validated `--min-colors` quality floor. The report records every attempted frame-rate/palette combination and the selected result. Automatic preview selection still comes from the authored semantic-hold keyframe so resampling cannot accidentally choose an in-between pose as the cover.

Do not create a platform directory when no platform or extra format was requested.
