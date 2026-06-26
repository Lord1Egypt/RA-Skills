<!-- MODULE: slicing -->

## Slicing — Profile Selection

**NEVER use hardcoded or remembered profile IDs.** Profile IDs are stored on the slicer server and are lost when the container restarts. Before every slice:

1. Run `claw3d profile list` — use whatever ID is listed there.
2. **If 0 profiles:** User must send a 3MF (use `--profile-from-3mf`) or create a profile first.
3. **If 1 profile:** Use it with `--profile <id>`.
4. **If 2+ profiles:** Ask in a numbered list, or use the printer's linked profile if the user chose a printer for this print.

## Source-Based Auto-Routing (Deterministic)

`claw3d slice` reads the `.source.json` sidecar automatically. When it detects `"source": "thingiverse"`, it:
- Auto-enables `--no-mesh-clean` (skips mesh repair)
- Auto-skips scaling (no 100mm default)

**You do NOT need to pass `--no-mesh-clean` manually** — the code handles it. Just pass the model file and the slicer does the right thing based on provenance.

When re-slicing, the previous settings are saved in `.slice_config.json` and reused automatically (max-dimension, strength, quality). You only need to pass flags that changed.

## Max Print Size — Two Paths

**Path A: Model from directory (Thingiverse)** — The model is already at the correct physical size. **NEVER ask for max print size.** Do NOT pass `--max-from-model` or `--max-dimension`. The source-based routing handles this automatically.

- **Prefer the `.stl` sidecar** (`model_<ID>.stl`) if it exists — send it directly, no conversion.
- **If only `.glb` exists** (model was fetched as GLB): use `model_<ID>.glb`. The auto-routing will apply `--no-mesh-clean` automatically.

Ask the user only:
> Before I slice, I need two things:
>
> 1. **Strength** — How strong should it be? (10%, 25%, 50%, 75%, or 100%)
> 2. **Detail** — How much print detail / quality? (10%, 25%, 50%, 75%, or 100%)

**Path B: Model from AI or user-provided** — Use `model_<ID>.glb`. No dimensions file. **MUST ask** for max print size, strength, and detail before slicing. Use the printer's build volume (from `claw3d printer list`) as the default max dimension suggestion — use the smallest of width/depth/height.

> Before I slice, I need a few things:
>
> 1. **Max print size** — What's the longest dimension you want? (e.g. 100mm or 150mm)
> 2. **Strength** — How strong should it be? (10%, 25%, 50%, 75%, or 100%)
> 3. **Detail** — How much print detail / quality? (10%, 25%, 50%, 75%, or 100%)

**Map percentages to CLI:** 10%→1, 25%→2, 50%→3, 75%→4, 100%→5. Use `--max-dimension <N>`, `--strength`, `--quality`.

**Natural language → CLI flags:**
- "make it stronger" → `--strength 4`
- "20% infill" → `--infill-density 20`
- "fit in 100mm" → `--max-dimension 100`
- "rotate 90 degrees on Y" → `claw3d rotate -i model.glb --rotation-y 90` (then preview/slice without rotation flags)
- "rotate 45 on X" → `claw3d rotate -i model.glb --rotation-x 45`
- "more detail" / "higher quality" / "thinner layers" → `--quality 4` or `--layer-height 0.1`

**Bed leveling:** Do NOT add `--bed-autocalibration` unless the user explicitly asks. Default OFF.

## Rotation Workflow — Baked Into File

`claw3d rotate` permanently modifies the model file. Rotation is cumulative by design — each call rotates from the model's current orientation, like dragging an object in a 3D editor. No state tracking needed.

**When the user asks to rotate a model** ("rotate 90 on X", "flip it sideways", "turn it upside down"):

**Step 1 — Rotate the file:**
```bash
claw3d rotate -i model_<ID>.glb --rotation-x 90
```
The GLB is now permanently rotated. All future preview/slice commands use the file as-is — no rotation flags needed.

