# OpenClaw 3D — Complete System Workflow

## System Architecture

```
User (Telegram/Discord/Web)
    │
    ▼
┌──────────────────────┐
│  OpenClaw Gateway     │  Node.js — routes messages, manages sessions
│  (openclaw-base)      │  Mounts: ~/.openclaw → /home/node/.openclaw
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  AI Agent (LLM)       │  Gemini / Claude — runs SKILL.md instructions
│  + claw3d CLI tools   │  Python CLI installed in same container
└──────────┬───────────┘
           │
     ┌─────┴──────────────────────┐
     ▼                            ▼
┌──────────────┐    ┌──────────────────────┐
│ Slicer API    │    │ External APIs         │
│ (CuraEngine)  │    │ - FAL.ai (FLUX/Tripo) │
│ FastAPI        │    │ - Gemini (analysis)   │
│ localhost:8000 │    │ - Thingiverse         │
└──────────────┘    └──────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              ┌──────────┐       ┌──────────┐
              │ Printer 1 │       │ Printer N │
              │ Moonraker │       │ PrusaLink │
              └──────────┘       └──────────┘
```

## File Lifecycle & Naming

All files live in the agent's working directory (Docker: `/home/node/.openclaw/workspace/`).

```
model_<ID>.glb                  ← 3D model (Z-up, preview-ready)
model_<ID>.stl                  ← STL sidecar (Z-up, slicing-ready, original scale)
model_<ID>.stl.dimensions.json  ← {x, y, z, max} in mm
model_<ID>.glb.dimensions.json  ← same, for GLB
model_<ID>.source.json          ← provenance: {source: "thingiverse"|"ai", ...}
preview_<ID>.mp4                ← 360° turntable video
model_<ID>.gcode                ← sliced G-code
model_<ID>_gcode_preview.mp4   ← G-code visualization (body=red, supports=yellow)
model_<ID>_parts/               ← multi-part directory (from Thingiverse)
model_<ID>_x4.stl              ← packed N copies
model_<ID>_plate1.stl          ← multi-plate packing output
thumb_<thing_id>.jpg            ← Thingiverse thumbnail
thumb_<thing_id>_A.jpg          ← stamped thumbnail (option badge)
frame_<ID>.jpg                  ← extracted video frame
```

`<ID>` = first 8 chars of UUID from MediaPath, or thing_id for Thingiverse models.

---

## Master Workflow

```
USER MESSAGE
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     1. ENTRY POINT                              │
│                                                                 │
│  What did the user send?                                        │
│  ├─ Text only (no media) ──────────────────────────► [2]        │
│  ├─ Image (photo/sketch) ──────────────────────────► [3]        │
│  ├─ Video ─────────────────────────────────────────► [4]        │
│  ├─ GLB file ──────────────────────────────────────► [5]        │
│  ├─ 3MF file ──────────────────────────────────────► [6]        │
│  └─ G-code file ───────────────────────────────────► [20]       │
└─────────────────────────────────────────────────────────────────┘
```

---

### [2] TEXT ONLY — Intent Classification

```
USER TEXT
    │
    ├─ Printer setup request ──────────────────────────► [6]
    │   ("add printer", "setup", sends IP/port)
    │
    ├─ Print control ──────────────────────────────────► [20]
    │   ("pause", "resume", "cancel", "status",
    │    "preheat", "home", "camera")
    │
    ├─ Rotation request ───────────────────────────────► [15]
    │   ("rotate 90 on X", "flip it", "turn sideways")
    │
    ├─ Slice settings change ──────────────────────────► [16]
    │   ("make it stronger", "more detail", "20% infill")
    │
    ├─ Re-slice / re-print ────────────────────────────► [14] or [20]
    │   ("slice it again", "print it")
    │
    ├─ Multiple copies ────────────────────────────────► [17]
    │   ("print 4 copies", "fill the plate")
    │
    ├─ Edit existing model ────────────────────────────► [5]
    │   ("make it blue", "add wheels") + prior GLB
    │
    ├─ Object request (identifiable) ──────────────────► [7] PRIMARY GATE
    │   ("I need a wine stand", "make me a phone holder")
    │
    └─ Ambiguous ──────────────────────────────────────► ASK
        ("make something for my office")
```

---

### [3] IMAGE RECEIVED — Primary Gate

