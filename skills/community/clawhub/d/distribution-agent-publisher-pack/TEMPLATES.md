# TEMPLATES.md — Publish Pack Templates (Skill1 Output)

This file defines the canonical JSON structure per platform.
Your agent should conform to these shapes.

---

## 0) Pack Envelope

{
  "meta": {
    "generated_at": "ISO-8601",
    "image_count": 1,
    "theme": "string",
    "lang": "zh|en",
    "music": { ...music_hint... }
  },
  "<platform>": { ... }
}

---

## 1) music_hint (meta.music)

{
  "mood": ["tense","calm"],
  "energy": 0.57,
  "bpm_range": [97,115],
  "genres": ["ambient techno","glitch hop","lofi"],
  "instrumentation": ["sub-bass","textured pads","granular synth","tight hats","soft percussion"],
  "use_case": ["tiktok","douyin","reels"],
  "search_terms": ["ambient techno glitch hop","neural network ambient","cyber ambient glitch"],
  "caption_line_zh": "像神经在发光的低频。",
  "caption_line_en": "Low-frequency nerves, softly lit.",
  "vision": { "ok": true, "features": {}, "flags": {}, "moods": [] }
}

---

## 2) X (x)

{
  "body": "string",
  "hashtags": ["#AIGC","#AIArt","#GenAI"],
  "options": {
    "reply_settings": "everyone"
  }
}

Notes:
- body should already include line breaks; keep short.
- hashtags are separate array for downstream rendering.

---

## 3) Bluesky (bluesky)

{
  "body": "string",
  "hashtags": ["#AIGC","#AIArt","#GenAI"]
}

---

## 4) Instagram (instagram)

{
  "hook": "string",
  "body": "string",
  "hashtags": ["#AIGC","#AIArt","#GenAI","#DigitalArt","#VisualEssay","#AIArtist"],
  "music_hint": { ...music_hint... },
  "options": {
    "sync_threads": true,
    "sync_facebook": true
  }
}

---

## 5) Threads (threads)

{
  "body": "string"
}

---

## 6) Facebook (facebook)

{
  "body": "string"
}

---

## 7) TikTok (tiktok)

{
  "body": "string",
  "hashtags": ["#AIArt","#GenAI","#VisualEssay"],
  "music_hint": { ...music_hint... },
  "options": {
    "privacy": "public"
  }
}

---

## 8) Douyin (douyin)

{
  "title": "string",
  "hook": "string",
  "body": "string",
  "hashtags": ["#AIGC","#AI绘画","#抽象艺术","#情绪表达"],
  "music_hint": { ...music_hint... },
  "options": {
    "privacy": "public"
  }
}

---

## 9) Xiaohongshu (xiaohongshu)

{
  "title": "string",
  "body": "string",
  "hashtags": ["#AIGC","#AI绘画","#视觉叙事","#抽象艺术","#情绪表达","#审美日记"],
  "keywords": ["AIGC","AI绘画","视觉叙事","情绪摄影","审美日记"]
}

Notes:
- title is crucial for CTR; keep within 18–26 CN chars.
- keywords are for SEO fields in platforms / future adapters.

---

## 10) Lemon8 (lemon8)

{
  "title": "string",
  "body": "string"
}