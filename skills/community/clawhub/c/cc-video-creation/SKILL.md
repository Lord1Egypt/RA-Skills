---
name: "cc-video-creation"
description: "CC can create professional FactSage videos itself — free, no API, without asking Jarvis. Pipeline: story → animation (Manim/Ken Burns/Kling AI) → upload."
metadata: {"clawbot":{"requires":{"python3":true},"permissions":{"exec":["python3"],"files":["projects/factsage/"],"notes":"Local video production (Manim/Ken Burns). Kling AI is a web UI (manual). No API keys, no paid calls."}}}
---

# 🎬 CC Video Creation Skill

CC can create professional FactSage videos itself — **free, no API, without asking Jarvis!**

---

## 🏗️ Pipeline (3 steps)

### Step 1: Choose a story 📜
Pick a script from `projects/factsage/scripts/` and edit as needed.

### Step 2: Choose animation type 🎨

| Type | Description | Run |
|------|-------------|-----|
| 📜 **Manim** | Gold-ink text + timelines + particles (0 kr) | `python3 produce_with_manim.py 9` |
| 🖼️ **Ken Burns** | Images zoom in/out + text overlay (0 kr) | `python3 produce_animated.py 9` |
| 🎬 **Kling AI** | Real AI video generation (free credits) | Kling AI web UI |

### Step 3: Upload 📱
Upload finished video to YouTube/TikTok manually.

---

## 🔑 Kling AI — Free AI video (animation)

The Kling AI account is created at **klingai.com** with `factsage.media@gmail.com`

1. Log in at **klingai.com** 📱
2. Click **Create** → **Text to Video**
3. Write a prompt (describe the story)
4. Choose style: Realistic / Animation
5. Click **Generate** (free credits!)
6. Download the video → assemble with voiceover

**Prompt tips:**
- House of Wisdom: "Golden age Baghdad library, scholars reading, intricate Islamic architecture, warm candlelight, animated style"
- Salahuddin: "Medieval battlefield, noble warrior on horseback, Jerusalem walls, cinematic golden hour"
- Hospitals: "Ancient hospital ward, doctors treating patients, arched doorways, Middle Eastern setting"

---

## 🛠️ Scripts (run yourself)

```bash
# Manim animation (0 kr)
cd projects/factsage
python3 produce_with_manim.py 9     # House of Wisdom
python3 produce_with_manim.py 3     # Islamic Hospitals
python3 produce_with_manim.py 7     # Salahuddin

# Ken Burns (0 kr)
python3 produce_animated.py 9

# See output
ls output/cc-09-*.mp4
```

---

## 📁 Output

All finished videos are in: `projects/factsage/output/`

| Abbreviation | Meaning |
|--------------|---------|
| `cc-09-...mp4` | CC Manim version |
| `animated-09-...mp4` | Ken Burns version |
| `manim-09-...mp4` | Manim test version |

---

## ❌ If something goes wrong

1. Check that you are in the `projects/factsage/` folder
2. Run with the `--quick` flag for faster rendering
3. Ask Jarvis — I'm here! 🧠
