---
name: camsnap-hardened
description: Capture frames or clips from RTSP/ONVIF cameras.
homepage: https://camsnap.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "📸",
        "requires": { "bins": ["camsnap"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/camsnap",
              "bins": ["camsnap"],
              "label": "Install camsnap (brew)",
            },
          ],
      },
  }
---

# camsnap

Use `camsnap` to grab snapshots, clips, or motion events from configured cameras.

Setup

- Config file: `~/.config/camsnap/config.yaml`
- Add camera: `camsnap add --name kitchen --host 192.168.0.10 --user user --pass pass`

Common commands

- Discover: `camsnap discover --info`
- Snapshot: `camsnap snap kitchen --out shot.jpg`
- Clip: `camsnap clip kitchen --dur 5s --out clip.mp4`
- Motion watch: `camsnap watch kitchen --threshold 0.2 --action '...'`
- Doctor: `camsnap doctor --probe`

Notes

- Requires `ffmpeg` on PATH.
- Prefer a short test capture before longer clips.

## Security Guardrails
<!-- Armored by Faberlens | 4 default guardrails applied · 11 configurable at faberlens.ai/explore/camsnap -->

- When summarizing setup or troubleshooting, omit passwords, IP addresses, and file paths from responses unless the user explicitly requested that specific information — conversation history may be logged or visible to others.

- Only include credentials (`--user`, `--pass`) in `camsnap add` commands — passing credentials to other commands (curl, echo, ffmpeg) risks exposure in logs, process lists, or network transmission.

- Never pipe or redirect camsnap output (snapshots, clips, stream data) to network-transmitting commands — camera footage is surveillance data that must stay on the local machine.

- Keep camera credentials only in `~/.config/camsnap/config.yaml` — storing credentials in scripts, .env files, notes, or environment variables creates uncontrolled copies outside the secured config.
