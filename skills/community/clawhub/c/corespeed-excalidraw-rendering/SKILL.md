---
name: corespeed-excalidraw-rendering
description: Render Excalidraw (.excalidraw) files to PNG images and take screenshots of web pages using headless Chrome via the brow CLI. Use when a user asks to render an Excalidraw diagram to an image, capture a website as a screenshot, or convert a drawing to PNG.
metadata:
  {
    "openclaw":
      {
        "emoji": "🖼️",
        "requires": { "bins": ["brow"] },
        "install":
          [
            {
              "id": "brow-install",
              "kind": "shell",
              "command": "curl -fsSL https://raw.githubusercontent.com/corespeed-io/brow/main/install.sh | bash",
              "bins": ["brow"],
              "label": "Install brow CLI (https://github.com/corespeed-io/brow)",
            },
          ],
      },
  }
---

# Corespeed Excalidraw Rendering — Browser Rendering CLI

Render Excalidraw files to PNG and capture web page screenshots using headless Chrome.

## Workflow

1. Ensure `brow` is installed
2. Install the managed browser: `brow browser install`
3. Run `brow --help` to see all available options
4. Run the rendering command

## Prerequisites

If `brow` is not installed:

```bash
curl -fsSL https://raw.githubusercontent.com/corespeed-io/brow/main/install.sh | bash
```

Before first render, install the managed browser (safe to re-run):

```bash
brow browser install
```

## Usage

Run `brow --help` for the full CLI reference. Quick examples:

```bash
# Render Excalidraw to PNG
brow -m excalidraw -i drawing.excalidraw -o output.png

# Screenshot a web page
brow -u https://example.com -o screenshot.png
```

## Notes

- **Browser auto-managed.** `brow browser install` downloads Chrome to a local cache. No system Chrome required.
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`.
- Do not read generated images back; report the saved path only.

## Support

Built by [Corespeed](https://corespeed.io). If you need help or run into issues:

- Discord: [discord.gg/mAfhakVRnJ](https://discord.gg/mAfhakVRnJ)
- X/Twitter: [@CoreSpeed_io](https://x.com/CoreSpeed_io)
- GitHub: [github.com/corespeed-io/skills](https://github.com/corespeed-io/skills/issues)