**Step 2 — Show preview (no rotation flags):**
```bash
claw3d preview -i model_<ID>.glb --build-volume <WxDxH> -o preview_<ID>_rotated.mp4
```
Send with: "Here it is rotated 90° on X — does this look right for printing?"

**Step 3 — When user confirms, slice (no rotation flags):**
```bash
claw3d slice -i model_<ID>.glb -p <profile_id> -o model_<ID>.gcode --build-volume <WxDxH>
```

**Multiple rotations just work:**
| User says | You run | Result |
|---|---|---|
| "rotate 90 on X" | `claw3d rotate -i model.glb --rotation-x 90` | Model is now 90° on X |
| "now rotate 90 on Y" | `claw3d rotate -i model.glb --rotation-y 90` | Model is now 90° X + 90° Y |
| "and 45 on Z" | `claw3d rotate -i model.glb --rotation-z 45` | All three rotations accumulated |

**Natural language mapping:**
- "flip it" / "turn it upside down" → `--rotation-x 180`
- "turn it sideways" → `--rotation-y 90`
- "rotate 90 on X and 45 on Z" → `--rotation-x 90 --rotation-z 45` (one command)

**Undo rotation:** If the user says "undo that rotation" or "go back":
```bash
claw3d rotate -i model_<ID>.glb --undo
```
This restores the file from before the last rotation. Up to 5 undo levels are kept.

**Do NOT pass `--rotation-x/y/z` to `claw3d preview` or `claw3d slice`.** Always use `claw3d rotate` first — the file is the source of truth.

## Useful Diagnostic Commands

```bash
# Check what happened to a model (source, dimensions, last slice settings, files)
claw3d model-status -i model_<ID>.glb

# System health check (API keys, slicer, printers, ffmpeg)
claw3d doctor
```

## Slice Command — Background Process Handling

**CRITICAL: Both `claw3d slice` and `claw3d preview` are long-running commands. You MUST wait for them to finish before proceeding. Do NOT return control to the user while they run.**

### How long-running commands work:

The exec call waits up to 2 minutes for the command to finish. Most commands complete within this window and return the result directly. If a command takes longer, exec returns `Command still running` with a session ID. In that case:

1. Call `process poll <session>` **once** with `timeout: 120000` (2 min wait).
2. You will be notified automatically when the process completes.
3. **Do NOT poll in a rapid loop** — this wastes API calls and hits rate limits.
4. When you see `Wrote <path>` or `[timing]` → the command finished. Proceed immediately.

### For `claw3d slice`:

1. Run `claw3d slice ...` — tell the user: "Slicing started! I'll let you know when it's ready."
2. Wait for completion (exec returns result, or poll once if backgrounded).
3. When you see `Wrote <path>` for the gcode preview → **send both files immediately**.

### For `claw3d preview`:

1. Run `claw3d preview ...` — tell the user: "Generating your 3D preview, I'll send it when it's ready!"
2. Wait for completion (exec returns result, or poll once if backgrounded).
3. When you see `Wrote <path>` → **send the file immediately. Do NOT ask the user if they want it.**

**YOU MUST NOT return control to the user until you see `Wrote <path>` or an error.**

**After slice succeeds, send BOTH the G-code and the G-code preview video.** Slice generates `model_<ID>_gcode_preview.mp4` by default (body red, supports yellow). Use the `message` tool so both files attach in Telegram.

**Include print estimates in your message.** The slice output includes an `[estimates]` line with print time, filament usage, and layer count. Always include these stats when sending the G-code, e.g.: "Here's your G-code! Estimated print time: 2h 30m | Filament: 12.5m (37g) | Layers: 245"

**When the user asks for "the video" after a slice:** They mean the G-code preview (`model_<ID>_gcode_preview.mp4`). **Do NOT run `claw3d preview`** — that renders the 3D model. Send the existing gcode preview file.

