# 🎨 ARTCLAW AI Creative Suite — OpenClaw Skill

An all-in-one AI content creation skill powered by the [ARTCLAW](https://artclaw.com/) platform. It supports AI image generation, AI video generation, PPT creation, multimodal analysis, and workflow orchestration.

---

## ✨ Features

| Capability | Description |
|------|------|
| 🖼️ AI Image Generation | Text-to-image, image-to-image, marketing visuals, product image sets |
| 🎬 AI Video Generation | Text-to-video, image-to-video |
| 🔍 Multimodal Analysis | Image understanding, video analysis, script analysis, character profile extraction |
| ⚡ Workflows | Run preset pipelines in one click (animation / comics / e-commerce detail page, etc.) |
| ✏️ Prompt Tools | Prompt optimization for logos, covers, marketing images, and carousels (free, no API key required) |

---

## 📦 Install on OpenClaw

Tell OpenClaw directly:

```text
install skill: https://github.com/ArtClaw1/artclaw-skill
```

---

## 🔑 Configure API Key

Generation features in this skill require an ARTCLAW API key.

1. Open the ARTCLAW settings page: **https://artclaw.com/#/settings**
2. In the **API Keys** section, click "Create", enter a name, and copy the generated key (it starts with `vk_`)
3. In the OpenClaw Skill configuration page, set the environment variable:

   ```
   ARTCLAW_API_KEY=vk_your_key_here
   ```

> **Note:** Prompt tool features are free to use and do not require an API key.

---

## 🚀 Quick Start

After installation and configuration, describe your creative request directly in the OpenClaw chat:

```text
Help me create a cyberpunk-style cat illustration
```

```text
Use this product image to generate an e-commerce carousel set
```

---

## 📋 Version

- **Version:** 1.1.0
- **Author:** ARTCLAW Team
- **License:** MIT