```
IMAGE + optional text
    │
    ▼
┌──────────────────────────────────────────────┐
│  [7] PRIMARY GATE: SEARCH or CREATE?         │
│                                              │
│  Replicate/copy intent?                      │
│  ("copy this", "make another one",           │
│   "clone this", "I want one like this")      │
│  ├─ YES ─────────────────────────► [9]       │
│  │   (image IS the design reference)         │
│  │                                           │
│  Could Thingiverse have 5+ results?          │
│  ("phone holder", "vase", "hook")            │
│  ├─ YES ─────────────────────────► [10]      │
│  │   SEARCH PATH                             │
│  │                                           │
│  Artistic/custom/sketch/unique?              │
│  ("style of this sculpture", sketch,         │
│   "custom for my setup")                     │
│  └─ YES ─────────────────────────► [8]       │
│      CREATE PATH                             │
└──────────────────────────────────────────────┘
```

---

### [4] VIDEO RECEIVED — Frame Extraction

```
VIDEO + optional text
    │
    ▼
ACK: "Great, let me take a look — give me a moment!"
    │
    ▼
┌──────────────────────────────────────────────┐
│  Can you SEE the video (media attached)?     │
│  ├─ YES (Case A) ────────────────────┐       │
│  │   Watch video natively.           │       │
│  │   Pick best frame timestamp.      │       │
│  │   ▼                               │       │
│  │   claw3d extract-frame            │       │
│  │     --input <video>               │       │
│  │     --timestamp HH:MM:SS          │       │
│  │     --output frame_<ID>.jpg       │       │
│  │                                   │       │
│  └─ NO (Case B: text Description)────┤       │
│      Video pre-processed by OpenClaw.│       │
│      Find video file:                │       │
│      ls -t inbound/ | head -5        │       │
│      ▼                               │       │
│      claw3d extract-frame            │       │
│        --input <video>               │       │
│        --output frame_<ID>.jpg       │       │
│      (Gemini picks frame)            │       │
│                                      │       │
│  Both cases produce: frame_<ID>.jpg  │       │
└──────────────┬───────────────────────┘       │
               │                               │
               ▼                               │
    ┌─ Treat frame as IMAGE ──────► [7] PRIMARY GATE
    │  (same as [3])
```

---

### [5] GLB RECEIVED — Edit Existing Model

```
GLB + user instruction ("make it blue", "add wheels")
    │
    ▼
ACK: "On it! Editing the 3D model. This can take a few minutes."
    │
    ▼
claw3d convert --edit-3d <GLB_path> --prompt "..." --output edited_<ID>.glb
    │
    ▼
claw3d preview --input edited_<ID>.glb --output preview_edited_<ID>.mp4
    │
    ▼
Send preview + GLB to user
    │
    ▼
[13] ASK ABOUT PRINTING (mandatory for AI models)
```

---

### [6] PRINTER SETUP / 3MF RECEIVED

```
3MF file or setup request
    │
    ▼
┌──────────────────────────────────────────┐
│  Has printer been added?                 │
│  ├─ NO ──► Ask for: name, IP, port      │
│  │         + 3MF (Cura project export)   │
│  │         ▼                             │
│  │         claw3d printer add            │
│  │           --name "..."                │
│  │           --host <ip>                 │
│  │           --port <port>               │
│  │           --profile-from-3mf <path>   │
│  │         ▼                             │
│  │         "Printer added! Ready to go." │
│  │                                       │
│  └─ YES, but no profile linked ──────────┤
│       ▼                                  │
│       claw3d profile create              │
│         --from-3mf <path>                │
│         --name "<printer>_profile"       │
│       ▼                                  │
│       claw3d printer set-profile         │
│         <printer_id> <profile_id>        │
│       ▼                                  │
│       "Profile linked! Build volume:     │
│        WxDxH mm. Ready to slice."        │
└──────────────────────────────────────────┘
```

---

### [7] PRIMARY GATE — Decision Point

```
(Already shown in [3] above)

SEARCH ──► [10]
CREATE ──► [8] (analyze) or [9] (replicate)
```

---

### [8] CREATE PATH — Analyze & Generate

