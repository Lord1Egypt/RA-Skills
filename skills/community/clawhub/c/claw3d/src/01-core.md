# claw3d — Unified 3D Workflow

Single skill for the full 3D pipeline: **create** models (AI), **search** (Thingiverse), **slice**, and **print**. Modular—only enabled capabilities appear below.

**CRITICAL — Execute immediately, never stop after acknowledging.** When you tell the user you'll do something (search, convert, preview, slice), you MUST execute the command in the SAME turn. Do NOT end your turn after just acknowledging — the user should never have to ask "done?" to get you to act. Acknowledge AND call the tool in one response.

**Setup order:** Printer first (when printing enabled) → then create/search models → slice → print.

---

## CRITICAL: Setup Flow — Printer + Profile First

**When printing is enabled and the user has no printers configured**, guide them to add a printer AND a linked slicing profile **before** creating or searching for models. A linked profile is required for slicing — it stores the build volume (width × depth × height) extracted from the 3MF, which determines how models are scaled.

**Always run `claw3d printer list` first.** If it returns nothing, go through setup below.

### Step 1 — Ask for printer info + 3MF

Send this message to the user:

> Let's get your printer set up. I need 3 things:
>
> 1. **Printer name** — e.g. "Creality K2 Pro Living Room"
> 2. **IP address + port** — e.g. `192.168.1.50:7125` (Moonraker default: 7125; Creality K2 SE: 4408)
> 3. **Cura project file (.3mf)** — Export it from Cura: **File → Save → "Export Universal Cura Project"** with your printer loaded. This file carries your printer's build volume and all settings — it's required for correct slicing.

Wait for the user to provide all three.

### Step 2 — Add printer with profile in one command

```bash
claw3d printer add --name "<name>" --host <ip> --port <port> --profile-from-3mf <MediaPath>
```

This does everything in one step:
- Registers the printer (name, IP, port) in `~/.config/claw3d/config.json`
- Extracts the Cura machine + extruder definitions from the 3MF
- Creates a slicing profile on the slicer server (stores `build_width`, `build_depth`, `build_height`)
- Links the profile to the printer as its default

**If the user provides name+IP but no 3MF yet:** Add without it (`printer add --name ... --host ... --port ...`), then immediately ask for the 3MF to create the profile:
> Got it! Now please send the Cura project file (.3mf) so I can create the slicing profile. In Cura: **File → Save → "Export Universal Cura Project"**.

Then: `claw3d profile create --from-3mf <MediaPath> --name "<printer_name>_profile"` → `claw3d printer set-profile <printer_id> <profile_id>`

**Printer backends:** Run `claw3d configure backends` to see options (Moonraker, PrusaLink, etc.). Community can add backends in `claw3d/backends/`.

---

## CRITICAL: When User Asks for a Model (Vague Request)

**When the user asks for a 3D model without specifying how** (e.g. "I need a cup", "I want a dragon", "find me a vase", no image attached), **do NOT default to one option.** Offer choices based on what's enabled:

> Great! Would you like me to:
> 1. **Search for existing models** — I'll look on Thingiverse and show you options to download *(if directory enabled)*
> 2. **Create a 3D model from an image** — Send me a sketch or photo and I'll turn it into 3D *(if ai-forger enabled)*
> 3. **Search first, then create from an image if nothing fits** — Best of both *(if both enabled)*

Wait for the user to choose. Only if they explicitly say "create it", "from a photo/sketch", "search", "look up", etc., then proceed.

**Never assume** — "I need a dragon" could mean search OR create from image. Always clarify when ambiguous. **Do not offer text-only 3D generation** — results are inaccurate; always require an image or sketch.

---

## Shared Rules: MediaPath and Unique IDs

**MediaPath:** When the user attaches a file (image, GLB, 3MF), the message includes a **MediaPath** — the full filesystem path. **Always** pass that exact path to `--image`, `--edit-3d`, `--profile-from-3mf`, etc. Copy it character-for-character.

**Unique output paths:** The workspace is shared. Using fixed names (`model.glb`, `preview.mp4`) causes old files from a previous request to be sent to new chats. **Always** derive a short ID from the MediaPath and use it for outputs.

MediaPath format: `.../file_13---b10560d7-18fd-40e9-8a49-996ad190a26c.jpg` — extract the segment after `---` and use the first 8 chars (e.g. `b10560d7`) as `ID`.

If the MediaPath has no UUID (unusual), use `date +%s` to get a unique ID.

---

## User Sends an IMAGE and Asks to 3D Print

**When the user attaches an image** and asks to "3D print this", "print this", "make it printable", etc. — you **CAN** do it *(if ai-forger + slicing + printing enabled)*:

1. **Acknowledge first** — "Yes! I'll turn that into a 3D model and get it ready to print. Give me a minute."
2. **Convert** — `claw3d convert --image <MediaPath> --output model_<ID>.glb`
3. **Get build volume** — Run `claw3d printer list`; note `[WxDxH mm]` if shown.
4. **Preview** — `claw3d preview --input model_<ID>.glb --output preview_<ID>.mp4 [--build-volume WxDxH]` — send the video
5. **Slice** — Run `claw3d profile list`, then slice with `--build-volume <WxDxH>` and profile or `--profile-from-3mf`
6. **Print** — Run `claw3d printers`, then `claw3d print --gcode model_<ID>.gcode`

**Do NOT say** "I can't print from an image" — you can create the 3D model first. If FAL_API_KEY is missing, convert will fail; then tell the user to set it up.

---

## Workflow Overview

```
Get model (search OR create) → optionally edit → slice → print
```

- **Search** — `claw3d search` → `claw3d fetch` → `claw3d dimensions` → present with preview
- **Create** — `claw3d convert --image` (requires image/sketch) → `claw3d preview` → present
- **Edit** — `claw3d convert --edit-3d` (when user sends GLB and asks to modify)
- **Slice** — `claw3d slice` (sends G-code + gcode preview video)
- **Print** — `claw3d print`

---

## Commands (Overview)

| Command | Purpose |
|---------|----------|
| `claw3d convert` | Image/sketch → GLB, or edit existing GLB |
| `claw3d preview` | 360° turntable of 3D model |
| `claw3d search` | Search Thingiverse |
| `claw3d fetch` | Download model from Thingiverse |
| `claw3d dimensions` | Bounding box (for slicing) |
| `claw3d pack` | Arrange multi-part on build plate |
| `claw3d slice` | GLB/STL → G-code |
| `claw3d print` | Upload G-code and start print |
| `claw3d printer` | Add/list/remove printers |
| `claw3d profile` | Create/list slicing profiles |
| `claw3d configure` | Select AI provider, see backends |

Run all via `exec`. Use `claw3d`.
