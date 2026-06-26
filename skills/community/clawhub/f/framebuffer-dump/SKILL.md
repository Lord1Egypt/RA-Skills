---
name: framebuffer-dump
description: Dump the current STM32 LCD framebuffer via J-Link and convert it to PNG for visual comparison with Figma. Use when user asks to export, snapshot, dump, or capture what is currently displayed on device screen.
---

# Framebuffer Dump (J-Link → PNG)

Export the **actual on-device rendered frame** directly from SDRAM framebuffer and convert to PNG.

## Default parameters (PRO2)
- Device: `STM32H747XI_M7`
- FB base: `0xD0000000`
- Resolution: `604x1024`
- Pixel format: `RGB888` (3 bytes/pixel)
- Dump size: `604*1024*3 = 1,855,488 (0x1C5000)`

## One-shot workflow

### 1) Create J-Link command file
Use `scripts/dump_fb.jlink.template` and replace placeholders:
- `{{DEVICE}}`
- `{{SPEED_KHZ}}` (e.g. `12000`)
- `{{OUT_BIN}}` (absolute path)
- `{{FB_ADDR}}` (e.g. `0xD0000000`)
- `{{FB_SIZE}}` (e.g. `0x1C5000`)

### 2) Dump raw framebuffer
```bash
JLinkExe -NoGui 1 -CommandFile /tmp/jlink_dump_fb.jlink > /tmp/jlink_dump_fb.log 2>&1
```

### 3) Convert raw to PNG
```bash
python3 scripts/dump_fb.py \
  --in /path/to/fb_dump.bin \
  --out /path/to/fb_dump_604x1024.png \
  --width 604 --height 1024 --stride 3
```

## Troubleshooting
- If output bin is 0 bytes: check J-Link connection / path permissions.
- If colors look wrong: verify pixel format is RGB888 (not BGR / RGB565).
- If image shifted/corrupt: verify width/height match current display mode.
- If command hangs too long: make sure dump size is correct (`0x1C5000` for 604x1024 RGB888).

## Notes
- This method captures **real framebuffer pixels** (no camera distortion).
- Best for Figma-vs-device pixel comparison and regression snapshots.