```
Image/frame + text
    │
    ▼
claw3d analyze --input <image> [--description "..."] [--pretty]
    │
    ▼
┌──────────────────────────────────────────────────┐
│  Result: native_mode?                            │
│  ├─ true  → Agent does classification            │
│  └─ false → Gemini returned JSON                 │
│                                                  │
│  image_type: sketch | photo | 3d_model | ref     │
│  needs_clarification?                            │
│                                                  │
│  ├─ false (clear subject, enough constraints)    │
│  │   ▼                                           │
│  │   [9] CONVERT                                 │
│  │                                               │
│  ├─ true, ambiguous subject ─────────────────┐   │
│  │   ASK: "I see X and Y. Which to print?"   │   │
│  │   ▼ (user answers)                        │   │
│  │   [9] CONVERT                             │   │
│  │                                           │   │
│  └─ true, functional object needs design ────┤   │
│      Send frame back + ask for red drawing   │   │
│      ▼ (user sends annotated image)          │   │
│      [9] CONVERT (with --annotated-image)    │   │
└──────────────────────────────────────────────────┘
```

---

### [9] CONVERT — Image/Sketch to 3D Model

```
Image + prompt (+ optional annotated image)
    │
    ▼
ACK: "Creating your 3D model now — I'll send it when it's ready!"
    │
    ▼
claw3d convert --image <path> [--annotated-image <path>] --prompt "..." --output model_<ID>.glb
    │
    ▼
claw3d printer list  ← get build volume for preview
    │
    ▼
claw3d preview --input model_<ID>.glb --output preview_<ID>.mp4 [--build-volume WxDxH]
    │
    ▼
Send preview_<ID>.mp4 + model_<ID>.glb to user
    │
    ▼
[13] ASK ABOUT PRINTING (mandatory for AI models)
```

---

### [10] SEARCH PATH — Find on Thingiverse

```
Query (from text or video/image analysis)
    │
    ▼
ACK: "Let me search for that — one moment!"
    │
    ▼
claw3d find "<query>" --max-passing 5
    │
    ├─ Exit 0 (models found) ─────────────────► [11]
    │
    └─ Exit 1 (none fit) ─────────────────────┐
        Round < 3? Refine query, retry ◄──────┘
        Round = 3?
            ▼
        "Couldn't find a match. Want me
         to generate a custom AI model?"
            ├─ YES ──► [9] CREATE
            └─ NO  ──► END
```

---

### [11] SEARCH — Pick & Present Options

```
claw3d find results (1-5 models)
    │
    ▼
Agent views all thumbnails (multimodal)
Picks best 3 matches
    │
    ▼
Stamp A/B/C badges on thumbnails (Python/PIL)
    │
    ▼
Send 3 messages with stamped thumbnails:
  "Option A — [name]: ...",  thumb_A.jpg
  "Option B — [name]: ...",  thumb_B.jpg
  "Option C — [name]: ... Pick A, B, C, or none",  thumb_C.jpg
    │
    ▼
┌────────────────────────────────────────────┐
│  User picks A, B, or C ──────────► [12]    │
│  User says "none" ───────────────► [10]    │
│  (retry with refined query, up to 3 rounds)│
└────────────────────────────────────────────┘
```

---

### [12] SEARCH — Variant Check & Preview

```
Chosen model (thing_id)
    │
    ▼
claw3d fetch --list-grouped <thing_id>
    │
    ▼
┌───────────────────────────────────────────────────────┐
│  Sub-variants (size/version)?                         │
│  ├─ YES ──► Ask user which size ──► claw3d fetch      │
│  │          --choose "<variant>" -o model_<ID>.glb    │
│  │          ▼                                         │
│  │          claw3d fit-check -i model_<ID>.stl        │
│  │            --apply-rotation                        │
│  │                                                    │
│  ├─ Cosmetic variations?                              │
│  │  Auto-select "<auto_selected>" ──► claw3d fetch    │
│  │          --choose "<keyword>" -o model_<ID>.glb    │
│  │                                                    │
│  ├─ Multi-part? Already packed by find. Skip.         │
│  │                                                    │
│  └─ Single file / complete-set? Already fetched.      │
│     Skip to preview.                                  │
└────────────────────┬──────────────────────────────────┘
                     │
                     ▼
claw3d preview -i model_<ID>.glb -o preview_<ID>.mp4 --real-scale
    │
    ▼
Send preview + dimensions:
  "Here's option [X] — [name]. Print size: X × Y × Z mm.
   Does this look right?"
    │
    ▼
┌────────────────────────────────────────────────────┐
│  User confirms ──────────────────────► [14]        │
│  User says "no, try another" ────────► [11]        │
│    (pick next option or re-search)                 │
│  User says "rotate it" ─────────────► [15]         │
│  User says "scale it" ──────────────► [15b]        │
└────────────────────────────────────────────────────┘
```

