---
name: ai-video-studio
version: 1.0.1
description: FableForge AI Agent SOP — A command-level executable playbook for producing high-quality management allegory videos. Covers the full pipeline from concept generation, story writing, TTS voice synthesis, to HyperFrames video rendering, including visual style guidelines and technical pitfall reference.
---

# 🔨 FableForge · AI Agent SOP (English)

This Skill is a **command-level executable SOP**, not a lessons-learned doc. Every Stage contains **exact commands** and **exit criteria**. Skipping steps or advancing before criteria are met is strictly prohibited.

---

## 0. Script Specification Standards (Hard Constraints)

Before any production begins, understand and enforce these non-negotiable specs. **Any script that deviates must be sent back for rewriting — it may not enter production.**

| Spec | Standard | Notes |
|------|----------|-------|
| Total duration | 60 ~ 120 seconds | Short-form: 60s recommended; deep insights can extend to 120s |
| Scene count | 8 ~ 12 scenes | Too few = loose pacing; too many = choppy cuts |
| Words per scene narration | ZH: 30~60 chars / EN: 20~40 words | ZH ~3.5 chars/sec, EN ~2.5 words/sec |
| Scene duration estimate | 5 ~ 12 seconds | Final values come from audio measurement only |
| Scene ID format | `scene1` ~ `scene{N}` | Must match `assets/scene{N}.png` exactly |
| Narration-scene mapping | 1 scene == 1 image == 1 narration block | Strictly 1:1:1 |

---

## 0.5 Quality Gates (Three Content Checkpoints)

Video quality is capped by three factors. **Each gate must be passed before advancing. Technical polish cannot cover for weak content.**

### Gate 1: Story Review (after concept generation, before presenting to user)

AI tends to produce "structurally correct but intellectually shallow" stories. Complete this self-check before showing the allegory to the user:

**Topic Selection Standard (embed in generation prompt):**
> The chosen management concept must simultaneously satisfy: **sounds counter-intuitive, makes people uncomfortable when stated plainly, is universally experienced at work but rarely named.** Concepts like "hard work pays off" do not qualify.

**Mandatory Self-Check (all must pass before submitting for user confirmation):**
- [ ] **Counter-intuition test**: Is this insight "everyone already knows this" or "everyone has lived this but never had words for it"? Former has no virality — rewrite.
- [ ] **Suspense test**: Can a viewer guess the ending by second 10? If yes, the metaphor is too obvious — add a reversal, rewrite.
- [ ] **Discomfort test**: Does the ending create mild discomfort or an "aha" that stings? No discomfort = no depth — rewrite.
- [ ] **Reality anchoring test**: Does the ending explanation map to a **specific workplace scenario the viewer could face today**?

---

### Gate 2: Script Rhythm Review (after storyboard conversion)

A script is an emotional score. The full film must have a pacing arc — a flat "same emotional gear throughout" is prohibited.

**Emotional Gear Definitions:**

| Gear | Name | Word Count | Typical Placement |
|------|------|-----------|------------------|
| 1 | Slow Narration | 40–60 words | Opening — establish the world |
| 2 | Building Tension | 30–50 words | Conflict development |
| 3 | Peak Intensity | 20–40 words | The critical turning point |
| 4 | Silence & Space | ≤ 15 words | The pause before the conclusion lands |

**Mandatory Pacing Arc (60-second standard template):**
```
Opening:    1 → 1 → 2   (smooth entry, slight warmup)
Rising:     2 → 2 → 3   (escalating conflict)
Climax:     3 → 3 → 4   (peak moment, then sudden stillness)
Resolution: 4 → 1       (after the pause, fewest words, biggest landing)
```

**Script Writing Rules:**
- **Write feelings, not actions.** Narration describes emotional states, not visual actions:
  - ❌ `"Ten wolves lined up in the valley, awaiting the Wolf King's command."`
  - ✅ `"Silence in the valley. Only wind, and the held breath of those waiting."`
- **Halve the word count for the resolution scene.** The most important insight needs the fewest words. Final scene narration: ≤ 20 words.
- **Tag every scene with its gear**: Add `- **Emotional Gear**: {1/2/3/4}` to the storyboard — this drives both image prompts and vocal tone.

---

### Gate 3: Image Quality Review (after image generation, before Stage 2)

**Composition & Aspect Ratio Rules (Mandatory):**
- **Fixed Aspect Ratio**: Must generate **16:9 landscape** images (DALL-E 3: `1792x1024`). Square images are prohibited for production.
- **Subject Position**: Subject must be positioned in the **upper third** of the frame — the bottom is the subtitle safe zone.
- **Mandatory Keywords**: `cinematic wide shot, 16:9 aspect ratio, subject positioned in upper third of frame, dark atmospheric space at bottom`
- **Coherence**: Unify the primary light direction across all scenes.

