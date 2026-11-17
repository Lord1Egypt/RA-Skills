<div align="center">

# 🎬 Gent Skill

### Professional cinematic visual studio for images, video intros, and designed overlays.  
### Use for image generation, prompt crafting, Figma visual design, ffmpeg video production, and voiceover assembly.  
### Upgrade your agent to do everything for free — Image generation, editing, writing, video production, and more.

[![Skill](https://img.shields.io/badge/skill-gent--skill-purple)](https://clawhub.ai/hleliofficiel/gent-skill)
[![ClawHub](https://img.shields.io/badge/ClawHub-published-22c55e)](https://clawhub.ai/hleliofficiel/gent-skill)
[![GitHub](https://img.shields.io/badge/GitHub-hleliofficiel/gent--skill-black)](https://github.com/hleliofficiel/gent-skill)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

<br/>

<img src="https://github.com/hleliofficiel/gent-skill/blob/main/istanbul-cinematic.jpg" width="60%" alt="Cinematic Istanbul"/>

<br/>

<a href="https://clawhub.ai/hleliofficiel/gent-skill"><b>View on ClawHub →</b></a> · <a href="https://clawskills.sh"><b>Browse Skills →</b></a>

</div>

---

## ✨ Why Gent Skill?

Gent Skill is the modern toolkit to **supercharge OpenClaw** with pro-grade cinematic visuals, free image generation, and smart video production.

Unlike single-purpose plugins, Gent Skill integrates **all 4 powerful domains** into one unified, autonomous workflow:

* **🎨 Image Generation** — photorealistic cinematic portraits & scenes via gen1.diversityfaces.org
* **🎥 Video Production** — AI-powered video creation with voiceover, transitions, and filmic assembly
* **🖌️ Design & Overlays** — Figma-grade overlays, typography, branding, and intro motion
* **✂️ Editing Pipeline** — ffmpeg compression, scaling, zoom, xfade, drawtext, and 16:9 cinematic formatting

**Everything runs through one provider, one pipeline, and delivers attachments that actually work.**

**SEO Keywords:** AI image generation, cinematic video intro, AI portrait generator, AI video maker, free AI art, JPEG output, Figma design automation, ffmpeg video editing, OpenClaw skill, ClawHub skill, diverse faces, professional headshots, cinematic Istanbul, payfopus intro, gentle skill

---

## 🚀 Quick Installation

### 1. Install Gent Skill

```bash
# via OpenClaw
openclaw skills install gent-skill

# or manually:
cp -r ./gent-skill ~/.openclaw/workspace/skills/
```

### 2. Get your FREE API Key (60 seconds)

1. Visit: https://gen1.diversityfaces.org/api-key-request
2. Enter username, email, country
3. Get your key instantly

### 3. Configure

```bash
export BEAUTY_API_KEY="your_api_key_here"
```

That's it. Everything is autonomous after that.

---

## 💡 Features

### 🎞️ Image Generation
- Photorealistic cinematic images
- 16:9 cinematic compositions
- Ultra-detailed, HDR, film-noir moods
- **Mandatory JPEG output** (works in Telegram & ClawHub)

### 🎬 Video Intros
- 12-second cinematic intros with zoompan + xfade
- Branding text overlays (drawtext)
- 1280×720 baseline, 30fps
- PayFopus intro ready

### 🎙️ Voiceover
- Assembly via `ai-video-gen/add_voiceover.py`
- TTS-ready, multi-scene

### 🖌️ Figma Design
- Visual audit, typography, brand identity
- Intro overlays, skewed layers, motion logos

### ✂️ FFmpeg Production
- Trim/compress/merge
- Resolution scaling FHD→720p
- Subtitle burn, watermark, audio extract

---

## 🔧 How it Works

```
User prompt
  → Intent classification (image | video | design | edit)
  → beauty-generation-api via gen1.diversityfaces.org → JPEG
  → (optional) Figma overlay design
  → ai-video-gen + ffmpeg-video-editor assembly
  → real attachment via message tool (Telegram)
  → confirm ok:true + messageId
```

**Delivery:** Every image/video is sent as a real file attachment, not markdown-only.  
**Guaranteed:** JPEG for images, MP4 for videos.

---

## 📁 Project Structure

```
gent-skill/
├── SKILL.md
├── PROMPT.md
├── QUICK_START.md
├── RATIONALE.md
├── config.json
├── skill-card.md
├── clawhub.yaml
├── scripts/README.md
└── LICENSE
```

---

## 🧪 Verified Examples

### 1. Istanbul Night Cinematic
![Istanbul](istanbul-cinematic.jpg)  
Prompt: *Lone person, rain-slicked cobblestone, city reflections, mosque silhouette* — delivered as JPEG attachment (messageId confirmed).

### 2. Bosphorus Tower
![Bosphorus](bosphorus-tower-cinematic.jpg)  
Cinematic tower above Bosphorus, golden hour — JPEG delivered.

### 3. PayFopus Intro Video
![Intro](payfopus-intro.mp4)  
12s, 1280×720, 30fps, instant attachment.

---

## 🛡️ Safety & Limits

- API key secret guarded
- Quota check before bulk runs
- Fail loudly with reason — never silent

---

## 🧑‍💻 Contributing

Issues & PRs welcome. Extend providers with custom plugins — the Gent Skill architecture is modular.

---

## ⭐ Support

- Star this repo
- Follow [@hleliofficiel](https://github.com/hleliofficiel)
- ClawHub: https://clawhub.ai/hleliofficiel/gent-skill

---

## 📜 License

Apache-2.0 — see [LICENSE](LICENSE)

---

<div align="center">

### Built with 💜 for OpenClaw

</div>