---

### [13] ASK ABOUT PRINTING (AI models only)

```
After sending AI-generated model + preview
    │
    ▼
"Want me to slice this for 3D printing? If so, I need:
 1. Max print size — longest dimension? (e.g. 100mm, 150mm)
 2. Strength — how strong? (10%, 25%, 50%, 75%, 100%)
 3. Detail — print quality? (10%, 25%, 50%, 75%, 100%)"
    │
    ▼
┌──────────────────────────────────────────────┐
│  User provides values ───────────► [14]      │
│  User says "no" ─────────────────► END       │
│  User says "rotate first" ───────► [15]      │
│  User says "edit it" ────────────► [5]       │
└──────────────────────────────────────────────┘
```

---

### [14] SLICE

```
Model file + user preferences
    │
    ▼
┌──────────────────────────────────────────────────────┐
│  Source?                                             │
│  ├─ AI-generated (no .source.json or source=ai)     │
│  │   Uses: model_<ID>.glb                            │
│  │   Flags: --max-dimension <user_value>             │
│  │          --strength <N> --quality <N>              │
│  │                                                   │
│  └─ Thingiverse (source.json has source=thingiverse) │
│      Prefer: model_<ID>.stl (if exists)              │
│      Fallback: model_<ID>.glb + --no-mesh-clean      │
│      NO --max-dimension (already at real size)        │
│      Flags: --strength <N> --quality <N>              │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
claw3d profile list  ← get profile ID
    │
    ├─ 0 profiles ──► "Need a 3MF first" ──► [6]
    ├─ 1 profile  ──► use it
    └─ 2+ profiles ─► ask or use printer-linked profile
                     │
                     ▼
claw3d slice -i <model> -p <profile_id> -o model_<ID>.gcode
    [--max-dimension N] [--strength N] [--quality N]
    [--no-mesh-clean] [--build-volume WxDxH]
    │
    ▼
POLL: process poll <session> every 10s until "Wrote" or error
    │
    ▼
"Slicing done! Here's the G-code and preview."
Send: model_<ID>.gcode + model_<ID>_gcode_preview.mp4
    │
    ▼
┌──────────────────────────────────────────────────┐
│  User says "print it" ──────────────► [20]       │
│  User says "rotate it" ─────────────► [15]       │
│  User says "make stronger / more detail" ► [16]  │
│  User says "print 4 copies" ────────► [17]       │
└──────────────────────────────────────────────────┘
```

---

### [15] ROTATE

```
User: "rotate 90 on X" / "flip it" / "turn sideways"
    │
    ▼
claw3d rotate -i model_<ID>.glb --rotation-x 90
    │  (BAKED into file — permanent, cumulative)
    │
    ▼
claw3d preview -i model_<ID>.glb -o preview_<ID>_rotated.mp4 [--build-volume WxDxH]
    │  (no rotation flags — file is already rotated)
    │
    ▼
Send preview:
  "Here it is rotated 90° on X — does this look right?"
    │
    ▼
┌──────────────────────────────────────────────┐
│  User confirms ──────────────────► [14]      │
│  User says "rotate more" ────────► [15]      │
│  User says "undo" ───────────────► [15]      │
│    (rotate opposite direction)               │
└──────────────────────────────────────────────┘
```

### [15b] SCALE

```
User: "make it bigger" / "scale to 150mm"
    │
    ▼
claw3d scale -i model_<ID>.glb --max-dimension 150 -o model_<ID>.glb
    │
    ▼
claw3d preview -i model_<ID>.glb -o preview_<ID>_scaled.mp4 [--build-volume WxDxH]
    │
    ▼
Send preview → user confirms → [14]
```

---

### [16] RE-SLICE WITH DIFFERENT SETTINGS