**Build volume for previews:** When a default printer is configured (i.e. the printer was added with `--profile-from-3mf`), `claw3d preview` and `claw3d slice` automatically use that printer's build volume — you do NOT need to pass `--build-volume` explicitly. If needed, you can always override with `--build-volume WxDxH` (e.g. `--build-volume 350x350x350`). The build volume renders the grey build plate, 10mm grid, and volume wireframe in the preview video. To verify the current default printer's build volume, run `claw3d printer list`.

```bash
# GLB + separate 3MF (most common) — read build volume from printer list
claw3d slice -i <glb_path> --profile-from-3mf <3mf_path> -o model_<ID>.gcode --build-volume <WxDxH>

# Thingiverse/directory model — use .stl sidecar if it exists (preferred: no conversion, no mesh fixes)
claw3d slice -i model_<ID>.stl -p <profile_id> -o model_<ID>.gcode --strength 3 --build-volume <WxDxH>

# Thingiverse/directory model — GLB only (no .stl sidecar): must use --no-mesh-clean
claw3d slice -i model_<ID>.glb -p <profile_id> -o model_<ID>.gcode --strength 3 --no-mesh-clean --build-volume <WxDxH>

# AI/user model — use .glb (must ask for max)
claw3d slice -i model.glb -p <profile_id> -o model.gcode --max-dimension 150 --strength 4 --build-volume <WxDxH>

# Single 3MF (model + settings in one file)
claw3d slice -i project.3mf -o model.gcode

# Per-parameter overrides
claw3d slice -i model.glb -p <profile_id> -o model.gcode --infill-density 20 --layer-height 0.15
# Rotation: use `claw3d rotate` first, then slice without rotation flags
claw3d rotate -i model.glb --rotation-y 90
claw3d slice -i model.glb -p <profile_id> -o model.gcode

# Profile management
claw3d profile create --from-3mf settings.3mf --name my_pla
claw3d profile list
claw3d profile set-default <profile_id>
claw3d profile clear   # delete all profiles (fresh start)

# Standalone preview with build area (read WxDxH from printer list)
claw3d preview --input model.glb --output preview.mp4 --build-volume <WxDxH>
claw3d gcode-preview --input model.gcode --output gcode_preview.mp4 --build-volume <WxDxH>
```

## Slice Flags Reference

| Flag | Description |
|------|-------------|
| `-i`, `--input` | Input GLB, STL, or 3MF |
| `-o`, `--output` | Output G-code path |
| `-p`, `--profile` | Profile ID (use `--profile` OR `--profile-from-3mf` for GLB/STL) |
| `--profile-from-3mf` | Create profile from 3MF, then slice |
| `--strength` | 1–5 (10%→1 … 100%→5). Default 3 |
| `--quality` | 1–5 (10%→1 … 100%→5). Detail / print quality level |
| `--max-dimension` | Scale longest axis to N mm (AI models) |
| `--max-from-model` | Use max from dimensions.json (directory models) |
| `--no-mesh-clean` | Skip all mesh repair during GLB→STL conversion. **Required for directory/Thingiverse GLBs** — mesh fixes are for AI models only and can delete real model geometry |
| `--rotation-x` | ⚠️ **Prefer `claw3d rotate` instead** — bakes rotation into file. Only use in slice/preview for one-off tests |
| `--rotation-y` | Same as above |
| `--rotation-z` | Same as above |
| `--layer-height` | Override layer height in mm (e.g. 0.15) |
| `--infill-density` | Override infill percentage (e.g. 20) |
| `--preview-video` | Generate 360° G-code preview video (default ON) |
| `--no-preview-video` | Skip G-code preview video (faster) |
| `--build-volume` | `WxDxH` mm (e.g. `350x350x350`). Shows build plate + grid in gcode preview. Read from `claw3d printer list`. |
| `--bed-autocalibration` | Run bed leveling before print. **Default OFF** — only add when user explicitly asks |

<!-- /MODULE: slicing -->
