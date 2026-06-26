# Module: 3D Model Search (Thingiverse Library)

**You CAN search for existing 3D models on Thingiverse.** Use `claw3d find`, `claw3d fetch`, and `claw3d preview` — do NOT use web search.

## When to Trigger This Flow

The intent classifier (`06-intent.md`) sets `consider_search: true` for common/functional objects. When that happens — or when the user explicitly asks to find/search/download a 3D model — follow this workflow.

**Skip this flow and go straight to AI generation** only when the user explicitly says "custom", "artistic", or describes something that clearly doesn't exist as a standard printable part.

---

## Full Workflow: Find → Pick → Preview

### Step 0 — Acknowledge (if triggered by video or image)

Before running anything, send:
> "Great, let me take a look at what you need — give me a moment!"

### Step 1 — Find fitting models (single command)

Run one command. It searches Thingiverse, downloads all thumbnails, fetches each model, packs multi-part models, and fit-checks all of them — returning only the models that physically fit in the printer.

```bash
claw3d find "<query>" --max-passing 4
```

**⚠ `claw3d find` is a long-running command (1–2 minutes).** When you see `Command still running`, this is the SEARCH running — NOT slicing. Do NOT say "Slicing started". Just poll silently with `process poll <session>` every 10 seconds until it finishes.

**Output format:**
```
[1] Balancing Wine Holder
    ID: 660698
    URL: https://www.thingiverse.com/thing:660698
    By: Tanacota
    Thumbnail: thumb_660698.jpg
    Model: model_660698.glb
    Extents: 153.8×160.5×69.8mm
    Rotation applied: none

[2] ...
```

- Build volume is auto-read from the default printer. Pass `--build WxDxH` to override.
- Exit 0 = at least one fitting model found. Exit 1 = none found — refine query and retry.
- All model files are already downloaded and pre-rotated (if a rotation was needed to fit).

### Step 2 — View thumbnails, pick best 4

View all returned thumbnail files visually (you are multimodal). Pick the **4 that best match** what the user needs — considering shape, function, and apparent quality. Record the thing ID for each.

**If fewer than 4 passed**, use however many there are.
**If exit 1 (none fit)**: run `claw3d find` with a refined query (change keywords, add constraints), up to 3 rounds total. After 3 rounds with no match, fall back to AI generation.

### Step 3 — Stamp A/B/C/D badges onto thumbnails, compose grid, send to user

Stamp option letters and compose a single 2×2 grid image (A top-left, B top-right, C bottom-left, D bottom-right):

```bash
claw3d stamp-thumbnails --grid thumb_660698.jpg thumb_123456.jpg thumb_789012.jpg thumb_456789.jpg
# Outputs: thumb_660698_A.jpg, thumb_123456_B.jpg, thumb_789012_C.jpg, thumb_456789_D.jpg
# Grid:   thumb_grid_thumb_660698.jpg  (single 2x2 image)
```

**MANDATORY: Send ONE message with the grid image attached.** Do NOT describe the options without the image. Do NOT skip the `media=` parameter. The user needs to SEE the thumbnails to choose — text-only is useless.

```
message(action="send", text="Here are four options I found:\n\nA — [name/brief reason]\nB — [name/brief reason]\nC — [name/brief reason]\nD — [name/brief reason]\n\nReply with A, B, C, or D — or let me know if none look right and I'll search again or create a custom one.", media="thumb_grid_thumb_660698.jpg")
```

**The `media=` field with the grid image path is REQUIRED.** If you send this message without the grid image attached, the user cannot see the options.

Wait for user response before continuing.

- **User picks A, B, C, or D**: read the thing ID from the `claw3d find` output for that option. Continue to Step 4 with that ID. The model is already downloaded and pre-rotated (if needed) — no re-fetch required.
- **User says none / not quite**: run `claw3d find` with a refined query, repeat from Step 1 — up to 3 rounds total
- **After 3 rounds with no match**: fall back to AI generation

### Step 4 — Get grouped file list (deterministic extension selection)

The chosen model is already downloaded. Use its thing ID to inspect variant/part structure:

```bash
claw3d fetch --list-grouped <thing_id>
```

This deterministically selects the best extension group (STL > OBJ > GLB > 3MF). Parse the output:

- `Best extension: .stl (N file(s))` — what will be downloaded
- `Sub-variants (size/version choices…)` — only shown if multiple size/version options exist
- `Multi-part model (N components…)` — only shown if multiple parts with no size variants

### Step 5 — Handle sub-variants or cosmetic variations (if any)

Read the `--list-grouped` output and follow exactly **one** of these branches:

**→ Output shows "Sub-variants" (size/version choices):**
Ask the user which size/version they want:
> "This model comes in several sizes: small, medium, large. Which would work best for you?"
Once user picks, use `--choose "<variant_tag>"` in Step 6.

**→ Output shows "Cosmetic variations" (same model, minor differences):**
Do NOT ask the user. Auto-select the variant marked `<- auto-selected` and inform them:
> "This model has a [no-text / simplified / …] version — I'll use that for a cleaner print."
Use `--choose "<auto_selected_filename_keyword>"` in Step 6. E.g. if `TiltedWineBottleStand_NoText.stl` is auto-selected, use `--choose "NoText"`.

**→ Output shows "Multi-part model" (multiple components):** all parts are needed — model was already packed by `claw3d find`. Skip directly to Step 7.

**→ Single file or complete-set:** model already downloaded by `claw3d find` — skip directly to Step 7.

### Step 6 — Re-fetch with variant/cosmetic choice (only if sub-variant or cosmetic was needed)

Skip this step if no `--choose` is needed (single file, complete-set, or already fetched correctly).

