---
name: genor-comfy-gate
description: Comprehensive ComfyUI operations reference for the Genor-Comfy-Gate gateway. Multi-modal: audio, images, video.
author: GenorTG (handle)
attribution: Adapted from the GSD Core project by TÂCHES / open-gsd (https://github.com/open-gsd/gsd-core)
metadata:
  openclaw:
    install:
      - id: node
        kind: node
        package: .
        label: "Install Node.js dependencies"
      - id: pm2
        kind: shell
        command: "bash ./install.sh"
        label: "Run install script (PM2 setup, dirs)"
---

# Genor-Comfy-Gate — Comprehensive Skill

**GitHub:** https://github.com/GenorTG/Genor-Opencaw-Comfyui-Gate
**Install:** `bash install.sh` | **Update:** `bash autobuild.sh`

**THE authoritative reference for ALL ComfyUI operations through our gateway.**
Multi-modal: audio, images, video (future). Read this before any generation. Updated as we learn.

## Workspace Structure

All user-specific workflows, custom instructions, and generated outputs MUST be stored inside a dedicated workspace folder:

```
~/projects/genor-comfyui/
├── workflows/           # Custom/user-specific ComfyUI workflow JSONs
│   ├── lustify-sdxl.json
│   ├── my-custom-workflow.json
│   └── ...
├── custom_instructions/ # User-specific prompting notes, style guides, presets
│   ├── prompt_templates/  # Per-model prompt generation system prompts
│   │   ├── illustrious_xl_prompt_gen.md
│   │   ├── animagine_xl_40_prompt_gen.md
│   │   ├── sdxl_base_prompt_gen.md
│   │   ├── z_image_turbo_prompt_gen.md
│   │   └── base_sd_prompt_gen.md
│   └── ...
├── generations/         # Generated images, audio, and their metadata
│   ├── images/
│   ├── audio/
│   └── ...
└── exports/             # Exported/shareable workflow packages
    └── ...
```

**Rules:**
- ALWAYS place new workflows in `~/projects/genor-comfyui/workflows/`
- ALWAYS save custom prompting instructions in `~/projects/genor-comfyui/custom_instructions/`
- Generated media goes to `~/media/comfy/` (gateway default), but reference/custom outputs go to `~/projects/genor-comfyui/generations/`
- Create the folder structure on first use if it doesn't exist
- Reference this structure when uploading workflows via `genor-comfy-gate__upload_workflow`

## Modalities

| Type | Status | Workflow | Model |
|------|--------|----------|-------|
| 🎵 Audio | ✅ Active | `acestep-rapcore` | ACE-Step 1.5 SFT merge |
| 🎬 Video | 🔜 Planned | — | — |

The gateway is modality-agnostic — it submits any workflow JSON to ComfyUI, polls, waits, downloads, and saves. Adding a new modality means adding a workflow file + WORKFLOW_INFO entry. The `type` field determines output dir (`audio/` or `images/`).

## Gateway

| Property | Value |
|----------|-------|
| Endpoint | `http://127.0.0.1:8188` |
| Auth | `x-api-key` header (localhost exempt) |
| Managed by | pm2 (`genor-comfy-gate`) |
| Location | `./` (installed dir) |
| Config | `env` / `COMFY_SERVERS` var |

## Backend Servers

Configure your ComfyUI backends via the `COMFY_SERVERS` environment variable:

```json
[
  {"url": "http://127.0.0.1:8188", "id": "local", "priority": true, "weight": 1}
]
```

Default: single local server at `http://127.0.0.1:8188`

| ID | URL | Priority |
|----|-----|----------|
| local | `http://127.0.0.1:8188` | ★ (default) |

### Load Balancing Logic (in `pickServer()`)
1. PRIMARY always preferred when IDLE (0 running tasks)
2. If PRIMARY has ANY running task → ALL new requests → SECONDARY
3. If SECONDARY offline → fallback to PRIMARY regardless
4. Download ALWAYS from the server that generated the file (`server.url`)

---

## Workflows

### `acestep-aio` — ACE-Step 1.5 Audio Generation

**Model:** `aceStep15Music_sft17BAIO.safetensors` (ACE-Step 1.5 SFT merge)

```
Workflow Pipeline:
  CheckpointLoader(160) → AnySwitch(model/clip/vae) → TextEncode(94) → KSampler(35 steps, dpmpp_3m_sde, beta, cfg=1) → VAEDecodeTiled → SaveAudioMP3(104)
  Lyrics: String(252) → TextEncode.lyrics
  Duration: mxSlider(274) → TextEncode + EmptyLatent
  Negative: ConditioningZeroOut(47) → zeroes the positive conditioning
```

#### Node Map

| Node | Class | Role | Injections |
|------|-------|------|------------|
| **94** | `TextEncodeAceStepAudio1.5` | Main text encoder | `prompt` → `tags`, `lyrics` ← 252, `bpm`, `keyscale`, `duration` ← 274, `language` |
| **252** | `String` | Lyrics feed into node 94 | `lyrics` → `String` |
| **3** | `KSampler` | Denoising (35 steps, dpmpp_3m_sde, beta, cfg=1) | `seed` ← 307 |
| **98** | `EmptyAceStep1.5LatentAudio` | Creates latent audio space | `seconds` ← 274 |
| **104** | `SaveAudioMP3` | Output V0 MP3 | — |
| **128** | `VAEDecodeAudioTiled` | VAE decode (tile=512, overlap=64) | — |
| **160** | `CheckpointLoaderSimple` | Loads model | — |
| **274** | `mxSlider` | Song duration (seconds) | `duration` → `Xi` and `Xf` |
| **307** | `Seed (rgthree)` | Global seed | `seed` → `seed` |
| **257** | `Text Concatenate` | Builds output filename | artist+title+path |
| **47** | `ConditioningZeroOut` | Negative prompt (zeroed) | — |
| **78** | `ModelSamplingAuraFlow` | Shift=13 | **Bypassed by default** — use `model_sampling: true` to enable |

#### Reference Nodes (informational, in workflow but not connected)

| Node | Content |
|------|---------|
| **317** | Genre description table (38 genres with tags) |
| **318** | Keyscale/BPM reference table (38 genres × scale + key + BPM) |
| **320** | Structure example (metalcore duet with timeline) |
| **321** | Preset example (detailed scene-by-scene prompt) |
| **319** | LLM input example (NSFW lyrics prompt format) |
| **400** | Disconnected tags node (original rapcore tags, kept for reference) |

#### Generation Parameters

```json
{
  "workflow": "acestep-rapcore",
  "prompt": "comma-separated tags (under 512 chars)",
  "lyrics": "structured lyrics with [section] tags",
  "duration": 180,
  "bpm": 150,
  "keyscale": "E minor",
  "language": "en",
  "seed": -1
}
```

All parameters EXCEPT `prompt` and `lyrics` are optional. Omitted parameters keep their workflow defaults.

**`model_sampling` (optional, boolean):** Enables ModelSamplingAuraFlow (shift=13) for acestep-aio. **Bypassed by default** — it's 50/50 whether it improves quality, so safer to leave off. Set `model_sampling: true` if you want to experiment with it on.

---

### The 8 Dimensions
Every caption should cover as many as possible, in 5-8 comma-separated tags:

1. **Style/Genre** — metalcore, synthwave, drum and bass, pop, folk
2. **Emotion/Atmosphere** — melancholic, euphoric, aggressive, dreamy, dark
3. **Instruments** — distorted guitar, 808 bass, strings, piano, synths
4. **Timbre/Texture** — warm, crisp, punchy, lush, airy, bright
5. **Vocal** — male/female, raspy, clean, powerful, breathy, belting
6. **Production** — polished, lo-fi, live, studio, dry, glossy
7. **Era** — 80s, 90s, modern, retro, vintage
8. **Speed/Rhythm** — driving, groovy, frantic, mid-tempo, laid-back

### Rules
- **5-8 tags max** — more degrades quality
- **BPM/key in parameters, NOT caption** — they're separate fields
- **No conflicting pairs** — e.g. "classical strings" + "death metal growls"
- **Texture words matter heavily** — they control mix/production quality
- **Specific > vague** — "melancholic piano ballad, female breathy vocal" > "sad song"
- **Repeat what you want more of** — repetition reinforces

### Known Good Captions
```
pop, piano+strings+guitar, female warm vocal, melancholic intimate, bedroom pop
```
```
rock, metal, heavy distorted guitar, powerful drums, melodic vocals, aggressive, epic, dramatic, guitar solo
```
```
heavy distorted guitar, fast thrash drums, pounding bass, aggressive, dark
```
```
rapcore metal fusion, nu-metal, punchy bass, warm distorted guitar, crisp drums, melodic chorus, heavy grooves, atmospheric, polished production, angsty female vocal, emotional
```

### Tags That Cause Problems
- `raw`, `gritty`, `distorted` (without balancing warmth) → metallic scraping, flat bass
- `heavy bass` → boomy/muddy; prefer `punchy bass`, `deep sub-bass`, `defined bass`
- `aggressive` on instruments → harsh overtones; use on emotion/vocal instead
- Too many instrument tags → cluttered, muddy mix
- "classical" + any heavy genre → contradictory, degrades both

### Texture Word Guide
| Word | Effect |
|------|--------|
| `warm` | Analog-style saturation, smooth high end |
| `crisp` | Clean transients, defined attacks |
| `punchy` | Tight, compressed low-mids, good for bass/kick |
| `bright` | Boosted highs, airy presence |
| `lush` | Wide stereo, rich harmonics, reverb-heavy |
| `dry` | Close-mic sound, minimal reverb |
| `airy` | Spacious high end, breathy |
| `polished` | Studio-quality, balanced EQ |
| `raw` | **USE WITH CAUTION** — unprocessed, potentially harsh |
| `gritty` | **USE WITH CAUTION** — distortion artifacts |

---

## Lyrics Engineering (ACE-Step)

### Required Structure Tags
ACE-Step REQUIRES section markers to align music with lyrics:
```
[Intro], [Verse], [Pre-Chorus], [Chorus], [Bridge], [Build], [Drop],
[Breakdown], [Guitar Solo], [Piano Interlude], [Outro]
```

### Vocal Control Tags (on own line inside sections)
```
[whispered], [raspy vocal], [powerful belting], [spoken word],
[falsetto], [harmonies], [clean vocal]
```

### Energy Tags (on own line inside sections)
```
[high energy], [low energy], [building energy], [euphoric],
[melancholic], [dreamy], [aggressive]
```

### Lyric Writing Rules
- **6-10 syllables per line** — fits the 5Hz LM planner
- **Natural phrasing** — write like human speech, not poetry
- **Avoid AI clichés:** "neon skies", "electric hearts/dreams", "breaking chains", "rising up", "fire inside"
- **Section description hints** on intro/outro lines: `(bass rumbles in)`, `(drums fade to silence)`
- **UPPERCASE = shouted/emphasized**
- **(parentheses) = background vocals/harmonies**

### 🔴 OBOWIĄZKOWA CHECKLISTA PRZED WYSŁANIEM TEKSTU DO GENERACJI
**Zanim wyślesz jakikolwiek tekst do ACE-Step — musisz odpowiedzieć sobie na każde z tych pytań i nie wysłać dopóki wszystkie nie są "TAK":**

1. **„Czy ten tekst ma sens?”** — czy opowiada spójną historię? Czy ma flow od intro do outro? Czy sekcje łączą się logicznie?
2. **„Czy jest gramatycznie poprawny?”** — bez błędów ortograficznych, interpunkcyjnych, składniowych. Sprawdź szczególnie polskie znaki, odmianę, przecinki.
3. **„Czy pasuje do autora/projektu?”** — czy ton, styl, przekleństwa, energia pasują do artysty (KOSTI/Bonnie Bones)? Czy brzmi jak ta postać?
4. **„Czy muzyka i jej kolejność ma sens?”** — czy struktura (Intro→Verse→Chorus→Verse→Bridge→Chorus→Outro) jest logiczna? Czy energia rośnie i opada naturalnie? Czy długość ogólnie ma sens (~120-180s)?
5. **„Czy duration jest odpowiednie?”** — 120-180 sekund standard. NIGDY nie wysyłaj duration=150 jeśli nie sprawdziłeś że tyle ma być.
6. **„Czy wiek autora brzmi wiarygodnie?”** — nie pisz „mam 15 lat”, „young girl”, „teen” w tekstach dorosłych artystów. KOSTI/Bonnie Bones to dorośli wykonawcy.

**Dopiero gdy na każde pytanie odpowiedź brzmi TAK — możesz wysłać do generacji.**

### Energy Flow Pattern
```
Intro       → [low energy]       — sparse, building
Verse 1     → [low energy]       — verse, storytelling, restrained
Pre-Chorus  → [building energy]  — tension rising
Chorus      → [high energy]      — maximum impact, full instrumentation
Verse 2     → [low energy]       — second verse, slightly more energy
Pre-Chorus  → [building energy]
Chorus      → [high energy]      — second chorus often bigger (harmonies)
Bridge      → [low energy]       — stripped back, different perspective
Breakdown   → [high energy]      — instrumental intensity (optional)
Final Chorus→ [high energy]      — biggest version
Outro       → [low energy]       — fade out
```

---

## Genre Reference (from workflow node 317)

### Key Genres & Their Tags

**Electronic**
- EDM/House: `four-on-the-floor, bright synths, uplifting, dance-driven, glossy production, rhythmic, energetic`
- Techno: `mechanical, hypnotic rhythms, minimalistic, pulsing bass, industrial textures, dark, repetitive`
- Trance: `euphoric, soaring leads, emotional pads, rolling basslines, uplifting, spacious, melodic, anthemic`
- Drum & Bass: `rapid breakbeats, deep sub-bass, high-energy, sharp percussion, rolling rhythms, crisp, driving`
- Dubstep: `heavy bass drops, wobbling synths, aggressive textures, syncopated rhythms, dark, cinematic, gritty`
- Future Bass: `shimmering chords, side-chained synths, emotional, bright leads, bouncy rhythms, glossy, melodic`
- Trap: `booming 808s, sharp hi-hats, atmospheric pads, swaggering, dark, punchy, spacious`

**Rock/Metal**
- Classic Rock: `crunchy guitars, steady drums, warm analog tone, energetic, melodic, vintage, riff-driven`
- Hard Rock: `heavy riffs, powerful drums, gritty vocals, aggressive, energetic, distorted, bold, driving`
- Metal: `distorted guitars, fast drums, dark atmosphere, aggressive, heavy, intense, powerful, tight`
- Progressive Metal: `complex structures, technical riffs, atmospheric layers, dramatic, epic, polished, dynamic`

**Urban**
- Boom Bap: `dusty drums, soulful samples, rhythmic, warm textures, punchy kicks, nostalgic, organic`
- Lo-Fi Hip-Hop: `mellow beats, vinyl crackle, soft keys, relaxed, dreamy, warm, minimal, hazy`
- Drill: `sliding 808s, haunting melodies, gritty textures, cold atmosphere, syncopated, tense, urban`

**Pop**
- Pop: `catchy hooks, bright synths, polished production, upbeat, melodic, modern, radio-ready, clean`
- Synth-Pop: `retro synths, bright pads, melodic, nostalgic, electronic, polished, dreamy, airy`
- K-Pop: `glossy production, bright synths, genre-blending, catchy hooks, polished, theatrical, vibrant`

**Soft/Ambient**
- Ambient: `soft pads, atmospheric textures, spacious, minimal, calm, evolving, dreamy, subtle, meditative`
- Cinematic: `sweeping strings, dramatic percussion, epic, emotional, grand, polished, powerful`

---

## Keyscale & BPM Reference (from workflow node 318)

| Genre | Scale | Key Range | BPM Range |
|-------|-------|-----------|-----------|
| EDM/House | Minor, Dorian | D#m–Am | 120–128 |
| Techno | Phrygian, Minor | Fm–A#m | 125–135 |
| Trance | Major, Mixolydian | A–D | 130–142 |
| Drum & Bass | Minor, Dorian | Em–Gm | 170–178 |
| Dubstep | Minor, Phrygian | Fm–G#m | 138–150 |
| Future Bass | Major, Minor | C–F | 140–160 |
| Trap | Harmonic Minor | Fm–Am | 130–150 |
| Hip-Hop | Minor, Dorian | Dm–Gm | 85–95 |
| Lo-Fi | Dorian, Lydian | Cm–Fm | 60–85 |
| Pop | Major, Mixolydian | C–G | 90–130 |
| Classic Rock | Minor Pentatonic | Em–Am | 100–140 |
| Hard Rock | Minor, Phrygian | Em–Gm | 120–160 |
| Metal | Phrygian, Harmonic Minor | Dm–F#m | 140–200 |
| Prog Metal | Dorian, Melodic Minor | C#m–F#m | 120–180 |
| Blues | Blues Scale, Minor Pentatonic | Em–Am | 70–120 |
| Funk | Mixolydian, Dorian | E–A | 100–120 |
| Disco | Mixolydian, Major | F–Bb | 110–130 |
| R&B | Dorian, Minor | Dm–Gm | 60–100 |
| Ambient | Lydian, Dorian | C–F | 60–90 |
| Cinematic | Minor, Harmonic Minor | Cm–Fm | 60–120 |
| Reggae | Major, Mixolydian | A–D | 70–90 |
| K-Pop | Major, Minor | C–F# | 100–140 |
| Anime OST | Lydian, Major | C–E | 80–160 |

---

## Structure Planning (from workflow node 320)

The workflow includes an example of how to structure a caption WITH a song structure plan:

```
metalcore, symphonic elements, theatrical, duet, heavy distorted guitar,
bright piano, studio-polished, dramatic, melodic, epic, intense.

Structure:
- Intro: brief intro dramatically builds to first verse
- Verse 1: atmospheric piano, sets scene, raspy male vocal only
- Verse 2: guitar power chords, groovy, young female vocal only
- Chorus: anthemic, layered, male+female duet harmonies
- Bridge: atmospheric, dreamy, calm, female vocal only
- Build-up: builds to epic instrumental solo
- Instrumental: fast guitar solo, lead licks, virtuoso shred
- End: powerful ending
```

This can go in the caption to give the model a temporal roadmap.

---

## Scene-by-Scene Prompting (from workflow node 321)

For maximum control, describe each section's instrumentation and mood in prose:

```
Intro: A metalcore-tinged, symphonic swell opens the track, with bright piano glimmering
over theatrical strings. Tension rises—studio-polished, dramatic—until it snaps into verse.

Verse 1: Drops to atmospheric piano, soft but charged. Raspy male vocal, intimate, whispered.
No guitars—just piano, subtle pads, suspended breath.

Verse 2: Guitar power chords crash in, groovy pulse. Young female vocal, bright and soaring.
Symphonic elements widen the space, cinematic lift.

Chorus: Erupts into anthemic, epic chorus. Male+female duet harmonies. Distorted guitars,
sweeping strings, pounding drums—polished, intense.

Bridge: Everything falls away. Dreamy, atmospheric, weightless. Soft pads, distant piano,
female vocal airy and ethereal. Suspended.

Build-up: Rhythmic pulses return. Low strings, tom rolls, rising synths. Guitars re-enter
in bursts. Energy coils toward instrumental break.

Instrumental: Fast guitar solo, virtuoso shred, rapid licks, melodic flourishes.
Symphonic backing, metalcore precision drums. Flashy, intense, climactic.
```

---

## Full API Reference

### Core Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check + server statuses |
| GET | `/workflows` | List available workflows with types |
| POST | `/generate-and-wait` | **PRIMARY** — submit, wait, download, save. Use this for all generation. |
| POST | `/prompt` | Submit workflow, return prompt_id |
| GET | `/history/:prompt_id` | Get single prompt result |
| GET | `/history` | Aggregated history from all servers |
| GET | `/queue` | Aggregated queue (running + pending) |
| GET | `/view` | Proxy media file download |
| GET | `/system_stats` | First alive server system info |
| GET | `/object_info` | Proxy to ComfyUI object_info |
| GET | `/extensions` | Proxy to ComfyUI extensions |

### Image Generation (legacy, use generate-and-wait instead)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/generate` | Get generation options form |
| POST | `/generate` | Submit image generation |
| POST | `/upload/image` | Upload image to ComfyUI input dir |

### Media Management

| Method | Path | Description |
|--------|------|-------------|
| GET | `/media-list` | List generated files (name, size, date, preview URLs) |
| POST | `/media-link-once` | Create one-time access token for a file |
| GET | `/media-once/:token` | Access file via one-time token (no API key needed) |

### Workflow Injection

| Method | Path | Description |
|--------|------|-------------|
| POST | `/workflow/:name/prompt` | Quick prompt submit for named workflow (auto-injects) |

### `POST /generate-and-wait` — Full Reference

```bash
curl -s -X POST http://127.0.0.1:8188/generate-and-wait \
  -H "Content-Type: application/json" \
  -d '{
    "workflow": "acestep-rapcore",
    "prompt": "...",
    "lyrics": "...",
    "duration": 200,
    "bpm": 150,
    "keyscale": "E minor",
    "language": "en",
    "seed": -1
  }'
```

**Audio params:** `prompt` (required), `lyrics`, `duration`, `bpm`, `keyscale`, `language`, `seed`  
**Image params:** `prompt` (required), `aspect_ratio`, `seed`, `steps`, `cfg`  
**Common:** `workflow` (default: `acestep-rapcore`), `client_id`

**Success response:**
```json
{
  "status": "ok",
  "file": "/var/data/comfy-media/audio/example-output.mp3",
  "filename": "example-output.mp3",
  "type": "audio",
  "server": "sec",
  "workflow": "acestep-rapcore",
  "file_size": 5882890
}
```

Output saved with metadata sidecar (`.json`) in `~/media/comfy/<audio|images>/`.

---

## Operational Notes

### Restart
```bash
pm2 restart genor-comfy-gate
pm2 logs genor-comfy-gate --lines 20
```

### Status Check
```bash
curl -s http://127.0.0.1:8188/ | python3 -m json.tool
curl -s http://127.0.0.1:8188/queue | python3 -m json.tool
```

### Media Location
```
~/media/comfy/audio/    — generated MP3 files + .json sidecars
~/media/comfy/images/   — generated PNG files + .json sidecars
```

### Gateway Behavior
- Submits workflow JSON with injected parameters
- Polls `/history/:prompt_id` every 2s until complete/fail/timeout
- Timeout: 600s (10 min) per generation
- After completion: waits 3s for file write, then downloads
- Saves to media dir with timestamped name + incrementing sequence number
- Metadata sidecar written alongside media file

### Growing Our Knowledge
When we discover new caption patterns, texture word effects, or workflow tricks:
1. Update this SKILL.md
2. Note the date and what we learned in `CHANGELOG.md` (next to this skill)

---

---

## Image Prompt Engineering Reference

**Baseline reference for ALL image generation models.** Use this when constructing prompts for any image workflow. Each model has its own syntax — using the wrong format produces garbage.

### Quick Model ID

| Model | Prompt Style | Quality Tags (end) | Negatives? | Notes |
|-------|-------------|-------------------|------------|-------|
| **Illustrious XL** | Booru tags, underscores, commas | `masterpiece, best quality, absurdres` | Yes | Most important tags FIRST. CFG 3-6. ~248 token limit. |
| **Animagine XL 4.0** | Tags + score tags | `masterpiece, high score, great score, absurdres` | Yes | Score tags have stronger impact. CFG 4-7. Euler a, 28 steps. |
| **SDXL Base** | Natural language + photography terms | N/A (built into description) | Yes | Camera/lens specs, DOF, lighting. CFG 7. DPM++ 2M Karras. |
| **Z-Image Turbo** | Full English sentences ONLY | N/A | **NO** (CFG=0) | No tag soup. Photography vocab required. ~512 token cap. |
| **Base SD / 1.5** | Hybrid: NL description + quality tags | `masterpiece, best quality, highres` | Yes | Most flexible. CFG 7-9. 75 token chunks. |

---

### Illustrious XL (LUSTIFY, WAI, Hyphoria, NoobAI)

**Format:** Booru-style tags, comma-separated, underscores for multi-word.

**Structure (order matters — first = most influence):**
```
subject, physical attributes, clothing, pose, environment, lighting, camera angle, quality tags
```

**Quality tags (ALWAYS at end):** `masterpiece, best quality, absurdres`

**Negative prompt:**
```
worst quality, low quality, bad anatomy, bad hands, extra fingers, blurry, lowres, signature, watermark, username
```
For mature content add: `loli, shota, child, aged_down`

**Weighting:** `(tag:1.2)` = 20% stronger, `(tag:0.8)` = 20% weaker

**Settings:** CFG 3-6, Steps 25-32, Sampler Euler a

**Rules:**
- No score tags (Pony-style scores don't work)
- ~248 token limit before dilution
- Artist tags work if artist has enough Danbooru presence
- For mature: add `mature, mature_female` to positive to counter loli bias

**Example:**
```
1girl, teenage, slavic, high cheekbones, fair skin, light blue eyes, long blonde hair, ponytail, school uniform, white button-up shirt, red ribbon, pleated miniskirt, cheerleader, pom-poms, thighhigh_socks, loafers, standing, leaning against locker, looking at viewer, confident smile, school hallway, afternoon sunlight, soft shadows, masterpiece, best quality, absurdres
```

---

### Animagine XL 4.0

**Format:** Tags with specific ordering. Score tags work here (unlike Illustrious).

**Structure:**
```
1girl/1boy/1other, character name, series, rating, everything else, quality tags
```

**Quality tags (ALWAYS at end):** `masterpiece, high score, great score, absurdres`

**Score tags (stronger impact than quality tags):** `high score`, `great score`, `good score`, `average score`, `bad score`, `low score`

**Rating tags:** `rating:safe`, `rating:questionable`, `rating:explicit`

**Negative prompt:**
```
lowres, bad anatomy, bad hands, text, error, missing finger, extra digits, fewer digits, cropped, worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry
```

**Settings:** CFG 5, Steps 28, Sampler Euler a

**Rules:**
- Score tags have STRONGER impact than quality tags — always include both
- Rating tags are recognized and work well
- Tags preferred over natural language

**Example:**
```
1girl, teenage, slavic, high cheekbones, fair skin, light blue eyes, long blonde hair, ponytail, school uniform, white shirt, red ribbon, pleated skirt, cheerleader, pom-poms, thighhighs, loafers, standing, leaning against locker, looking at viewer, smile, school hallway, afternoon, masterpiece, high score, great score, absurdres
```

---

### SDXL Base (Realistic / Photorealistic)

**Format:** Natural language with photography terminology. Full descriptive sentences.

**Structure:**
```
[Persona]: Age, Gender, Facial Features, Hair & Eyes, Expression, Pose
[Clothing]: Type, Material, Fit, Color, Accessories, Footwear
[Scene & Mood]: Environment, Lighting, Photography Style, Camera Settings
```

**Key vocabulary:**
- Camera: "Shot on Canon EOS 5D Mark IV, 85mm lens", "Sony A7 III, 50mm f/1.8"
- DOF: "Shallow depth of field (f/1.4), creamy bokeh"
- Lighting: "Golden hour", "studio softbox", "overcast diffused", "low-key dramatic"
- Composition: "Close-up portrait", "medium shot", "full body", "dutch angle"

**Negative prompt:**
```
cartoon, illustration, anime, painting, CGI, 3D render, unrealistic proportions, extra fingers, low quality, blurry, bad anatomy, bad hands, deformed, plastic skin, airbrushed
```

**Settings:** CFG 7, Steps 30, Sampler DPM++ 2M Karras

**Rules:**
- Photography vocabulary is #1 factor for realism
- Describe skin texture (pores, freckles, imperfections) to avoid plastic look
- Camera model + lens + aperture = instant realism boost

**Example:**
```
A 17-year-old Slavic teenage girl with high cheekbones, fair skin, light blue eyes, and long blonde hair tied in a high ponytail, wearing a crisp white button-up shirt with a red ribbon tie, a short pleated navy blue miniskirt, white thigh-high socks, and polished leather loafers, holding cheerleading pom-poms and leaning casually against metal lockers in a bright school hallway, looking at the camera with a confident playful smile, warm afternoon sunlight streaming through windows, shot on Canon EOS 5D Mark IV, 85mm lens at f/1.8, shallow depth of field with creamy bokeh background
```

---

### Z-Image Turbo

**Format:** Full natural English sentences ONLY. NO tag soup. NO comma-separated lists.

**Critical rules:**
1. Write in complete natural English sentences
2. Subject goes FIRST in the prompt
3. NO negative prompts (CFG=0, negatives ignored entirely)
4. Include specific photography equipment vocabulary for realism
5. Describe facial asymmetries and skin texture to avoid plastic look
6. ~512 token effective attention cap

**Photography vocabulary:**
- Candid: "Shot on a point-and-shoot film camera", "Handheld iPhone snapshot with slight motion blur", "Disposable camera aesthetic, slight overexposure"
- Cinematic: "Shot on Fujifilm GFX100 II medium format camera, 110mm f/2 lens, shallow depth of field", "Medium-format Hasselblad"
- Studio: "Studio lighting with softbox key light, fill light, rim light"

**Settings:** CFG 0, Steps 8, Sampler Default (distilled)

**Rules:**
- Model defaults to "beauty stock photography" — actively counteract with specific vocab
- "Realistic", "average", "normal" do almost nothing alone — pair with equipment references
- Text rendering is a strength — put text at VERY START

**Example:**
```
A teenage Slavic cheerleader with high cheekbones, fair skin dotted with light freckles, pale blue eyes, and long blonde hair tied in a slightly messy high ponytail stands in a bright school hallway, wearing a crisp white button-up shirt with a red ribbon loosely tied at the collar, a short pleated navy blue miniskirt, white thigh-high socks with a subtle cable-knit texture, and polished brown leather loafers, holding bright cheerleading pom-poms in her right hand and leaning casually against a row of blue metal lockers with a confident playful smile, warm afternoon sunlight streaming through tall windows casting long diagonal shadows across the linoleum floor, shot on a point-and-shoot film camera with slight overexposure giving a candid yearbook-photo aesthetic
```

---

### Base SD / SD 1.5

**Format:** Hybrid — natural language description with quality tags appended at the end.

**Structure:**
```
[Natural language description of subject, clothing, pose, environment, lighting], masterpiece, best quality, highres
```

**Quality tags (always at end):** `masterpiece, best quality, highres`

**Negative prompt:**
```
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digits, cropped, worst quality, low quality, blurry, ugly, deformed
```
Add for realistic: `cartoon, illustration, anime, painting, CGI, 3D render, plastic, airbrushed`
Add for anime: `realistic, photograph, photorealistic, live action`

**Settings:** CFG 7-9, Steps 25-30, Sampler Euler a or DPM++ 2M Karras

**Rules:**
- 75 token limit per CLIP chunk — use weighting/splitting for long prompts
- Hands are the weakest point — avoid complex hand positions
- Different fine-tunes expect different styles — adapt based on model name

**Example:**
```
A teenage Slavic girl with high cheekbones, fair skin, blue eyes, and long blonde hair in a ponytail, wearing a white button-up shirt with a red ribbon, a short pleated miniskirt, thigh-high socks, and loafers, holding cheerleading pom-poms, standing in a school hallway leaning against lockers, looking at camera with a confident smile, afternoon sunlight, masterpiece, best quality, highres
```

---

### Automated Prompt Generation (Workflow Integration)

For fully automated workflows where user input → prompt → image:

1. Take raw user input (vague description)
2. Apply the appropriate model's prompt structure above
3. Expand vague terms with specific details (hair, eyes, clothing, pose, lighting)
4. Append correct quality tags for the model
5. Output ONLY the raw prompt text — no markdown, no labels, no settings
6. Feed directly into the generation pipeline

**Key principle:** The system prompt for the LLM handling this should output ONLY the finalized prompt. No greetings, no explanations, no code fences, no model name, no settings, no negative prompt. Just the raw prompt text.

## Lessons Learned

#### Full Pipelin
```
CheckpointLoader(43) → LoRA stack(47,80) → Resolution(17) → KSampler(7, 12 steps LCM) →
  UltimateSDUpscale(88, 2x, 4x-UltraSharp) →
  FaceDetailer NIP(97) → FaceDetailer V(98) → FaceDetailer P(101) →
  FaceDetailer face(104, 1024px, 6 steps) → FaceDetailer hands(105, 2048px, 6 steps) →
  SeedVR2VideoUpscaler(114, 2048px final) → CRT Post-Process(115) → SaveImage(200)
```

#### Active LoRAs (node 80)
| LoRA | Strength | Purpose |
|------|----------|--------|
| AddMicroDetails v6 | 0.2 | Skin texture, fine details |
| PersonEnhanceV2 ILL | 0.1 | Better anatomy/face |
| TrendCraft Style Detailer v2.4I | 0.1 | Overall polish/detail |

#### Active LoRAs (node 47)
| LoRA | Strength | Purpose |
|------|----------|--------|
| DTLVVTT DMD2 V5-LITE | 1.0 | DMD2 distillation (faster/better LCM) |

#### FaceDetailer Pipeline
Sequential detailers with YOLO detectors:
1. **NIP** (`nipples_yolov8s-seg.pt`) — nipple detection, 1024px, denoise 0.4
2. **V** (`nsfw-seg-vagina-x.pt`) — vagina detection, 1024px, denoise 0.4
3. **P** (`nsfw-seg-penis-x.pt`) — penis detection, 1024px, denoise 0.4
4. **Face** (`Anzhc Face seg 768MS v2 y8n.pt`) — face detection, 1024px, 6 steps, denoise 0.4
5. **Hands** (`PitHandDetailer-v2-Test-v9c.pt`) — hand detection, **2048px**, 6 steps, denoise 0.5

#### SeedVR2 Upscaler (node 114)
- Model: `seedvr2_ema_7b_sharp-Q4_K_M.gguf` (quantized 7B)
- VAE: `ema_vae_fp16.safetensors`
- Final resolution: 2048
- Color correction: lab

#### CRT Post-Process (node 115)
- Vibrance: +0.015 (subtle saturation boost)
- Vignette: 0.5 strength, 0.7 radius, 2.0 softness

### Danbooru Tag Prompting (LUSTIFY)

**CRITICAL:** LUSTIFY is Illustrious-based — use Danbooru-format tags, NOT natural language descriptions.

#### Quality/Priority Tags (always include)
```
masterpiece, best quality, amazing quality, very aesthetic, absurdres
```

#### Subject Tags
```
1girl, solo, cute, petite, pale skin, medium breasts
```

#### Clothing/Accessories
```
gym uniform, white shirt, sports shorts, sneakers, ponytail
```

#### Action/Pose (keep it SIMPLE — complex actions confuse the model)
```
jumping, dynamic pose, looking at viewer
```

#### Setting/Light
```
gym background, afternoon light, dutch angle, from below
```

#### Negative Prompt (always)
```
blurry, worst quality, bad quality, error, melted body, bad anatomy, bad hands, disfigured
```

#### What Works
- **Character portraits work best** — this is a hentai/character model
- **Simple dynamic poses** (jumping, running, leaning) — YES
- **Quality tags first** — `masterpiece, best quality` are weighted
- **POV/camera tags** — `dutch angle`, `from below`, `from above`, `close-up`
- **Lighting tags** — `sunlight`, `god rays`, `afternoon light`, `backlight`
- **Keep tags under ~25** — more dilutes quality

#### What Fails
- **Natural language descriptions** — "mid-jump over a vaulting horse" → model doesn't understand
- **Complex multi-object composition** — "vaulting horse + girl midair" = garbled anatomy
- **"photorealistic" tag** — fights the anime/illustrious base, produces uncanny results
- **Overloaded action tags** — "jumping + spread legs + leaning forward + vaulting horse" = nightmare
- **Multiple characters** — this workflow is tuned for `1girl, solo`

### Image Generation Parameters

```json
{
  "workflow": "acestep-aio",
  "prompt": "masterpiece, best quality, 1girl, cute, ...",
  "aspect_ratio": "7:9 (Portrait)",
  "seed": -1
}
```

Valid aspect ratios:
- `1:1 (Square)`
- `4:5 (Portrait)`
- `7:9 (Portrait)` ← default, best for single character
- `3:2 (Landscape)`
- `16:9 (Landscape)`
- `9:16 (Portrait)`

Additional optional params: `megapixels` (default 1.5), `steps`, `cfg`, `denoise`, `sampler_name`, `scheduler`

### Adding a New Workflow (any modality)

1. Export workflow JSON from ComfyUI → save to `workflows/<name>.json`
2. Add entry to WORKFLOW_INFO in server.js:
   ```js
   '<name>': { file: '<name>.json', type: 'audio'|'image'|'video', ext: 'mp3'|'png'|'mp4',
               promptNode: '94', promptField: 'tags', lyricsNode: '252', lyricsField: 'String',
               outputNode: '104' }
   ```
3. Restart: `pm2 restart genor-comfy-gate`
4. Test, then document in this SKILL.md

The gateway auto-handles: prompt injection, duration, BPM/keyscale (audio), aspect_ratio (image),
seed, polling, download from correct server, save to media dir, metadata sidecar.

## Auto-build & Run Scripts

**MUST USE** — these scripts handle the full lifecycle: install, build, run, update, restart.

### One-Command Install
```bash
cd ~/.openclaw/workspace/projects/Genor-Comfy-Gate
bash install.sh
```
Does everything: `npm install` → create media dirs → create workspace → PM2 start/save.

### One-Command Auto-build & Restart
```bash
cd ~/.openclaw/workspace/projects/Genor-Comfy-Gate
bash autobuild.sh
```
Full update cycle: `git pull` → `npm install` → `pm2 restart genor-comfy-gate`.
Use this after pulling changes, updating workflows, or modifying server code.

### Manual Commands

| Action | Command |
|--------|---------|
| Install deps | `npm install` |
| Create dirs | `mkdir -p ~/media/comfy/audio ~/media/comfy/images` |
| Create workspace | `mkdir -p ~/projects/genor-comfyui/{workflows,custom_instructions/prompt_templates,generations/{images,audio},exports}` |
| Start (PM2) | `pm2 start server.js --name genor-comfy-gate -- --port 8188` |
| Start (PM2 ecosystem) | `pm2 start pm2-ecosystem.config.cjs` |
| Dev mode (hot-reload) | `npm run dev` |
| Direct run | `node server.js --port 8188` |
| Restart | `pm2 restart genor-comfy-gate` |
| Stop | `pm2 stop genor-comfy-gate` |
| Logs | `pm2 logs genor-comfy-gate` |
| Status | `pm2 list \| grep genor-comfy-gate` |
| Health check | `curl -s http://127.0.0.1:8188/ \| python3 -m json.tool` |

### First-Time Setup Flow
```bash
cd ~/.openclaw/workspace/projects/Genor-Comfy-Gate

# 1. Install everything
bash install.sh

# 2. Verify it's running
curl -s http://127.0.0.1:8188/ | python3 -m json.tool

# 3. Check logs
pm2 logs genor-comfy-gate --lines 20
```

### Update Flow (after code changes)
```bash
cd ~/.openclaw/workspace/projects/Genor-Comfy-Gate
bash autobuild.sh
```

## Lessons Learned

### 2026-05-19 — Image Generation
- **LUSTIFY is Illustrious-based, uses Danbooru tags** — natural language prompts produce garbled results
- Quality tags (`masterpiece, best quality`) must come FIRST — they're weighted
- Complex action scenes fail — model is trained for character portraits, keep poses simple
- "photorealistic" tag on anime model = uncanny valley, avoid
- Keep prompts under 25 tags — overloading dilutes quality
- Pipeline has SeedVR2 upscaler (7B GGUF) + 5-stage FaceDetailer → 2048px final output
- Face/hand detailers produce excellent close-up quality

### 2026-05-19 — Audio Generation
- **Download 400 bug:** `getOutputInfo()` function returned undefined filenames despite reading them from history correctly. Fixed by inlining output scanning in the handler.
- **Load balancer:** PRIMARY-first when idle, ALL→SECONDARY when PRIMARY busy (not round-robin).
- **Workflow cleanup:** Removed duplicate nodes 401, 402. Lyrics now go through node 252 (String) → node 94.
- **Caption quality:** `raw`, `gritty`, `heavy drops` cause metallic scraping and flat bass. Use `warm`, `crisp`, `punchy`, `polished` for clean instruments.
- **5-8 tags sweet spot** for SFT merge model. More degrades quality.
- **8 dimensions matter:** Missing emotion/timbre = flat results. Cover: genre, emotion, instruments, timbre, vocal, production, era, rhythm.