```
User: "make it stronger" / "20% infill" / "thinner layers"
    │
    ▼
Map natural language → CLI flags:
  "stronger"        → --strength 4
  "20% infill"      → --infill-density 20
  "more detail"     → --quality 4
  "0.1mm layers"    → --layer-height 0.1
    │
    ▼
claw3d slice -i <same model> -p <profile_id> -o model_<ID>.gcode
    <new flags> [--build-volume WxDxH]
    │
    ▼
Send updated G-code + preview ──► [14] exit points
```

---

### [17] MULTIPLE COPIES / FILL PLATE

```
User: "print 4 copies" / "fill the plate"
    │
    ▼
claw3d pack -i model_<ID>.stl --copies 4
    [--rotation-x 90] --build <WxDxH>
    -o model_<ID>_x4.stl
    │
    ▼
┌──────────────────────────────────────────────┐
│  All fit on one plate?                       │
│  ├─ YES ──► slice model_<ID>_x4.stl ► [14]  │
│  │                                           │
│  ├─ Multiple plates needed ──────────────┐   │
│  │   plate1.stl, plate2.stl, ...         │   │
│  │   ▼                                   │   │
│  │   Slice each plate                    │   │
│  │   Queue all: claw3d queue add ...     │   │
│  │   ──────────────────────────► [18]    │   │
│  │                                       │   │
│  └─ Doesn't fit (part too large) ────────┤   │
│      "Only N fit per plate. Pack N?"     │   │
│      ▼ (user confirms)                  │   │
│      Retry with fewer copies             │   │
└──────────────────────────────────────────────┘
```

---

### [18] MULTI-PLATE QUEUE

```
Multiple plates sliced and queued
    │
    ▼
claw3d print --gcode plate1.gcode
    │
    ▼
"Plate 1 printing! Let me know when it's done."
    │
    ▼
User: "done" / "next"
    │
    ▼
claw3d queue next
    ├─ Returns next path ──► claw3d print --gcode <path>
    │   "Plate 2 printing!"
    │   ▼
    │   (loop until queue empty)
    │
    └─ Exit 1 (empty) ──► "All plates printed! Assembly time."
```

---

### [20] PRINT CONTROL

```
┌─────────────────────────────────────────────────────────┐
│  claw3d printers  ← check printer availability          │
│  ├─ 0 printers ──► "Add a printer first" ──► [6]       │
│  ├─ 1 printer  ──► use it                              │
│  └─ 2+ printers ─► ask which one                       │
│                                                         │
│  Action?                                                │
│  ├─ PRINT ────► claw3d print --gcode <file> [--printer] │
│  ├─ STATUS ───► claw3d status [--printer]               │
│  ├─ PAUSE ────► claw3d pause [--printer]                │
│  ├─ RESUME ───► claw3d resume [--printer]               │
│  ├─ CANCEL ───► claw3d cancel [--printer]               │
│  ├─ CAMERA ───► claw3d camera [--printer] [--snapshot]  │
│  ├─ PREHEAT ──► claw3d preheat --extruder T --bed T     │
│  ├─ COOLDOWN ─► claw3d cooldown [--printer]             │
│  ├─ HOME ─────► claw3d home [--axes x y z]             │
│  ├─ FILES ────► claw3d files [--path subdir]            │
│  ├─ START ────► claw3d start --file <name>              │
│  └─ STOP ─────► claw3d emergency-stop [--printer]       │
└─────────────────────────────────────────────────────────┘
```

---

## Key Loops & Back-Edges

```
[9]  CONVERT ──► [13] ASK ──► [14] SLICE ──► [20] PRINT
                   │             ▲    │
                   │             │    ├──► [15] ROTATE ──► [14]
                   │             │    ├──► [16] RE-SLICE ──► [14]
                   │             │    └──► [17] COPIES ──► [14]
                   │             │
                   └─ [15] ROTATE (before slicing)
                   └─ [5]  EDIT ──► [13]

[10] SEARCH ──► [11] PICK ──► [12] VARIANT ──► [14] SLICE ──► [20] PRINT
                  ▲                   │
                  └───── user rejects ┘

[10] SEARCH (3 rounds fail) ──► [9] CREATE (fallback)
```

---

## Coordinate System

**Everything is Z-up** except pyrender preview (Y-up, converted at render time).

