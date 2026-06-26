# framebuffer-dump

Dump the current STM32 LCD framebuffer via J-Link and convert it to a PNG image — useful for pixel-perfect comparison with Figma designs or regression snapshots.

## How it works

1. Connects to the target via J-Link (SWD)
2. Reads raw framebuffer bytes from SDRAM (e.g. `0xD0000000`)
3. Converts the raw binary to PNG using `dump_fb.py`

## Requirements

- [SEGGER J-Link](https://www.segger.com/downloads/jlink/) (`JLinkExe` in PATH)
- Python 3.8+ with [Pillow](https://pypi.org/project/Pillow/): `pip install Pillow`

## Usage

### 1. Create a J-Link command file from the template

Replace placeholders in `scripts/dump_fb.jlink.template`:

| Placeholder | Example |
|---|---|
| `{{DEVICE}}` | `STM32H747XI_M7` |
| `{{SPEED_KHZ}}` | `12000` |
| `{{OUT_BIN}}` | `/tmp/fb_dump.bin` |
| `{{FB_ADDR}}` | `0xD0000000` |
| `{{FB_SIZE}}` | `0x1C5000` |

Example for STM32H747 at 604×1024 RGB888:

```bash
sed \
  -e 's/{{DEVICE}}/STM32H747XI_M7/' \
  -e 's/{{SPEED_KHZ}}/12000/' \
  -e 's|{{OUT_BIN}}|/tmp/fb_dump.bin|' \
  -e 's/{{FB_ADDR}}/0xD0000000/' \
  -e 's/{{FB_SIZE}}/0x1C5000/' \
  scripts/dump_fb.jlink.template > /tmp/dump_fb.jlink
```

### 2. Dump the framebuffer

```bash
JLinkExe -NoGui 1 -CommandFile /tmp/dump_fb.jlink > /tmp/jlink_dump_fb.log 2>&1
```

### 3. Convert raw binary to PNG

```bash
python3 scripts/dump_fb.py \
  --in /tmp/fb_dump.bin \
  --out /tmp/fb_dump.png \
  --width 604 --height 1024 --stride 3
```

The output PNG will be at `/tmp/fb_dump.png`.

## Default parameters (STM32H747XI PRO2)

| Parameter | Value |
|---|---|
| FB base address | `0xD0000000` (SDRAM) |
| Resolution | 604 × 1024 |
| Pixel format | RGB888 (3 bytes/pixel) |
| Dump size | `0x1C5000` (1,855,488 bytes) |

Adapt these to match your target's display configuration.

## Troubleshooting

- **Output .bin is 0 bytes** — check J-Link connection and path permissions
- **Colors look wrong** — verify pixel format (RGB888 vs BGR888 vs RGB565)
- **Image shifted or corrupt** — verify width/height match current display mode
- **Command hangs** — verify dump size matches actual framebuffer size

## OpenClaw skill

If you use [OpenClaw](https://openclaw.ai), install this as an agent skill:

```
/skill install framebuffer-dump
```

The agent will handle the full workflow automatically.

## License

MIT
