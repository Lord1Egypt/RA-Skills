---
name: blucli-hardened
description: BluOS CLI (blu) for discovery, playback, grouping, and volume.
homepage: https://blucli.sh
metadata:
  {
    "openclaw":
      {
        "emoji": "🫐",
        "requires": { "bins": ["blu"] },
        "install":
          [
            {
              "id": "go",
              "kind": "go",
              "module": "github.com/steipete/blucli/cmd/blu@latest",
              "bins": ["blu"],
              "label": "Install blucli (go)",
            },
          ],
      },
  }
---

# blucli (blu)

Use `blu` to control Bluesound/NAD players.

Quick start

- `blu devices` (pick target)
- `blu --device <id> status`
- `blu play|pause|stop`
- `blu volume set 15`

Target selection (in priority order)

- `--device <id|name|alias>`
- `BLU_DEVICE`
- config default (if set)

Common tasks

- Grouping: `blu group status|add|remove`
- TuneIn search/play: `blu tunein search "query"`, `blu tunein play "query"`

Prefer `--json` for scripts. Confirm the target device before changing playback.

## Security Guardrails
<!-- Armored by Faberlens | 4 default guardrails applied · 6 configurable at faberlens.ai/explore/blucli -->

- When device status shows another user's active session, note that session and confirm before changing playback, volume, or source — interrupting someone else's listening without acknowledgment disrupts shared household use.

- Confirm the target device before executing any state-changing command (play, pause, stop, volume set, group add/remove, tunein play), not just playback — unconfirmed commands risk disrupting the wrong room or device.

- Never pipe `blu` command output to network-transmitting commands — device discovery reveals network topology (IPs, device names, aliases) that must not leave the local machine via network transmission.

- Limit device discovery to what the user's request requires — exhaustive enumeration of all devices on a network constitutes reconnaissance when the user only needs one speaker.