| Stage | Up | Notes |
|-------|-----|-------|
| Thingiverse STL | Z | Native |
| AI GLB (post-convert) | Z | +90°X baked during `claw3d convert` |
| `claw3d rotate` | Z | Rotates in Z-up space |
| `claw3d pack` | Z | Packs in Z-up space |
| Slicer API | Z | Expects Z-up |
| G-code | Z | Layer height = Z |
| **Preview** | **Y** | −90°X applied at render time only |

---

## State Tracking — What the System Remembers

| State | Where stored | Deterministic? |
|-------|-------------|----------------|
| Model geometry + rotation | In the .glb/.stl file itself | YES — `claw3d rotate` bakes it |
| Model dimensions | .dimensions.json sidecar | YES |
| Model provenance (AI vs Thingiverse) | .source.json sidecar | YES |
| Printer config | ~/.config/claw3d/config.json | YES |
| Slicing profile | Slicer API /profiles registry | YES — but lost on container restart |
| Print queue | ~/.config/claw3d/queue.json | YES |
| **Slice settings (strength, quality)** | **Nowhere — agent memory only** | **NO** |
| **Max print dimension (AI models)** | **Nowhere — agent memory only** | **NO** |
| **User's preferred orientation** | **In the file (after rotate)** | **YES** |
| **Which Thingiverse option was picked** | **Nowhere — agent memory only** | **NO** |
| **Conversation context / intent** | **Agent context window** | **NO** |

---

# Part 2: Improvements — Where Code Should Replace AI Judgment

## Priority 1: Critical — Data Loss / Wrong Behavior

### 1.1 Persist Slice Settings in a Sidecar

**Problem:** When the user says "re-slice but stronger", the agent must remember the previous settings (max-dimension, strength, quality, infill, etc.). If the agent forgets or context is compacted, it either uses defaults or asks again.

**Solution:** Create `model_<ID>.slice_config.json` sidecar. Every `claw3d slice` call writes it. Next slice reads it as defaults.

```json
{
  "max_dimension_mm": 150,
  "strength": 3,
  "quality": null,
  "infill_density": null,
  "layer_height": null,
  "profile_id": "creality_k2_pro_abc123",
  "no_mesh_clean": false,
  "build_volume": "350x350x350"
}
```

`claw3d slice` loads this if it exists, applies CLI overrides on top. Agent only needs to pass what changed.

### 1.2 Persist Model Session Context

**Problem:** After a model is created/fetched, the agent needs to remember: source (AI vs Thingiverse), thing_id, original query, user's chosen option (A/B/C), max print size. If context compacts, all lost.

**Solution:** Extend `model_<ID>.source.json` to become a full session file:

```json
{
  "source": "thingiverse",
  "thing_id": "660698",
  "query": "wine stand",
  "option_letter": "B",
  "original_extents_mm": [153.8, 160.5, 69.8],
  "max_dimension_mm": null,
  "created_at": "2026-03-10T14:30:00Z"
}
```

Or for AI models:
```json
{
  "source": "ai",
  "prompt": "a replica of the black S-hook",
  "original_image": "/path/to/frame.jpg",
  "max_dimension_mm": 100,
  "created_at": "2026-03-10T14:30:00Z"
}
```

### 1.3 Profile Persistence Across Restarts

**Problem:** Slicer API stores profiles in memory + disk, but the profile registry (`profiles.json`) lives inside the Docker container at `/opt/claw3d/profiles/`. If the slicer container restarts, profiles MAY survive (volume-mounted) or MAY NOT.

**Solution:**
- Ensure `/opt/claw3d/profiles/` is volume-mounted in docker-compose
- `claw3d printer add --profile-from-3mf` should store the 3MF path in the printer config, so profiles can be auto-recreated on startup
- Add `claw3d profile ensure` command that checks if the linked profile exists and re-creates it from stored 3MF if not

---

## Priority 2: High — Remove AI Guesswork

### 2.1 Deterministic Source-Based Slice Routing

**Problem:** The agent reads skill instructions to decide: "Is this a Thingiverse model? Use --no-mesh-clean and no scaling. Is this AI? Use --max-dimension." This is fragile — the agent can (and has) applied 100mm scaling to Thingiverse models.

**Solution:** Make `claw3d slice` read `.source.json` and auto-configure:

