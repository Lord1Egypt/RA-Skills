---
name: claw3d
description: "Unified 3D workflow: create models (AI), search (Thingiverse), slice, print. Modular—enable only what you need."
metadata:
  {
    "openclaw": {
      "emoji": "🖨️",
      "skillKey": "claw3d",
      "primaryEnv": "FAL_API_KEY",
      "requires": {{REQUIRES_JSON}},
      "homepage": "https://github.com/makermate/openclaw-3d",
      "install": [
        {
          "id": "uv",
          "kind": "uv",
          "package": "claw3d",
          "bins": ["claw3d"],
          "label": "Install claw3d (via uv)"
        }
      ],
      "setupNote": "FAL_API_KEY: required for 3D generation (use input above or .env). GEMINI_API_KEY: optional but recommended — enables image intent analysis and video-to-3D (Gemini 2.5 Flash, free tier at aistudio.google.com/apikey). THINGIVERSE_ACCESS_TOKEN: add to .env for model search. VIDEO SUPPORT: OpenClaw defaults to a 5MB media limit per channel. To allow videos up to 50MB via Telegram, add to openclaw.json under channels.telegram: {\"mediaMaxMb\":50}"
    }
  }
---