**Style Locking Workflow:**
```
1. Generate scene1 normally → once satisfied, extract its core prompt as the "style prefix"
2. For scene2 ~ scene{N}: prepend the style prefix to every prompt
   Format: "[scene1 core style], [lighting desc], same art style, —"
```

**Character Consistency (required for scripts with recurring characters):**
```
1. Before any scene images, generate a "Character Bible" reference image (front-facing full body, no background)
2. Document the character's visual traits (fur color, build, eyes, signature features)
3. Every subsequent scene image containing this character must include these trait keywords
```

**Image Self-Check (all must pass before entering Stage 2):**
- [ ] Subject sits in the upper third; bottom has sufficient dark space for subtitle overlay
- [ ] Image mood matches the scene's emotional gear (Gear 3 images cannot look peaceful)
- [ ] All scenes share consistent lighting and color palette
- [ ] No obvious AI artifacts (extra fingers, garbled text, distorted proportions)

---

## Stage 1: Concept, Script & Asset Generation

### 1.1 Concept Generation (pause & wait for user confirmation)

Use the following prompt template to generate the allegory:

> *"From the domain of [management / leadership / organizational behavior], select a PhD-level concept. Write a fable that illustrates the concept indirectly. Don't reveal the answer at the start — let the insight dawn on the reader near the end. After the story, explain the concept and what each story element represents as a metaphor."*

**Deduplication check**: Before generating, scan all `YYYYMMDD/script-template.md` files in the workspace to ensure the theme does not repeat a previous work.

⛔ **After this step: STOP. Present the full allegory to the user and await explicit confirmation. Do not continue without confirmation.**

### 1.2 Storyboard Conversion (after user confirmation)

Break the story down into a scene-by-scene storyboard using the spec standards, write to `YYYYMMDD/script-template.md`.

Storyboard format:
```markdown
## Scene {N} — {Scene Name}
- **Time (draft estimate)**: {X} ~ {Y} seconds
- **Emotional Gear**: {1 / 2 / 3 / 4}
- **Narration**: {ZH 30-60 chars / EN 20-40 words}
- **Visual Description**: {Image generation prompt}
```

### 1.3 TTS Voice Generation

**Voice Selection (Priority Awareness):**
- **Default Principle**: Always check the `/语音模型/voxenv` environment first. If it exists, **MUST** use the user's voice clone for narration.
- **Fallback**: Only use Kokoro or other generic models if explicitly requested or if the clone environment is unavailable.

**Voice pacing optimization:**

VoxCPM2's emotional output is relatively flat — inject dramatic texture at the text level:
- Insert `…` before key nouns/verbs to slow the model down and add weight
- Use `|||` to manually segment paragraphs at natural dramatic breaks (when > 130 characters)
- For Gear 4 (silence/space) scenes, add `…` between every phrase

```
❌ Flat delivery:
"You thought you selected warriors. You only selected the best at killing teammates."

✅ With dramatic pauses:
"You thought… you selected warriors. ||| In truth, you only selected — the most efficient killers… of teammates."
```

Run in the project directory:

```bash
# Use VoxCPM2 with the virtual environment Python (one script per project)
cp /Users/lucas/Work/09.Antigravity/语音模型/generate_cantillon.py \
   /Users/lucas/Work/09.Antigravity/语音模型/generate_{project_name}.py
# Edit TARGET_TEXT, OUTPUT_FILE variables
/Users/lucas/Work/09.Antigravity/语音模型/voxenv/bin/python3 \
  /Users/lucas/Work/09.Antigravity/语音模型/generate_{project_name}.py
```

### 1.4 Image Asset Generation

Generate one image per scene using the "Visual Description" prompt from the storyboard. Naming must strictly follow `scene1.png`, `scene2.png` ... `scene{N}.png`, saved to `YYYYMMDD/assets/`.

**✅ Stage 1 Exit Criteria (all must be met before entering Stage 2):**
```bash
ls YYYYMMDD/assets/ | grep -E "^scene[0-9]+\.png$" | wc -l  # must equal scene count
ls YYYYMMDD/assets/narration.wav                              # must exist
```
- [ ] Image count in `assets/` == storyboard scene count
- [ ] `assets/narration.wav` exists
- [ ] Image filenames are sequential (no gaps, e.g., scene1–scene10 cannot skip scene7)

### 1.5 BGM (Background Music) Matching

BGM is the emotional engine and must be selected before entering Stage 2.

**BGM Workflow:**
1. **Mood Tagging**: Analyze the "Emotional Gear" of each scene to extract core keywords (e.g., Suspense, Epic, Minimalist, Melancholic).
2. **Library Search**: Search royalty-free libraries (Scott Buckley, Pixabay, Bensound) and download 1 global background track.
3. **Configuration**:
   - `data-track-index`: Set to `-1` (always the bottom layer).
   - `data-volume`: Default `0.15` to `0.25` (adjust via preview; must not drown narration).