```python
# In slice_cmd.py, after loading the file:
source_json = _load_source_json(inp)
if source_json and source_json.get("source") == "thingiverse":
    # Auto-enable: no scaling, no mesh clean
    if max_dim is None and not parsed.max_dimension:
        max_dim = None  # explicit: no scaling
    if not parsed.no_mesh_clean:
        parsed.no_mesh_clean = True  # auto-protect
```

The agent doesn't need to remember — the file metadata drives it.

### 2.2 `claw3d pipeline` — Single Command for Common Flows

**Problem:** The most common flows (image → 3D → preview → ask about printing) require the agent to orchestrate 3-4 commands in sequence, with correct flag passing between them. Each step is a chance for the agent to make a mistake.

**Solution:** `claw3d pipeline` wraps common multi-step sequences:

```bash
# Image to preview (CREATE path)
claw3d pipeline create --image <path> --prompt "..." --id <ID>
# Does: convert → preview → outputs both files

# Thingiverse to preview (SEARCH path)
claw3d pipeline search "<query>" --pick 3 --id <ID>
# Does: find → stamp thumbnails → output stamped images

# Slice and print
claw3d pipeline print --model <path> --strength 3 --quality 3 --printer <id>
# Does: slice → poll → print → status
```

This reduces agent orchestration errors dramatically.

### 2.3 Deterministic Thumbnail Stamping

**Problem:** The A/B/C badge stamping is a 15-line Python snippet the agent must copy-paste and modify for each thumbnail. Agents regularly botch this (wrong variable, wrong ID, forget to change letter).

**Solution:** Built into CLI:

```bash
claw3d stamp-thumbnails --thumbnails thumb_660698.jpg thumb_123456.jpg thumb_789012.jpg
# Outputs: thumb_660698_A.jpg, thumb_123456_B.jpg, thumb_789012_C.jpg
```

### 2.4 `claw3d suggest-rotation` — Auto-Optimal Print Orientation

**Problem:** The agent guesses print orientation based on visual intuition. Users often need 2-3 rotation cycles to get it right.

**Solution:** Analyze the mesh and suggest the orientation with least overhang / best bed adhesion:

```bash
claw3d suggest-rotation -i model_<ID>.glb --build <WxDxH>
# Output: --rotation-x 90 (flat base detected, 82% bed contact)
```

This could use simple heuristics: find the largest flat face, orient it downward.

---

## Priority 3: Medium — UX & Robustness

### 3.1 Undo/History for Model Edits

**Problem:** `claw3d rotate` overwrites the file. If the user says "undo that rotation", there's no way back except rotating the opposite direction (which accumulates floating-point errors).

**Solution:** Keep a backup before each destructive operation:

```
model_<ID>.glb              ← current
model_<ID>.glb.bak.1        ← before last rotate
model_<ID>.glb.bak.2        ← before that
```

Add `claw3d undo -i model_<ID>.glb` that restores the most recent backup.

### 3.2 Unified Model Status Command

**Problem:** To understand "what has happened to this model", the agent needs to check multiple files: .source.json, .dimensions.json, .slice_config.json, and look for .gcode / preview files.

**Solution:** `claw3d model-status -i model_<ID>.glb`:

```
Model: model_660698.glb
Source: Thingiverse (thing:660698 — "Balancing Wine Holder")
Dimensions: 153.8 × 160.5 × 69.8 mm
Rotation: 90° X (baked)
Sliced: YES → model_660698.gcode (strength 3, quality 3)
Printed: NO
Preview: preview_660698.mp4
```

The agent can call this at the start of a session to recover full context.

### 3.3 Smart Default Max Dimension

**Problem:** For AI models, the agent must ask the user for max print size. But the printer's build volume is known. The agent should suggest a reasonable default.

**Solution:** Already partially there in 05-printing.md, but make it code:

```python
# In slice_cmd.py, for AI models with no --max-dimension:
if source == "ai" and max_dim is None:
    build_vol = get_default_printer_build_volume()
    if build_vol:
        suggested = min(build_vol) * 0.8  # 80% of smallest axis
        print(f"No --max-dimension specified. Suggested: {suggested:.0f}mm "
              f"(80% of printer's {min(build_vol):.0f}mm axis)", file=sys.stderr)
```

### 3.4 Webhook / Event Notifications

**Problem:** Long operations (slice, convert, preview) require the agent to poll. If the agent's context compacts during polling, it loses track.

