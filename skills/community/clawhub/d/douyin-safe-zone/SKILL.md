---
name: douyin-safe-zone
description: Plan and inspect protected content areas for 9:16 Douyin video or image-post layouts, or create a transparent reference overlay. Treat included measurements as adjustable references and verify against the current publishing preview.
license: MIT-0
metadata:
  version: "1.0.0"
---

# Douyin Safe Zone

Use this skill when laying out a Douyin 9:16 video frame, image post, or 3:4 profile cover. The included measurements are **project-derived reference defaults, not official or guaranteed platform safe-area rules**. App controls, captions, devices, and playback crops can change; use the actual preview as the final check.

## Reference layouts

| Profile | Canvas | Top | Right | Bottom | Left |
|---|---:|---:|---:|---:|---:|
| 9:16 playback | 1080×1920 | 170 px | 86 px | 288 px | 86 px |
| 3:4 cover | 1080×1440 | 115 px | 86 px | 216 px | 86 px |

Adjust margins for the target content and preview. Keep the background and nonessential decoration full-bleed; place titles, subtitles, faces, logos, key numbers, and calls to action inside the chosen protected area. Leave padding inside cards. For a 3:4 cover, compose independently instead of cropping a 9:16 frame.

For a fixed screen-recording demonstration, keep its frame and explanatory text regions stable between related scenes; allow crops and focus changes inside the frame. Treat this as a design choice only when the user has selected such a template.

## Optional overlay generator

The script requires Python 3 and Pillow. It creates a transparent PNG guide that should be hidden or removed before export:

```bash
python3 scripts/create_safe_zone_overlay.py --profile douyin-playback-reference --output /tmp/douyin-guide.png
python3 scripts/create_safe_zone_overlay.py --profile douyin-cover-3x4 --output /tmp/douyin-cover-guide.png
```

Pass `--top`, `--right`, `--bottom`, or `--left` to override a reference value. Negative or impossible margins are rejected. The overlay is a layout aid, not a publishing asset or a platform compliance result.

Before handoff, check the exported dimensions, confirm the guide is not baked into the image, and inspect the asset at its intended display size and in the current publishing preview.