4. **Integration into index.html**:
   ```html
   <audio id="bgm" src="assets/bgm.mp3" data-start="0" data-duration="{total duration}" data-track-index="-1" data-volume="0.25"></audio>
   ```

**✅ Stage 1.5 Exit Criteria:**
- [ ] `assets/bgm.mp3` is in place.
- [ ] `script-template.md` (or `视频脚本.md`) includes BGM attribution (author, link, and CC license).

---

## Stage 2: Audio Analysis & Data-Driven Timeline

### 2.1 Get precise audio duration

```bash
export PATH=./bin:$PATH
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1 YYYYMMDD/assets/narration.wav
# Record the output duration=XX.XXXXXX — this is the authoritative total video length
```

### 2.2 Get precise scene timestamps (choose one)

**Option A — Whisper transcription (recommended, highest accuracy):**
```bash
npx hyperframes transcribe YYYYMMDD/assets/narration.wav
# Generates YYYYMMDD/assets/transcript.json with word-level timestamps
```

**Option B — Silence detection (for audio with clear pauses):**
```bash
export PATH=./bin:$PATH
ffmpeg -i YYYYMMDD/assets/narration.wav -af silencedetect=noise=-30dB:duration=0.3 -f null - 2>&1 | grep silence
# Record each silence_end timestamp as the scene transition point
```

### 2.3 Map timestamps to scenes

From the 2.2 output, derive a JS data array — **no manual estimation allowed:**

```js
const scenes = [
  { id: "scene1", start: 0,    duration: 5.8,  subtitle: "Narration text..." },
  { id: "scene2", start: 5.8,  duration: 6.2,  subtitle: "Narration text..." },
  // ...
];
```

**✅ Stage 2 Exit Criteria:**
- [ ] `transcript.json` generated OR `silencedetect` output recorded
- [ ] Sum of all `start + duration` values deviates from audio total by < 0.2 seconds
- [ ] Every `data-start` value is machine-derived — zero estimated values

---

## Stage 3: Static Layout Build & Validation

### 3.1 HTML Base Template (mandatory spec)

```html
<!-- Root container: all three data-* attributes are required -->
<div id="composition"
     data-composition-id="composition"
     data-width="1920"
     data-height="1080">

  <!-- Audio track -->
  <audio id="narration"
         src="assets/narration.wav"
         data-start="0"
         data-duration="{total duration from Stage 2.1}"
         data-track-index="0">
  </audio>

  <!-- Scenes are injected by JS — never hard-code scene HTML -->
  <div id="scenes-container"></div>
</div>

<script>
  // GSAP timeline must always be paused: true — never change this
  const tl = gsap.timeline({ paused: true });

  // Register early so timeline survives any downstream JS error
  window.__timelines = window.__timelines || {};
  window.__timelines["composition"] = tl;

  const scenes = [/* Stage 2.3 data array */];
  const container = document.getElementById("scenes-container");

  scenes.forEach(({ id, start, duration, subtitle }) => {
    const scene = document.createElement("div");
    scene.id = id;
    scene.className = "clip";
    scene.dataset.start = start;
    scene.dataset.duration = duration;
    scene.dataset.trackIndex = "1";

    const bgImg = document.createElement("img");
    bgImg.className = "bg-fill";
    bgImg.src = `assets/${id}.png`;

    const fgImg = document.createElement("img");
    fgImg.className = "fg-main";
    fgImg.src = `assets/${id}.png`;

    const overlay = document.createElement("div");
    overlay.className = "overlay";
    const sub = document.createElement("div");
    sub.className = "subtitle";
    sub.textContent = subtitle; // textContent auto-escapes — eliminates < > injection bugs
    overlay.appendChild(sub);

    scene.appendChild(bgImg);
    scene.appendChild(fgImg);
    scene.appendChild(overlay);
    container.appendChild(scene);

    tl.fromTo(fgImg,
      { scale: 1.0, transformOrigin: "center center" },
      { scale: 1.06, duration: duration, ease: "none" },
      start
    );
  });
</script>
```

### 3.2 CSS Layout Rules (mandatory)

```css
/* Container: 16:9 ratio */
#composition { background: #000; overflow: hidden; }

/* 1. Background layer: Blurred (for hierarchy or non-16:9 assets) */
.bg-blur {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: cover;
  filter: blur(40px) brightness(0.4);
  z-index: 1;
}

/* 2. Foreground layer: Main subject */
.fg-main {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  object-fit: contain; /* ensures no cropping */
  z-index: 2;
  transform-origin: center center;
}

/* 3. Subtitle layer */
.subtitle {
  position: relative;
  z-index: 10;
}
```