**With sub-variant chosen (e.g. user picked "large"):**
```bash
claw3d fetch <thing_id> --choose "large" -o model_<ID>.glb
claw3d fit-check -i model_<ID>.stl --apply-rotation
```

**With cosmetic variant auto-selected (e.g. NoText):**
```bash
claw3d fetch <thing_id> --choose "NoText" -o model_<ID>.glb
claw3d fit-check -i model_<ID>.stl --apply-rotation
```

### Step 7 — Dimensions (automatic)

**`claw3d find`** auto-computes dimensions from the fitted extents. The `Extents:` line in the output is the already-rotated bounding box.

> Only run `claw3d dimensions -i <file>` manually if the file was re-fetched in Step 6 (variant selection).

### Step 8 — Generate preview with build plate shown

Build volume is auto-read from the default printer config. Generate the preview with **`--real-scale`** so the user sees the model at its actual physical size relative to the build plate:

```bash
claw3d preview -i model_<ID>.glb -o preview_<ID>.mp4 --real-scale
# or for multi-plate:
claw3d preview -i model_<ID>_plate1.glb -o preview_<ID>_p1.mp4 --real-scale
claw3d preview -i model_<ID>_plate2.glb -o preview_<ID>_p2.mp4 --real-scale
```

`--real-scale` shows the model at its true mm dimensions on the plate. `--build-volume` is auto-read from the default printer (no need to pass it). If no printer is configured yet, ask the user for their build volume and pass it explicitly.

### Step 9 — Send preview(s) to user

**Important:** Thingiverse thumbnails are often lifestyle renders that can look very different from the actual printable model. The 3D preview video is the ground truth — always describe the dimensions so the user understands what they're actually getting.

**Single plate:**
```
message(action="send", text="Here's the 3D preview of option [A/B/C] — [model name]. Print size: X × Y × Z mm. Does this look right? If it doesn't match what you expected from the thumbnail, say so and I'll try the next option.", media="preview_<ID>.mp4")
```

**Multi-plate (N plates needed):**
```
message(action="send", text="This model needs N separate prints. Here's plate 1 (X × Y × Z mm):", media="preview_<ID>_p1.mp4")
message(action="send", text="Plate 2 (X × Y × Z mm):", media="preview_<ID>_p2.mp4")
# … all plates
message(action="send", text="Print them sequentially and assemble. Ready to slice when you are!")
```

---

## Printing Multiple Copies (Duplicate / Fill Plate)

When the user asks to print N copies of a model ("add 3 more", "print 4 of these", "fill the plate"):

1. **Use `claw3d pack --copies N`** on the original STL sidecar. Pass any rotation the user wants baked in via `--rotation-x/y/z`. The packer places all N copies with 2mm gaps.

```bash
# 4 copies, standing up (rotation-x 90), on a 220×215×245mm plate:
claw3d pack -i model_<ID>.stl --copies 4 --rotation-x 90 --build 220x215x245 -o model_<ID>_x4.stl
```

2. **If pack exits with error** ("exceeds build volume"): tell the user how many fit per plate, pack that many, slice, then ask if they want more plates.

3. **If pack produces multiple plates** (`model_<ID>_x4_plate1.stl`, `model_<ID>_x4_plate2.stl`): slice and queue each plate separately.

4. **Slice the packed STL** directly — no rotation flags needed (rotation already baked by pack):

```bash
claw3d slice -i model_<ID>_x4.stl -p <profile_id> -o model_<ID>_x4.gcode --build-volume <WxDxH>
```

**Rotation is already baked in by `--rotation-x/y/z` in the pack step — do NOT also pass rotation to `claw3d slice`.**

---

## Fallback: AI Generation

If no Thingiverse result matches, say:

> "I couldn't find a good match in the Thingiverse library. I can generate a custom 3D model using AI — want me to do that?"

If yes, follow the AI generation flow from `02-ai-forger.md`.

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `claw3d find "<query>" --max-passing 5` | Search + download thumbnails + fetch + fit-check in one shot. Returns only models that fit the printer |
| `claw3d fetch --list-grouped <id>` | Best extension group + sub-variant detection (deterministic) |
| `claw3d fetch --list-only <id>` | Raw file list (complete sets vs parts) |
| `claw3d fetch <id> -o model.glb` | Download + convert to GLB |
| `claw3d fetch <id> --choose "large" -o model.glb` | Download only files matching substring |
| `claw3d pack -i dir/ --build WxHxD -o model.glb` | Arrange multi-part on build plate (2mm gap). Exit 1 if part too large |
| `claw3d pack -i model.stl --copies 4 --build WxHxD -o model_x4.stl` | Duplicate single model 4 times on plate |
| `claw3d pack -i model.stl --copies 4 --rotation-x 90 --build WxHxD -o model_x4.stl` | Duplicate with baked rotation |
| `claw3d fit-check -i model.stl --apply-rotation` | One-off fit check: exits 0 = fits, exits 1 = doesn't fit |
| `claw3d dimensions -i model.glb` | Bounding box + save `.dimensions.json` sidecar for future slicing |
| `claw3d preview -i model.glb -o preview.mp4` | 360° turntable video |

---

## Prerequisites

- **THINGIVERSE_ACCESS_TOKEN** — Free App Token from https://www.thingiverse.com/apps/create

## Error Handling

| Error | Action |
|-------|--------|
| No results / 401 | Check THINGIVERSE_ACCESS_TOKEN in Control UI → Skills → claw3d |
| "No directory providers configured" | Add token in Control UI |
| `claw3d find` exit 1 (0 fitting models) | Refine query and retry, up to 3 rounds; then AI generation |
| `claw3d find` not found | Rebuild Docker: `docker build -f Dockerfile.claw3d -t openclaw:claw3d .` then restart |