**Solution:** Add optional webhook callbacks:

```bash
claw3d slice ... --webhook "http://localhost:PORT/callback"
# Slicer calls webhook when done → OpenClaw can notify agent
```

### 3.5 Health Check / Dependency Validation

**Problem:** Multiple services must be running (slicer, printer), multiple API keys configured (FAL, Gemini, Thingiverse). Failures are discovered mid-workflow.

**Solution:** `claw3d doctor`:

```
[OK] Slicer API: http://localhost:8000 (responding)
[OK] FAL_API_KEY: configured
[OK] GEMINI_API_KEY: configured
[OK] THINGIVERSE_ACCESS_TOKEN: configured
[OK] Printer: Creality K2 Pro (192.168.28.102:4408) — online, idle
[OK] Profile: creality_k2_pro_profile (350×350×350mm)
[WARN] ffmpeg: not found (video frame extraction will fail)
```

---

## Priority 4: Structural / DB Improvements

### 4.1 Model Registry (Replace File-Convention DB)

**Problem:** The entire "database" is implicit file naming conventions (`model_<ID>.glb`, `model_<ID>.source.json`, etc.). This is fragile — files can be orphaned, IDs confused, and there's no way to list "all models in this session."

**Solution:** SQLite or JSON registry at `~/.config/claw3d/models.json`:

```json
{
  "models": {
    "660698": {
      "id": "660698",
      "source": "thingiverse",
      "thing_id": 660698,
      "name": "Balancing Wine Holder",
      "files": {
        "glb": "model_660698.glb",
        "stl": "model_660698.stl",
        "gcode": "model_660698.gcode",
        "preview": "preview_660698.mp4",
        "gcode_preview": "model_660698_gcode_preview.mp4"
      },
      "dimensions_mm": [153.8, 160.5, 69.8],
      "slice_config": { "strength": 3, "quality": 3 },
      "rotation_history": ["X+90"],
      "status": "sliced",
      "created_at": "2026-03-10T14:30:00Z",
      "printed_at": null
    }
  }
}
```

Commands:
```bash
claw3d models list              # all models in workspace
claw3d models show <ID>         # full detail
claw3d models clean             # remove orphaned files
```

### 4.2 Session Tracking

**Problem:** No concept of "this conversation's models." If the user starts a new chat, the agent doesn't know what models exist from previous sessions.

**Solution:** Add session_id to model registry. The OpenClaw gateway already has session IDs — pass them through:

```bash
claw3d convert --image ... --session <session_id> --output model_<ID>.glb
```

Then `claw3d models list --session <id>` shows only that session's work.

### 4.3 Print Job Tracking

**Problem:** After `claw3d print`, there's no record of what was printed, when, on which printer, or the outcome. Can't answer "what did I print last week?"

**Solution:** Print history in registry:

```json
{
  "print_history": [
    {
      "model_id": "660698",
      "gcode": "model_660698.gcode",
      "printer_id": "creality_k2_pro",
      "started_at": "2026-03-10T15:00:00Z",
      "status": "completed",
      "duration_minutes": 47
    }
  ]
}
```

### 4.4 Queue Improvements

**Problem:** Queue is a flat list of file paths. No metadata about which model, what plate number, estimated time.

**Solution:** Enrich queue items:

```json
{
  "path": "model_660698_x4_plate1.gcode",
  "label": "Wine Stand × 4 — Plate 1/2",
  "model_id": "660698",
  "plate_number": 1,
  "total_plates": 2,
  "estimated_time_seconds": 2400,
  "estimated_filament_grams": 45.2
}
```

These estimates come from the slicer job status (already available after slicing).

---

## Summary: Top 5 Impact Improvements

| # | Change | Impact | Effort |
|---|--------|--------|--------|
| 1 | **Source-based auto-routing in slice** (2.1) | Eliminates scaling/mesh-clean bugs forever | Low |
| 2 | **Slice config sidecar** (1.1) | Agent never forgets settings on re-slice | Low |
| 3 | **Model registry** (4.1) | Single source of truth, replaces fragile naming | Medium |
| 4 | **`claw3d pipeline`** (2.2) | Reduces 4-step orchestration to 1 command | Medium |
| 5 | **`claw3d doctor`** (3.5) | Catches missing config before user hits errors | Low |