**✅ Stage 3 Exit Criteria:**
- [ ] All images display fully (no cropping, no offset) in pure static view
- [ ] `data-composition-id`, `data-width`, `data-height` are correctly set
- [ ] Subtitles injected via `textContent` — no hard-coded HTML subtitle strings

---

## Stage 4: Animation, Pre-flight & Render

### 4.1 GSAP Animation (only after Stage 3 passes)

Ken Burns zoom is already wired in the Stage 3 template. If you need custom per-scene easing, add it here.

### 4.2 Mandatory Pre-flight (last defense before rendering)

```bash
export PATH=./bin:$PATH
npx hyperframes@latest inspect YYYYMMDD/
```

**✅ Stage 4 Exit Criteria (all must be met — no exceptions):**
- [ ] `inspect` exits with code 0 (zero errors)
- [ ] Console-printed `totalDuration` matches Stage 2.1 audio length (deviation < 0.2s)
- [ ] Zero `StaticGuard` warnings

### 4.3 Render

```bash
export PATH=./bin:$PATH
# Force use of promo_video.mp4 for automatic GitHub sync (exempted in .gitignore)
npx hyperframes@latest render YYYYMMDD/ -o YYYYMMDD/promo_video.mp4 --force-new
```

---

## Stage 5: Publishing & Archiving

### 5.1 Script Metadata

Update `视频脚本.md` / `script-template.md` with:

```markdown
## Technical Details
- **Voice**: VoxCPM2 user clone / Kokoro am_adam
- **Measured Duration**: {ffprobe value}s
- **BGM**: {track name} by {author} (CC BY 4.0)
- **YouTube**: {URL}
```

### 5.2 README Update

Add a new row to the Demo Works table in `README.md` (both English and Chinese sections).

### 5.3 Git Sync

```bash
git add YYYYMMDD/ README.md
git commit -m "feat: Add {video_title} project"
git push origin main
```

**✅ Stage 5 Exit Criteria:**
- [ ] Script file contains full metadata (voice, duration, BGM, YouTube link)
- [ ] `README.md` demo works table updated (both EN and ZH)
- [ ] `git push` successful

---

## Appendix A: Visual Style Guide

### Style Decision Principles
- **Adaptive**: Visual style must serve the story. Options: ink painting, modern minimalist, steampunk, cyberpunk, cinematic realism.
- **Coherence**: All images in a single film must share the same color palette, lighting, and visual language.

### Image Prompt Engineering
- **Lead with style**: Define art direction first (`Cinematic realistic style` / `Oriental brush painting` / `Minimalist vector art`)
- **Quality suffix**: Append to every prompt: `hyper-realistic details, cinematic lighting, masterpiece, 8K, subject in upper third, dark space at bottom`
- **Text/diagram images**: `A [style] visualization with labels. Main node: "Core concept". Sub-nodes: "Term 1", "Term 2". Professional design, glowing connections.`

---

## Appendix B: Known Technical Pitfalls

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Image cropped / shifted | GSAP matrix overwrites `translate` centering | Use `object-fit: contain` — never `translate` |
| Square image top cropped | `object-fit: cover` clips subject | Force 16:9 generation, or use `contain` + blurred bg |
| Video ends early / missing last scene | Unescaped `<` or `>` in subtitle breaks DOM | Use `textContent` injection |
| `inspect` reports `totalDuration undefined` | Root container missing `data-duration` | Add `data-duration="{audio total}"` |
| `inspect` crashes / MP4 has random duration | Violated render contract | Timeline always `paused: true`, never `play()` |
| Color shift on screen | `img` tag has `filter: hue-rotate(...)` | Remove the filter |
| `FFmpeg not found` | Environment not configured | `export PATH=./bin:$PATH` |

---

## Appendix C: Environment Setup (one-time)

```bash
# FFmpeg static binaries (macOS)
curl -L https://evermeet.cx/ffmpeg/get/zip -o ffmpeg.zip && unzip ffmpeg.zip
curl -L https://evermeet.cx/ffmpeg/get/ffprobe/zip -o ffprobe.zip && unzip ffprobe.zip
mkdir -p bin && mv ffmpeg bin/ && mv ffprobe bin/ && chmod +x bin/*
```

---

## Appendix D: Project Archive Structure

```text
YYYYMMDD/
  ├── index.html          (timeline composition — Stage 3/4 output)
  ├── assets/
  │   ├── scene1.png      (scene images, count == scene count)
  │   ├── scene{N}.png
  │   ├── narration.wav   (TTS audio — Stage 1.3 output)
  │   ├── bgm.mp3         (background music — Stage 1.5 output)
  │   └── transcript.json (Whisper timestamps — Stage 2.2 output)
  ├── script-template.md  (English storyboard — Stage 1.2 output)
  └── promo_video.mp4     (finished film — Stage 4.3 output, Git exemption list)
```
